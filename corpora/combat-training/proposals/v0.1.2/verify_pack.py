#!/usr/bin/env python3
"""Verify the bilateral combat-training pack and corrected State of Fighter."""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(MANIFEST.read_text())
    if data.get("schema_version") != 1:
        raise ValueError("unsupported schema_version")
    if data.get("pack_id") != "aneek-combat-training":
        raise ValueError("unexpected pack_id")
    expected = {row["path"]: row["sha256"] for row in data["artifacts"]}
    if len(expected) != len(data["artifacts"]):
        raise ValueError("duplicate artifact path")
    actual = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.name != "manifest.json" and "__pycache__" not in path.parts
    }
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        changed = sorted(
            path for path in set(actual) & set(expected) if actual[path] != expected[path]
        )
        raise ValueError(
            f"pack mismatch missing={missing} extra={extra} changed={changed}"
        )
    state = json.loads((ROOT / "state" / "aneek-state-of-fighter.json").read_text())
    if state.get("state_version") != "1.1.0":
        raise ValueError("unexpected State of Fighter version")
    if state.get("goal", {}).get("id") != "goals/aneek-fighter-development":
        raise ValueError("State of Fighter is not anchored to the fighter-development goal")
    skills = {row["id"]: row for row in state["skills"]}
    if skills["lead-hook"]["state"] != "clean_isolated_drilling":
        raise ValueError("lead hook state is incorrect")
    for skill_id in ("rear-hook", "lead-uppercut", "rear-uppercut"):
        if skills[skill_id]["state"] != "not_introduced":
            raise ValueError(f"{skill_id} must remain not_introduced")
    program = state["current_program"]
    if program["completed_session"] != "A" or program["next_session"] != "B":
        raise ValueError("current session progression is incorrect")
    print(f"verified {data['pack_id']}@{data['version']}: {len(actual)} artifacts")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
