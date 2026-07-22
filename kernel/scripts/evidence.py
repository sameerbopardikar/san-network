"""Shared fail-closed validation for repository-contained evidence envelopes."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ENVELOPE_KEYS = {
    "schema_version",
    "kind",
    "event",
    "subject_pin",
    "author_principal",
    "timestamp",
    "environment_digest",
    "verdict",
}
SHA256_RE = re.compile(r"^(?:sha256:)?[a-f0-9]{64}$")
PRINCIPAL_RE = re.compile(r"^github:[A-Za-z0-9-]{1,39}$")


def evidence_envelope_errors(
    item: dict,
    *,
    index: int,
    repo_root: Path,
    allowed_roots: tuple[Path, ...],
    kind: str,
    event: str,
    subject_pin: dict,
    author_principal: str,
    timestamp: str,
    environment_digest: str | None,
    verdict: str,
) -> list[str]:
    """Verify path, digest, and typed envelope bindings for one evidence item."""
    prefix = f"evidence[{index}]"
    uri = item.get("uri", "")
    parsed = urlsplit(uri)
    if parsed.query or parsed.fragment:
        return [f"{prefix} uri must not contain a query or fragment"]
    if parsed.scheme or parsed.netloc:
        return [f"{prefix} must use a repository-relative uri"]
    relative = Path(parsed.path)
    if not parsed.path or relative.is_absolute() or ".." in relative.parts:
        return [f"{prefix} uri must stay inside the repository"]
    target = (repo_root / relative).resolve()
    resolved_roots = tuple(root.resolve() for root in allowed_roots)
    if not any(target == root or root in target.parents for root in resolved_roots):
        return [f"{prefix} must live under a dedicated evidence root"]
    if not target.is_file():
        return [f"{prefix} target does not exist inside the repository: {uri}"]
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    expected_digest = str(item.get("sha256", "")).removeprefix("sha256:")
    errors = []
    if actual != expected_digest:
        errors.append(f"{prefix} sha256 does not match repository content: {uri}")
    try:
        envelope = json.loads(target.read_text())
    except (UnicodeDecodeError, json.JSONDecodeError):
        return errors + [f"{prefix} target must be a JSON evidence envelope"]
    if not isinstance(envelope, dict) or set(envelope) != ENVELOPE_KEYS:
        return errors + [f"{prefix} target must be an exact typed evidence envelope"]
    expected = {
        "schema_version": "san.evidence/v1",
        "kind": kind,
        "event": event,
        "subject_pin": subject_pin,
        "author_principal": author_principal,
        "timestamp": timestamp,
        "environment_digest": environment_digest,
        "verdict": verdict,
    }
    for field, value in expected.items():
        if envelope.get(field) != value:
            errors.append(f"{prefix} envelope {field} does not match the evidence claim")
    if not PRINCIPAL_RE.fullmatch(str(envelope.get("author_principal", ""))):
        errors.append(f"{prefix} envelope author_principal is invalid")
    if not SHA256_RE.fullmatch(str(envelope.get("environment_digest", ""))):
        errors.append(f"{prefix} envelope environment_digest is invalid")
    return errors
