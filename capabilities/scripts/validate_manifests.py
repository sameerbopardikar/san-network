#!/usr/bin/env python3
"""Schema and semantic validation for every checked-in capability manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
CAPABILITY_ROOT = ROOT / "capabilities"
SCHEMA_PATH = ROOT / "kernel" / "schemas" / "capability-manifest.schema.json"
sys.path.insert(0, str(ROOT / "kernel" / "scripts"))
from evidence import evidence_envelope_errors  # noqa: E402


def _verified_identity_registry() -> dict[str, str]:
    registry = {}
    for path in (ROOT / "kernel" / "agents").glob("*.json"):
        card = json.loads(path.read_text())
        identity = card["github_identity"]
        if identity["state"] == "verified" and identity["login"]:
            registry[card["agent_id"]] = f"github:{identity['login'].lower()}"
    return registry


def capability_manifest_errors(
    data: object,
    *,
    identity_registry: dict[str, str] | None = None,
    fixture_evidence: bool = False,
) -> list[str]:
    """Return fail-closed identity, location, digest, and envelope errors."""
    if not isinstance(data, dict):
        return ["capability manifest must be an object"]
    registry = identity_registry if identity_registry is not None else _verified_identity_registry()
    approved_principals = set(registry.values())
    roots = [ROOT / "evidence" / "capabilities"]
    if fixture_evidence:
        roots.append(CAPABILITY_ROOT / "fixtures" / "evidence")
    errors = []
    for index, item in enumerate(data.get("evidence", [])):
        actor = item.get("actor", "")
        if actor.startswith("agent:"):
            author = registry.get(actor)
        elif actor.startswith("github:") and actor.lower() in approved_principals:
            author = actor.lower()
        else:
            author = None
        if author is None:
            errors.append(f"evidence[{index}] actor must resolve to a verified actor principal")
            author = "github:unverified"
        errors.extend(evidence_envelope_errors(
            item,
            index=index,
            repo_root=ROOT,
            allowed_roots=tuple(roots),
            kind="capability",
            event=item.get("kind", ""),
            subject_pin=data.get("kernel_pin", {"kind": "none", "value": "none"}),
            author_principal=author,
            timestamp=item.get("timestamp", ""),
            environment_digest=item.get("environment_digest"),
            verdict=item.get("verdict", ""),
        ))
    return errors


def manifest_errors(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"malformed JSON: {exc}"]
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(data)]
    if not errors:
        errors.extend(capability_manifest_errors(data))
    return sorted(set(errors))


def checked_in_manifests() -> list[Path]:
    return sorted(
        path for path in CAPABILITY_ROOT.rglob("manifest*.json")
        if "fixtures" not in path.relative_to(CAPABILITY_ROOT).parts
    )


def main() -> int:
    failed = False
    manifests = checked_in_manifests()
    if not manifests:
        print("no capability manifests found")
        return 1
    for path in manifests:
        errors = manifest_errors(path)
        if errors:
            print(f"invalid capability manifest {path.relative_to(ROOT)}: {errors}")
            failed = True
        else:
            print(f"valid capability manifest: {path.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
