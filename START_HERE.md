# Start Here

## ⚡ Quick setup

```bash
python -m pip install -e ".[dev]"
```

## 🎯 Fast path — see the final project

1. Read `README.md`
2. Read `docs/07_architecture.md`
3. Run `notebooks/07_capstone_audit.ipynb`
4. Run `python scripts/quality_gate.py`

## 📚 Full learning path

Work through the notebooks in `notebooks/` in order:

| # | Notebook | Lesson |
|---|---|---|
| 01 | why data validation | data contracts, inspection |
| 02 | first schema | `DataFrameModel`, `Field` |
| 03 | messy input + errors | coercion, nulls, lazy validation |
| 04 | business rules | custom/cross-column checks |
| 05 | typed pipeline | `DataFrame[Schema]`, `check_types` |
| 06 | testing + CI | test architecture, coverage |
| 07 | capstone audit | architecture review |

Detailed lessons are in `docs/`.

## 🏋️ Practice path

Each phase has exercises and interview questions:

```text
challenges/   ← try these first
interview/    ← test your knowledge
solutions/    ← check your answers
```

## ✅ Quality gate

```bash
python scripts/quality_gate.py
```
