#!/usr/bin/env python3
"""Run every deterministic SAN V0 check from the repository root."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ([sys.executable, "scripts/validate.py"], ROOT / "kernel"),
    ([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], ROOT / "kernel"),
    ([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], ROOT / "capabilities"),
    ([sys.executable, "scripts/verify_release.py", "agentic-engineering/releases/v0.1.0"], ROOT / "corpora"),
    ([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], ROOT / "corpora"),
]

for command, cwd in COMMANDS:
    print(f"==> {cwd.relative_to(ROOT)}: {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)

print("SAN V0 validation passed", flush=True)
