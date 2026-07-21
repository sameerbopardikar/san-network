#!/usr/bin/env python3
"""Validate SAN kernel schemas, Agent Cards, and work-object invariants."""

import fnmatch
import json
import re
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


def _identity_registry() -> dict[str, str]:
    """Map verified SAN agent IDs to canonical GitHub principals."""
    registry = {}
    for path in AGENT_DIR.glob("*.json"):
        card = json.loads(path.read_text())
        github = card["github_identity"]
        if github["state"] == "verified" and github["login"]:
            registry[card["agent_id"]] = f"github:{github['login'].lower()}"
    return registry


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
    execution_roles = [roles["executor"], roles["reviewer"], roles["verifier"]]
    if len(set(execution_roles)) != 3:
        errors.append("executor, reviewer, and verifier must be pairwise distinct")

    registry = _identity_registry()
    executor_principal = registry.get(roles["executor"])
    if executor_principal is None:
        errors.append("executor must resolve to a verified agent identity before merger checks")
    elif executor_principal == roles["merger"].lower():
        errors.append("merger must not resolve to the executor identity")

    included = data["scope"]["include"]
    excluded = data["scope"]["exclude"]
    if any(_patterns_overlap(left, right) for left in included for right in excluded):
        errors.append("scope include and exclude paths overlap")
    if not set(data["writer_lease"]["paths"]).issubset(set(included)):
        errors.append("writer lease paths must be declared in scope.include")
    for changed in data["changed_paths"]:
        if not any(fnmatch.fnmatchcase(changed, pattern) for pattern in included):
            errors.append(f"changed path is outside scope.include: {changed}")
        if any(fnmatch.fnmatchcase(changed, pattern) for pattern in excluded):
            errors.append(f"changed path intersects scope.exclude: {changed}")

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
            and item["environment_digest"]
            != data["golden_fixture"]["environment_digest"]
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
