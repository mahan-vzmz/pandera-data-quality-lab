# Start Here

## Fast path — understand the final project

1. Read `README.md`.
2. Read `docs/07_architecture.md`.
3. Run `notebooks/07_capstone_audit.ipynb`.
4. Run `python scripts/quality_gate.py`.
5. Review `docs/portfolio_guide.md` before presenting the project.

## Full learning path

```text
01 why data validation
02 first schema
03 messy input + errors
04 business rules
05 typed pipeline
06 testing + CI
07 capstone audit
```

Corresponding notebooks are in `notebooks/` and detailed lessons are in `docs/`.

## Practice path

Each phase has:

```text
challenges/
interview/
solutions/
```

Try the challenge and interview questions before opening the reference solutions.

## Setup

```bash
python -m pip install -e ".[dev]"
jupyter lab
```

## Final quality gate

```bash
python scripts/quality_gate.py
```
