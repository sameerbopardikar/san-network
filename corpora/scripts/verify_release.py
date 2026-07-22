#!/usr/bin/env python3
"""Verify a corpus release's schema, provenance, links, and exact bytes."""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
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
    """Require every artifact source ID to resolve to one complete provenance row.

    When an artifact embeds ``source_cards``, each card must match the provenance
    row field-for-field (url, revision, revision_kind, revision_url, retrieved_at,
    rights_basis, evidence_lane, included_raw_body) and its ``source_id`` must be
    listed in that artifact's ``source_ids``. Artifacts that only list
    ``source_ids`` still require known IDs against the complete provenance table.
    """
    known = set(sources)
    meta_fields = (
        "url",
        "revision",
        "revision_kind",
        "revision_url",
        "retrieved_at",
        "rights_basis",
        "evidence_lane",
        "included_raw_body",
    )
    for artifact in data["artifacts"]:
        path = artifact["path"]
        declared = set(artifact["source_ids"])
        unknown = sorted(declared - known)
        if unknown:
            raise ValueError(f"unknown source IDs for {path}: {unknown}")
        cards = artifact.get("source_cards") or []
        for card in cards:
            source_id = card.get("source_id")
            if source_id not in sources:
                raise ValueError(f"unknown source card for {path}: {source_id}")
            if source_id not in declared:
                raise ValueError(
                    f"source card not declared in artifact source_ids for {path}: "
                    f"{source_id}"
                )
            row = sources[source_id]
            for field in meta_fields:
                if field not in card:
                    raise ValueError(
                        f"source card missing {field} for {path}: {source_id}"
                    )
                if card[field] != row[field]:
                    raise ValueError(
                        f"source card metadata mismatch for {path}: "
                        f"{source_id}.{field}"
                    )


SOURCE_CARD_FIELD_MAP = {
    "URL": "url",
    "Immutable revision": "revision",
    "Revision URL": "revision_url",
    "Retrieved at": "retrieved_at",
    "Evidence lane": "evidence_lane",
    "Rights basis": "rights_basis",
}


def _parse_source_card_markdown(text: str) -> dict:
    """Extract provenance-bound fields from an on-disk source-card Markdown body."""
    fields: dict[str, object] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("- "):
            continue
        body = line[2:].strip()
        if ":" not in body:
            continue
        label, _, value = body.partition(":")
        label = label.strip()
        value = value.strip()
        key = SOURCE_CARD_FIELD_MAP.get(label)
        if key is None:
            if label == "Raw third-party body included":
                lowered = value.lower()
                if lowered in {"no", "false", "0"}:
                    fields["included_raw_body"] = False
                elif lowered in {"yes", "true", "1"}:
                    fields["included_raw_body"] = True
                else:
                    raise ValueError(
                        f"unparseable included_raw_body value: {value!r}"
                    )
            continue
        fields[key] = value
    return fields


def validate_on_disk_source_cards(release: Path, sources: dict[str, dict]) -> None:
    """Require each sources/*.md artifact to match its provenance row field-for-field."""
    required = (
        "url",
        "revision",
        "revision_url",
        "retrieved_at",
        "rights_basis",
        "evidence_lane",
        "included_raw_body",
    )
    for source_id, row in sorted(sources.items()):
        relative = f"sources/{source_id}.md"
        path = release / relative
        if not path.is_file():
            raise ValueError(f"missing on-disk source card: {relative}")
        try:
            card = _parse_source_card_markdown(path.read_text())
        except ValueError as exc:
            raise ValueError(f"source card parse failed for {relative}: {exc}") from exc
        for field in required:
            if field not in card:
                raise ValueError(f"source card missing {field} for {relative}")
            if card[field] != row[field]:
                raise ValueError(
                    f"on-disk source card provenance mismatch for {relative}: "
                    f"{field} card={card[field]!r} provenance={row[field]!r}"
                )


def _front_matter(text: str) -> dict:
    """Parse optional YAML front matter without external YAML deps.

    Only extracts the relations list shape used by release concepts.
    Other front-matter keys are ignored.
    """
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    block = parts[1]
    relations: list[dict] = []
    in_relations = False
    current: dict | None = None

    def _clean_value(value: str) -> str:
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            return value[1:-1]
        return value

    for raw in block.splitlines():
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" \t"))
        stripped = raw.strip()
        if indent == 0 and stripped.endswith(":") and not stripped.startswith("-"):
            key = stripped[:-1].strip()
            in_relations = key == "relations"
            if current is not None:
                relations.append(current)
                current = None
            continue
        if not in_relations:
            continue
        if stripped.startswith("- "):
            if current is not None:
                relations.append(current)
            current = {}
            rest = stripped[2:].strip()
            if rest and ":" in rest:
                key, _, value = rest.partition(":")
                current[key.strip()] = _clean_value(value)
            continue
        if current is not None and ":" in stripped:
            key, _, value = stripped.partition(":")
            current[key.strip()] = _clean_value(value)
    if current is not None:
        relations.append(current)
    return {"relations": relations} if relations else {}


