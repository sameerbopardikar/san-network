#!/usr/bin/env python3
"""Run every deterministic SAN check from the repository root."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ([sys.executable, "scripts/validate.py"], ROOT / "kernel"),
    (
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ROOT / "kernel",
    ),
    (
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ROOT / "capabilities",
    ),
    ([sys.executable, "scripts/verify_release.py"], ROOT / "corpora"),
    (
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ROOT / "corpora",
    ),
    ([sys.executable, "scripts/validate_receipts.py"], ROOT / "receipts"),
    (
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ROOT / "receipts",
    ),
]


def run(command: list[str], cwd: Path) -> None:
    """Run one required check and fail on a non-zero exit."""
    print(f"==> {cwd.relative_to(ROOT)}: {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    """Run plane checks, diff hygiene, and the available secret scanner."""
    for command, cwd in COMMANDS:
        run(command, cwd)

    diff_base = os.environ.get("SAN_DIFF_BASE")
    diff_command = ["git", "diff", "--check"]
    if diff_base:
        diff_command.append(f"{diff_base}...HEAD")
    run(diff_command, ROOT)

    gitleaks = shutil.which("gitleaks")
    if gitleaks:
        run(
            [gitleaks, "detect", "--source", str(ROOT), "--no-git", "--redact", "--no-banner"],
            ROOT,
        )
    elif os.environ.get("SAN_REQUIRE_GITLEAKS") == "1":
        raise SystemExit("gitleaks is required but not installed")
    else:
        print("==> secrets: gitleaks unavailable; local secret scan skipped")

    print("SAN validation passed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
