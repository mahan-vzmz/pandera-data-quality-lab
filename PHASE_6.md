# Phase 6 — Reliability Engineering and CI

Phase 6 changes the question from **“does this example work?”** to **“how do we keep it working as the repository changes?”**

## Delivered

- shared pytest fixtures in `tests/conftest.py`
- focused unit tests for pure business-rule helpers
- integration and regression tests for the typed pipeline
- historical Phase 2/3/4 behavior regression coverage
- 90% coverage gate
- Ruff lint gate
- package-build gate
- local `scripts/quality_gate.py`
- GitHub Actions matrix for Python 3.10, 3.12, and 3.14
- Dependabot configuration for pip and GitHub Actions
- Phase-6 notebook, challenge, interview set, and solutions

## Quality gate

```bash
python scripts/quality_gate.py
```

This runs:

```text
compile -> lint -> tests + coverage -> package build
```

CI uses the same principles on every pull request and push to `main`.
