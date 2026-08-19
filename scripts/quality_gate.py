"""Run the local quality gates used by CI.

Usage:
    python scripts/quality_gate.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*command: str) -> None:
    """Run one quality-gate command and stop on failure."""
    print(f"\n$ {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    """Compile, lint, test with coverage, and build the package."""
    run(sys.executable, "-m", "compileall", "-q", "src", "tests", "examples", "scripts")
    run("ruff", "check", ".")
    run(
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--cov=pandera_lab",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-fail-under=90",
    )

    for generated in (ROOT / "build", ROOT / "dist"):
        if generated.exists():
            shutil.rmtree(generated)
    for egg_info in (ROOT / "src").glob("*.egg-info"):
        shutil.rmtree(egg_info)

    run(sys.executable, "-m", "build")
    print("\nAll quality gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
