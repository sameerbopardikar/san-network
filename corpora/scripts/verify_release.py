#!/usr/bin/env python3
"""Verify a corpus release's schema, provenance, links, and exact bytes."""

import hashlib
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE = SCRIPT_ROOT / "agentic-engineering" / "releases" / "v0.1.0"
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
BLOCKED_REFERENCE_MARKERS = (
    "sources/private-practitioner/",
    "receipts/2026-",
    "synthesis/indydevdan-",
    "synthesis/tactical-agentic-",
)


def sha256(path: Path) -> str:
    """Return the canonical SHA-256 digest for one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_provenance(path: Path) -> dict[str, dict]:
    """Load unique, immutable provenance rows keyed by source ID."""
    rows = {}
    required = {
        "source_id",
        "url",
        "revision",
        "revision_kind",
        "revision_url",
        "retrieved_at",
        "rights_basis",
        "evidence_lane",
        "included_raw_body",
    }
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        missing = sorted(required - set(row))
        if missing:
            raise ValueError(f"provenance line {number} missing {missing}")
        source_id = row["source_id"]
        if source_id in rows:
            raise ValueError(f"duplicate provenance source_id: {source_id}")
        if row["included_raw_body"] is not False:
            raise ValueError(f"raw source bodies are prohibited for {source_id}")
        if row["revision_kind"] != "git-commit":
            raise ValueError(f"unsupported revision kind for {source_id}")
        if not re.fullmatch(r"[a-f0-9]{40}", row["revision"]):
            raise ValueError(f"unpinned revision for {source_id}")
        rows[source_id] = row
    if not rows:
        raise ValueError("provenance is empty")
    return rows


def validate_manifest(data: dict, schema: dict) -> None:
    """Validate the manifest schema and cross-artifact invariants."""
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if errors:
        detail = "; ".join(error.message for error in errors)
        raise ValueError(f"manifest schema errors: {detail}")

    paths = [artifact["path"] for artifact in data["artifacts"]]
    if len(paths) != len(set(paths)):
        raise ValueError("manifest contains duplicate artifact paths")
    for artifact in data["artifacts"]:
        if artifact["release_version"] != data["version"]:
            raise ValueError(f"release pin mismatch: {artifact['path']}")


def validate_source_bindings(data: dict, sources: dict[str, dict]) -> None:
    """Require every artifact source ID to resolve to one provenance row."""
    known = set(sources)
    for artifact in data["artifacts"]:
        unknown = sorted(set(artifact["source_ids"]) - known)
        if unknown:
            raise ValueError(f"unknown source IDs for {artifact['path']}: {unknown}")


def validate_links(release: Path, artifact_paths: set[str]) -> None:
    """Reject unresolved release-local wiki links and excluded private paths."""
    for relative in sorted(artifact_paths):
        path = release / relative
        if path.suffix != ".md":
            continue
        text = path.read_text()
        for marker in BLOCKED_REFERENCE_MARKERS:
            if marker in text:
                raise ValueError(f"excluded reference marker in {relative}: {marker}")
        for target in WIKILINK.findall(text):
            candidates = {target, f"{target}.md"}
            if not candidates & artifact_paths:
                raise ValueError(f"unresolved wikilink in {relative}: {target}")


def validate_release(release: Path) -> tuple[str, str, int]:
    """Validate one release and return corpus ID, version, and artifact count."""
    release = release.resolve()
    repo_root = release.parents[3]
    manifest_path = release / "manifest.json"
    schema_path = repo_root / "kernel" / "schemas" / "corpus-release.schema.json"
    data = json.loads(manifest_path.read_text())
    schema = json.loads(schema_path.read_text())
    validate_manifest(data, schema)

    expected = {artifact["path"]: artifact["sha256"] for artifact in data["artifacts"]}
    actual = {
        str(path.relative_to(release)): sha256(path)
        for path in sorted(release.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        changed = sorted(
            path
            for path in set(actual) & set(expected)
            if actual[path] != expected[path]
        )
        raise ValueError(
            f"release mismatch missing={missing} extra={extra} changed={changed}"
        )

    sources = load_provenance(release / "provenance.ndjson")
    if len(sources) != data["source_count"]:
        raise ValueError("source_count does not match provenance rows")
    validate_source_bindings(data, sources)
    validate_links(release, set(expected))
    return data["corpus_id"], data["version"], len(actual)


def main() -> int:
    """CLI entry point."""
    release = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_RELEASE
    try:
        corpus_id, version, count = validate_release(release)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"release verification failed: {error}", file=sys.stderr)
        return 1
    print(f"verified {corpus_id}@{version}: {count} artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
