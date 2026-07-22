#!/usr/bin/env python3
"""Validate SAN kernel schemas, Agent Cards, and work-object invariants."""

import fnmatch
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
AGENT_DIR = ROOT / "agents"
WORK_FIXTURE_DIR = ROOT / "fixtures" / "work-object"
EXPECTED_AGENTS = {
    "agent:expert",
    "agent:gideon",
    "agent:gerri",
    "agent:nemertes",
}
INDEPENDENT_GATE_EVIDENCE = {
    "build",
    "test",
    "secret-scan",
    "rights-scan",
    "rollback-test",
    "coderabbit-review",
    "independent-review",
}
MATURITY_EVIDENCE = {
    "specified": set(),
    "built": {"build"},
    "tested": {"build", "test"},
    "independently-reviewed": INDEPENDENT_GATE_EVIDENCE,
    "destination-verified": INDEPENDENT_GATE_EVIDENCE | {"destination-verification"},
    "adopted": INDEPENDENT_GATE_EVIDENCE
    | {"destination-verification", "adoption"},
    "monitored": INDEPENDENT_GATE_EVIDENCE
    | {"destination-verification", "adoption", "monitoring"},
    "rolled-back": {"rollback"},
}


def _norm_digest(value: str) -> str:
    """Strip the optional sha256: prefix so digests compare by hash bytes."""
    return value.removeprefix("sha256:")


def _identity_registry() -> dict[str, str]:
    """Map verified SAN agent IDs to canonical GitHub principals."""
    registry = {}
    for path in AGENT_DIR.glob("*.json"):
        card = json.loads(path.read_text())
        github = card["github_identity"]
        if github["state"] == "verified" and github["login"]:
            registry[card["agent_id"]] = f"github:{github['login'].lower()}"
    return registry


def _canonical_identity(value: str) -> str:
    """Fold an identity string for case/whitespace-insensitive comparison."""
    return value.strip().casefold()


def _static_prefix(pattern: str) -> str:
    """Return the literal prefix before the first glob metacharacter."""
    return re.split(r"[*?[]", pattern, maxsplit=1)[0]


def _patterns_overlap(left: str, right: str) -> bool:
    """Conservatively detect exact, glob, and containment overlap."""
    if left == right or fnmatch.fnmatchcase(left, right) or fnmatch.fnmatchcase(right, left):
        return True
    left_prefix = _static_prefix(left)
    right_prefix = _static_prefix(right)
    return bool(
        left_prefix
        and right_prefix
        and (
            left_prefix.startswith(right_prefix)
            or right_prefix.startswith(left_prefix)
        )
    )


