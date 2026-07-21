#!/usr/bin/env python3
"""Validate receipt fixtures and enforce cross-field role separation."""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "kernel" / "schemas" / "adoption-receipt.schema.json"
VALID_DIR = ROOT / "receipts" / "fixtures" / "valid"
INVALID_DIR = ROOT / "receipts" / "fixtures" / "invalid"
ROLE_FIELDS = ("executor_agent_id", "reviewer_agent_id", "verifier_agent_id")


def validation_errors(path: Path) -> list[str]:
    """Return schema and cross-field errors for one receipt."""
    schema = json.loads(SCHEMA_PATH.read_text())
    data = json.loads(path.read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(data)]
    roles = [data.get(field) for field in ROLE_FIELDS]
    if all(roles) and len(set(roles)) != len(roles):
        errors.append("executor, reviewer, and verifier must be pairwise distinct")
    return sorted(errors)


def main() -> int:
    """Validate positive fixtures and prove negative fixtures are rejected."""
    failed = False
    for path in sorted(VALID_DIR.glob("*.json")):
        errors = validation_errors(path)
        if errors:
            print(f"invalid expected-valid receipt {path}: {errors}")
            failed = True
        else:
            print(f"valid receipt: {path.relative_to(ROOT)}")

    for path in sorted(INVALID_DIR.glob("*.json")):
        errors = validation_errors(path)
        if not errors:
            print(f"unexpectedly valid adversarial receipt: {path}")
            failed = True
        else:
            print(f"rejected adversarial receipt: {path.relative_to(ROOT)}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