def _resolve_relation_target(target: str, artifact_paths: set[str]) -> bool:
    """Return True when a normalized same-directory relation target resolves.

    Rejects absolute paths, parent-directory traversal, and the historical
    ``concepts/`` stripping alias that allowed cross-directory matches. Bare
    slugs may still resolve under ``concepts/``.
    """
    cleaned = target.strip()
    if not cleaned or cleaned.startswith("/"):
        return False
    if chr(92) in cleaned:
        return False
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    parts = Path(cleaned).parts
    if any(part in {"..", ""} for part in parts):
        return False
    cleaned = Path(*parts).as_posix() if parts else ""
    if not cleaned:
        return False
    candidates = {cleaned, f"{cleaned}.md"}
    if "/" not in cleaned:
        candidates.add(f"concepts/{cleaned}.md")
        candidates.add(f"concepts/{cleaned}")
    return bool(candidates & artifact_paths)


def validate_links(release: Path, artifact_paths: set[str]) -> None:
    """Reject unresolved release-local wiki links, relation targets, and private paths."""
    for relative in sorted(artifact_paths):
        path = release / relative
        if path.suffix != ".md":
            continue
        body = path.read_text()
        for marker in BLOCKED_REFERENCE_MARKERS:
            if marker in body:
                raise ValueError(f"excluded reference marker in {relative}: {marker}")
        for target in WIKILINK.findall(body):
            candidates = {target, f"{target}.md"}
            if not candidates & artifact_paths:
                raise ValueError(f"unresolved wikilink in {relative}: {target}")
        meta = _front_matter(body)
        relations = meta.get("relations") or []
        if relations and not isinstance(relations, list):
            raise ValueError(f"relations must be a list in {relative}")
        for index, relation in enumerate(relations):
            if not isinstance(relation, dict) or "target" not in relation:
                raise ValueError(f"relation[{index}] missing target in {relative}")
            target = relation["target"]
            if not isinstance(target, str) or not target.strip():
                raise ValueError(f"relation[{index}] empty target in {relative}")
            if not _resolve_relation_target(target, artifact_paths):
                raise ValueError(
                    f"unresolved relation target in {relative}: {target}"
                )


def _parse_iso_utc(value: str) -> datetime:
    """Parse an ISO-8601 timestamp with explicit timezone; normalize to UTC.

    Offsets and trailing Z are accepted. Naive (offset-less) timestamps are
    rejected so provenance cannot silently assume UTC.
    """
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError(
            f"ISO-8601 timestamp requires explicit timezone offset or Z: {value!r}"
        )
    return dt.astimezone(timezone.utc)


def validate_release(release: Path) -> tuple[str, str, int]:
    """Validate one release and return corpus ID, version, and artifact count."""
    release = release.resolve()
    repo_root = SCRIPT_ROOT.parent
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
    parsed_retrievals: list[tuple[str, datetime]] = []
    for source_id, row in sources.items():
        retrieved_at = row["retrieved_at"]
        if not isinstance(retrieved_at, str):
            raise ValueError(f"retrieved_at must be a string for {source_id}")
        try:
            parsed_retrievals.append((retrieved_at, _parse_iso_utc(retrieved_at)))
        except ValueError as exc:
            raise ValueError(
                f"provenance retrieved_at must be ISO-8601 for {source_id} "
                f"(retrieved_at={retrieved_at!r}): {exc}"
            ) from exc
    latest_retrieval, latest_dt = max(parsed_retrievals, key=lambda item: item[1])
    released_at = data.get("released_at")
    if not isinstance(released_at, str):
        raise ValueError("released_at must be an ISO-8601 timestamp string")
    try:
        released_dt = _parse_iso_utc(released_at)
    except ValueError as exc:
        raise ValueError(
            f"released_at must be ISO-8601 "
            f"(released_at={released_at!r}): {exc}"
        ) from exc
    if released_dt <= latest_dt:
        raise ValueError(
            f"released_at must be strictly after latest provenance retrieved_at "
            f"(released_at={released_at!r} latest_retrieval={latest_retrieval!r})"
        )
    if len(sources) != data["source_count"]:
        raise ValueError("source_count does not match provenance rows")
    validate_source_bindings(data, sources)
    validate_on_disk_source_cards(release, sources)
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
