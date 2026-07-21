#!/usr/bin/env python3
"""Validate receipt fixtures and enforce semantic adoption invariants."""

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "kernel" / "schemas" / "adoption-receipt.schema.json"
VALID_DIR = ROOT / "receipts" / "fixtures" / "valid"
INVALID_DIR = ROOT / "receipts" / "fixtures" / "invalid"
ROLE_FIELDS = ("executor_agent_id", "reviewer_agent_id", "verifier_agent_id")


def _semantic_errors(data: object) -> list[str]:
    """Return cross-field errors without assuming a schema-valid mapping."""
    if not isinstance(data, dict):
        return []
    errors = []
    roles = [data.get(field) for field in ROLE_FIELDS]
    if all(isinstance(role, str) for role in roles) and len(set(roles)) != len(roles):
        errors.append("executor, reviewer, and verifier must be pairwise distinct")

    event = data.get("event_type")
    result = data.get("result")
    benchmark = data.get("benchmark_result")
    previous = data.get("previous_baseline_pin")
    candidate = data.get("candidate_pin")
    resulting = data.get("resulting_baseline_pin")
    rollback = data.get("rollback_target_pin")
    subject = data.get("subject_pin")

    if event in {"adopt", "promote"}:
        if benchmark != "passed" or result != "accepted":
            errors.append("adopt/promote requires a passed benchmark and accepted result")
        if resulting != candidate or subject != candidate:
            errors.append("adopt/promote subject and resulting baseline must equal candidate pin")
        if previous == candidate:
            errors.append("adopt/promote candidate must differ from previous baseline")
    elif event == "reject":
        if result != "rejected" or resulting != previous:
            errors.append("reject must retain the previous baseline")
    elif event in {"rollback", "demote"}:
        if result != "rolled-back" or resulting != rollback:
            errors.append("rollback/demote must restore the exact rollback target")
    elif event in {"rollback-failed", "revoke"}:
        if not isinstance(resulting, dict) or resulting.get("kind") != "none":
            errors.append("failed restoration or revocation must record baseline pin none")

    maturity = data.get("evidence_maturity")
    claims = data.get("claims")
    if maturity != "declared" and isinstance(claims, list) and maturity not in claims:
        errors.append("evidence maturity must be present in claims")
    if result == "accepted" and benchmark != "passed":
        errors.append("an accepted result requires a passed benchmark")

    evidence = data.get("evidence")
    if isinstance(evidence, list):
        for index, item in enumerate(evidence):
            if isinstance(item, str):
                errors.append("evidence items must be structured objects, not URI strings")
                continue
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            digest = item.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest or ""):
                errors.append(f"evidence[{index}] requires an immutable sha256 digest")
            uri = item.get("uri")
            if not isinstance(uri, str) or not uri.strip():
                errors.append(f"evidence[{index}] requires a non-empty uri")
            item_pin = item.get("subject_pin")
            if subject is not None and item_pin != subject:
                errors.append(
                    f"evidence[{index}] subject_pin must match the receipt subject_pin"
                )
    return errors


def validation_errors(path: Path) -> list[str]:
    """Return schema and semantic errors for one receipt file."""
    try:
        schema = json.loads(SCHEMA_PATH.read_text())
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"malformed JSON: {exc.msg} (line {exc.lineno} column {exc.colno})"]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(data)]
    errors.extend(_semantic_errors(data))
    return sorted(set(errors))


def _operational_receipts() -> list[Path]:
    """Return committed non-fixture receipt JSON under receipts/.

    Fail closed on unexpected non-JSON operational artifacts (except README.md)
    so disposition prose cannot bypass the schema gate by living beside receipts.
    """
    skip_roots = {"fixtures", "scripts", "tests", ".pytest_cache"}
    found = []
    root = ROOT / "receipts"
    unexpected = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in skip_roots:
            continue
        if path == root / "README.md" or path.name == ".gitkeep":
            continue
        if path.suffix == ".json":
            found.append(path)
            continue
        unexpected.append(path)
    if unexpected:
        rel = ", ".join(str(p.relative_to(ROOT)) for p in unexpected)
        raise SystemExit(
            "unsupported non-JSON operational receipt artifact(s): "
            f"{rel}. Move prose dispositions under docs/ or convert to schema-valid JSON."
        )
    return found


def main() -> int:
    """Validate positive fixtures, adversarial fixtures, and operational receipts."""
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

    for path in _operational_receipts():
        errors = validation_errors(path)
        if errors:
            print(f"invalid operational receipt {path}: {errors}")
            failed = True
        else:
            print(f"valid operational receipt: {path.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