def _parse_time(value: str) -> datetime:
    """Parse a JSON Schema date-time into an aware UTC datetime."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)




def adoption_receipt_errors(
    data: dict,
    validator: Draft202012Validator,
) -> list[str]:
    """Return schema and separation-of-duties errors for one adoption receipt."""
    errors = [error.message for error in validator.iter_errors(data)]
    if errors:
        return errors
    roles = [
        data.get("executor_agent_id"),
        data.get("reviewer_agent_id"),
        data.get("verifier_agent_id"),
    ]
    if any(role is None for role in roles):
        return errors
    if len(set(roles)) != 3:
        errors.append("executor, reviewer, and verifier must be pairwise distinct")
    if data.get("event_type") in {"adopt", "promote"}:
        if data.get("subject_pin") != data.get("candidate_pin"):
            errors.append("subject_pin must equal candidate_pin for adopt/promote")
        if data.get("resulting_baseline_pin") != data.get("candidate_pin"):
            errors.append(
                "resulting_baseline_pin must equal candidate_pin for adopt/promote"
            )
    return errors

def work_object_errors(
    data: dict,
    validator: Draft202012Validator,
    *,
    now: datetime | None = None,
) -> list[str]:
    """Return schema and semantic cross-field errors for one SAN work object."""
    errors = [error.message for error in validator.iter_errors(data)]
    if errors:
        return errors

    roles = data["roles"]
    # BK-15: canonicalize (strip+casefold) all four coordination identities
    # before checking pairwise separation, so case/alias variation such as
    # "agent:expert" vs "AGENT:EXPERT" cannot bypass the distinctness gate.
    # All four (executor/reviewer/verifier/merger) must be present and
    # pairwise distinct; the merger is a github: principal string, the other
    # three are agent: identities, but any reuse across any of the four
    # (not merely executor vs the other two) is a separation-of-duties defect.
    identity_fields = {
        "executor": roles.get("executor"),
        "reviewer": roles.get("reviewer"),
        "verifier": roles.get("verifier"),
        "merger": roles.get("merger"),
    }
    missing_identities = [name for name, value in identity_fields.items() if not value]
    if missing_identities:
        errors.append(
            "roles.executor, roles.reviewer, roles.verifier, and roles.merger "
            f"must all be present: missing {sorted(missing_identities)}"
        )
    else:
        canonical = {
            name: _canonical_identity(value) for name, value in identity_fields.items()
        }
        seen: dict[str, list[str]] = {}
        for name, value in canonical.items():
            seen.setdefault(value, []).append(name)
        collided = {value: names for value, names in seen.items() if len(names) > 1}
        if collided:
            errors.append(
                "executor, reviewer, verifier, and merger must be pairwise distinct "
                f"(case/whitespace-insensitive): collisions {collided}"
            )

    registry = _identity_registry()
    executor_principal = registry.get(roles["executor"])
    if executor_principal is None:
        errors.append("executor must resolve to a verified agent identity before merger checks")
    elif executor_principal == _canonical_identity(roles["merger"]):
        errors.append("merger must not resolve to the executor identity")

    included = data["scope"]["include"]
    excluded = data["scope"]["exclude"]
    if any(_patterns_overlap(left, right) for left in included for right in excluded):
        errors.append("scope include and exclude paths overlap")
    if not set(data["writer_lease"]["paths"]).issubset(set(included)):
        errors.append("writer lease paths must be declared in scope.include")

    # BK-16: reject scope.exclude entries that are malformed (non-string,
    # empty, absolute, home-relative, or containing a ".."/"." traversal
    # segment) instead of silently dropping them from the overlap check, and
    # require changed_paths to be present and non-empty before evaluating it
    # against scope.
    def _malformed_path_entry(value: object) -> str | None:
        if not isinstance(value, str) or not value.strip():
            return "non-string or empty path entry"
        if value.startswith("/") or value.startswith("~"):
            return f"absolute or home-relative path not allowed: {value}"
        segments = re.split(r"/+", value)
        if any(segment in (".", "..") for segment in segments):
            return f"path traversal segment not allowed: {value}"
        return None

    for label, collection in (("scope.include", included), ("scope.exclude", excluded)):
        for entry in collection:
            reason = _malformed_path_entry(entry)
            if reason:
                errors.append(f"{label} contains a malformed entry: {reason}")

    changed_paths = data.get("changed_paths") or []
    if not changed_paths:
        errors.append("changed_paths must be present and non-empty")
    for changed in changed_paths:
        reason = _malformed_path_entry(changed)
        if reason:
            errors.append(f"changed_paths contains a malformed entry: {reason}")
            continue
        if not any(fnmatch.fnmatchcase(changed, pattern) for pattern in included):
            errors.append(f"changed path is outside scope.include: {changed}")
        if any(fnmatch.fnmatchcase(changed, pattern) for pattern in excluded):
            errors.append(f"changed path intersects scope.exclude: {changed}")

    # Reject a schema-valid but Git-impossible branch name (e.g. "../main")
    # by checking it against Git's own ref-format rules rather than relying
    # solely on the regex pattern in the JSON Schema.
    branch = data.get("branch", "")
    ref_check = subprocess.run(
        ["git", "check-ref-format", "--branch", branch],
        capture_output=True,
        text=True,
    )
    if ref_check.returncode != 0:
        errors.append(f"branch is not a valid Git ref: {branch!r}")

    lease = data["writer_lease"]
    if lease["state"] != "active":
        errors.append("writer lease must be active")
    reference_time = now or datetime.now(timezone.utc)
    if _parse_time(lease["expires_at"]) <= reference_time:
        errors.append("writer lease must not be expired")

    subject_sha = data["subject_sha"]
    evidence = data["evidence"]
    if any(item["subject_sha"] != subject_sha for item in evidence):
        errors.append("all evidence must bind the current subject_sha")

    expected_actor_verdict = {
        "build": (roles["executor"], "pass"),
        "test": (roles["verifier"], "pass"),
        "secret-scan": (roles["verifier"], "pass"),
        "rights-scan": (roles["verifier"], "pass"),
        "rollback-test": (roles["verifier"], "pass"),
        "coderabbit-review": ("github:coderabbitai", "go"),
        "independent-review": (roles["reviewer"], "go"),
        "destination-verification": (roles["verifier"], "pass"),
        "adoption": (roles["verifier"], "pass"),
        "monitoring": (roles["verifier"], "pass"),
        "rollback": (roles["verifier"], "pass"),
    }
    for item in evidence:
        expected = expected_actor_verdict[item["kind"]]
        if (item["actor"], item["verdict"]) != expected:
            errors.append(
                f"{item['kind']} evidence requires actor/verdict {expected}, "
                f"got {(item['actor'], item['verdict'])}"
            )
        if (
            data["golden_fixture"]["required"]
            and _norm_digest(item["environment_digest"])
            != _norm_digest(data["golden_fixture"]["environment_digest"])
        ):
            errors.append(f"{item['kind']} evidence uses the wrong environment digest")

    evidence_kinds = {item["kind"] for item in evidence}
    missing = MATURITY_EVIDENCE[data["maturity"]] - evidence_kinds
    if missing:
        errors.append(
            f"maturity {data['maturity']} is missing evidence kinds: {sorted(missing)}"
        )
    if data["maturity"] in {
        "independently-reviewed",
        "destination-verified",
        "adopted",
        "monitored",
    } and not data["rollback"]["verified"]:
        errors.append("reviewed or promoted maturity requires verified rollback")
    return errors


def main() -> int:
    """Validate schema syntax, Agent Cards, and positive/adversarial fixtures."""
    schemas = {}
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        data = json.loads(path.read_text())
        Draft202012Validator.check_schema(data)
        schemas[path.name] = data
        print(f"valid schema: {path.relative_to(ROOT)}")

    agent_validator = Draft202012Validator(
        schemas["agent-card.schema.json"], format_checker=FormatChecker()
    )
    seen = set()
    for path in sorted(AGENT_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        errors = sorted(agent_validator.iter_errors(data), key=lambda error: list(error.path))
        if errors:
            detail = "; ".join(error.message for error in errors)
            raise SystemExit(f"invalid Agent Card {path}: {detail}")
        if data["agent_id"] in seen:
            raise SystemExit(f"duplicate Agent Card identity: {data['agent_id']}")
        seen.add(data["agent_id"])
        print(f"valid Agent Card: {path.relative_to(ROOT)}")
    if seen != EXPECTED_AGENTS:
        raise SystemExit(
            f"Agent Card set mismatch missing={sorted(EXPECTED_AGENTS - seen)} "
            f"extra={sorted(seen - EXPECTED_AGENTS)}"
        )

    work_validator = Draft202012Validator(
        schemas["work-object.schema.json"], format_checker=FormatChecker()
    )
    valid_fixture = json.loads((WORK_FIXTURE_DIR / "valid.json").read_text())
    valid_errors = work_object_errors(valid_fixture, work_validator)
    if valid_errors:
        raise SystemExit(f"invalid work-object fixture: {'; '.join(valid_errors)}")
    print("valid work-object fixture: fixtures/work-object/valid.json")

    for path in sorted(WORK_FIXTURE_DIR.glob("invalid-*.json")):
        invalid = json.loads(path.read_text())
        if not work_object_errors(invalid, work_validator):
            raise SystemExit(f"adversarial work-object fixture was accepted: {path.name}")
        print(f"rejected adversarial work-object fixture: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
