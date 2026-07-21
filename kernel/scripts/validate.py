#!/usr/bin/env python3
"""Validate SAN kernel schemas, Agent Cards, and work-object invariants."""

import json
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
MATURITY_EVIDENCE = {
    "specified": set(),
    "built": {"build"},
    "tested": {"build", "test"},
    "independently-reviewed": {
        "build",
        "test",
        "coderabbit-review",
        "independent-review",
    },
    "destination-verified": {
        "build",
        "test",
        "coderabbit-review",
        "independent-review",
        "destination-verification",
    },
    "adopted": {
        "build",
        "test",
        "coderabbit-review",
        "independent-review",
        "destination-verification",
        "adoption",
    },
    "monitored": {
        "build",
        "test",
        "coderabbit-review",
        "independent-review",
        "destination-verification",
        "adoption",
        "monitoring",
    },
    "rolled-back": {"rollback"},
}


def work_object_errors(data: dict, validator: Draft202012Validator) -> list[str]:
    """Return schema and cross-field errors for one SAN work object."""
    errors = [error.message for error in validator.iter_errors(data)]
    if errors:
        return errors

    roles = data["roles"]
    execution_roles = [roles["executor"], roles["reviewer"], roles["verifier"]]
    if len(set(execution_roles)) != 3:
        errors.append("executor, reviewer, and verifier must be pairwise distinct")

    included = set(data["scope"]["include"])
    excluded = set(data["scope"]["exclude"])
    if included & excluded:
        errors.append("scope include and exclude paths overlap")
    if not set(data["writer_lease"]["paths"]).issubset(included):
        errors.append("writer lease paths must be declared in scope.include")

    subject_sha = data["subject_sha"]
    if any(item["subject_sha"] != subject_sha for item in data["evidence"]):
        errors.append("all evidence must bind the current subject_sha")

    evidence_kinds = {item["kind"] for item in data["evidence"]}
    missing = MATURITY_EVIDENCE[data["maturity"]] - evidence_kinds
    if missing:
        errors.append(
            f"maturity {data['maturity']} is missing evidence kinds: {sorted(missing)}"
        )
    return errors


def main() -> int:
    """Validate schema syntax, Agent Cards, and positive/adversarial fixtures."""
    schemas = {}
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        data = json.loads(path.read_text())
        Draft202012Validator.check_schema(data)
        schemas[path.name] = data
        print(f"valid schema: {path.relative_to(ROOT)}")

    agent_schema = schemas["agent-card.schema.json"]
    agent_validator = Draft202012Validator(
        agent_schema,
        format_checker=FormatChecker(),
    )
    seen = set()
    for path in sorted(AGENT_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        errors = sorted(
            agent_validator.iter_errors(data),
            key=lambda error: list(error.path),
        )
        if errors:
            detail = "; ".join(error.message for error in errors)
            raise SystemExit(f"invalid Agent Card {path}: {detail}")
        agent_id = data["agent_id"]
        if agent_id in seen:
            raise SystemExit(f"duplicate Agent Card identity: {agent_id}")
        seen.add(agent_id)
        print(f"valid Agent Card: {path.relative_to(ROOT)}")

    if seen != EXPECTED_AGENTS:
        raise SystemExit(
            f"Agent Card set mismatch missing={sorted(EXPECTED_AGENTS - seen)} "
            f"extra={sorted(seen - EXPECTED_AGENTS)}"
        )

    work_schema = schemas["work-object.schema.json"]
    work_validator = Draft202012Validator(
        work_schema,
        format_checker=FormatChecker(),
    )
    valid_fixture = json.loads((WORK_FIXTURE_DIR / "valid.json").read_text())
    valid_errors = work_object_errors(valid_fixture, work_validator)
    if valid_errors:
        raise SystemExit(f"invalid work-object fixture: {'; '.join(valid_errors)}")
    print("valid work-object fixture: fixtures/work-object/valid.json")

    for name in ("invalid-same-role.json", "invalid-stale-evidence.json"):
        invalid = json.loads((WORK_FIXTURE_DIR / name).read_text())
        if not work_object_errors(invalid, work_validator):
            raise SystemExit(f"adversarial work-object fixture was accepted: {name}")
        print(f"rejected adversarial work-object fixture: fixtures/work-object/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
