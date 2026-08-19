"""Run the local quality gates used by CI.

Usage:
    python scripts/quality_gate.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*command: str) -> None:
    """Run one quality-gate command and stop on failure."""
    print(f"\n$ {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    """Compile, lint, and test with coverage."""
    run(sys.executable, "-m", "compileall", "-q", "src", "tests", "examples", "scripts")
    run(sys.executable, "-m", "ruff", "check", ".")
    run(
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--cov=pandera_lab",
        "--cov-report=term-missing",
        "--cov-fail-under=90",
    )

    print("\nAll quality gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
