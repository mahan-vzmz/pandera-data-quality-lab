# Pandera Data Quality Lab

A seven-phase, problem-driven repository for learning **Pandera**, **pandas**, executable **data contracts**, and production-style **data quality engineering**.

The project starts with an unreliable e-commerce CSV and progressively builds a trustworthy path from raw source data to validated analytics output, then hardens that path with tests and CI.

## What this repository demonstrates

- class-based Pandera schemas with explicit dtype/value contracts
- controlled coercion, null policy, uniqueness, and categorical domains
- lazy validation with structured `failure_cases`
- custom column and cross-column business rules
- floating-point-safe monetary validation
- typed dataframe function boundaries with `DataFrame[Schema]`
- runtime input/output validation with `@pa.check_types`
- explicit source-data failure vs programming-defect semantics
- unit, contract, regression, and end-to-end pipeline tests
- coverage, lint, package-build, and multi-version CI gates
- notebooks, challenges, interview questions, and solutions for every stage

## Problem

An analytics team receives `orders.csv` from an upstream system. The file may contain:

```text
wrong dtypes
missing values
duplicate order IDs
invalid categories
invalid dates
unexpected metadata
wrong monetary totals
```

Downstream analytics should never blindly trust this source.

## Final architecture

```mermaid
flowchart TD
    A[Untrusted orders.csv] --> B[load_orders_csv]
    B --> C[validate_orders / OrderSchema]
    C -->|invalid| D[failure_cases]
    D --> E[Detailed + summary reports]
    C -->|valid| F[Trusted OrderSchema DataFrame]
    F --> G[@pa.check_types]
    G --> H[enrich_orders]
    H --> I[EnrichedOrderSchema output validation]
    I --> J[Trusted enriched CSV]
```

Detailed architecture: `docs/07_architecture.md`.

## The key design decision

The system distinguishes two categories of failure:

```text
bad source data
    -> expected operational outcome
    -> structured validation reports
    -> no trusted output

bad transformation output after trusted input
    -> programming defect
    -> exception propagates
    -> do not disguise it as source-data failure
```

## Core source contract

```python
class OrderSchema(pa.DataFrameModel):
    order_id: Series[int] = pa.Field(unique=True, nullable=False, coerce=True)
    customer_id: Series[str] = pa.Field(nullable=False)
    product_id: Series[str] = pa.Field(nullable=False)
    quantity: Series[int] = pa.Field(gt=0, nullable=False, coerce=True)
    unit_price: Series[float] = pa.Field(gt=0, nullable=False, coerce=True)
    discount: Series[float] = pa.Field(ge=0, le=1, nullable=False, coerce=True)
    total: Series[float] = pa.Field(nullable=False, coerce=True)
    status: Series[str] = pa.Field(isin=ALLOWED_ORDER_STATUSES, nullable=False)
    order_date: Series[DateTime] = pa.Field(nullable=False, coerce=True)
```

The full class also contains custom non-blank identifier checks and a dataframe-level total formula check.

## Typed transformation

```python
@pa.check_types(lazy=True)
def enrich_orders(
    df: DataFrame[OrderSchema],
) -> DataFrame[EnrichedOrderSchema]:
    ...
```

Output fields:

```text
gross_amount     = unit_price * quantity
discount_amount  = gross_amount * discount
net_amount       = total
order_month      = YYYY-MM(order_date)
is_discounted    = discount > 0
```

The output schema validates the **meaning**, not only the dtype, of each derived field.

## Repository structure

```text
pandera-data-quality-lab/
├── .github/
│   ├── workflows/ci.yml
│   └── dependabot.yml
├── data/
│   ├── raw/
│   ├── reference/
│   └── clean/
├── notebooks/              # 7 progressive notebooks
├── docs/                   # lessons + architecture + cheat sheet
├── challenges/             # problem-driven exercises
├── interview/              # phase-specific + master interview bank
├── solutions/              # reference answers
├── examples/
├── scripts/
│   └── quality_gate.py
├── src/pandera_lab/
│   ├── business_rules.py
│   ├── ingestion.py
│   ├── validation.py
│   ├── reporting.py
│   ├── transformations.py
│   ├── pipeline.py
│   └── schemas/
└── tests/
```

## Install

The final release pins Pandera for reproducible learning behavior:

```text
pandera[pandas]==0.32.1
```

Development setup:

```bash
python -m pip install -e ".[dev]"
```

Or:

```bash
python -m pip install -r requirements.txt
```

## Run the project

Run the end-to-end example:

```bash
python examples/phase5_run_pipeline.py
```

Run tests:

```bash
python -m pytest -q
```

Run all local quality gates:

```bash
python scripts/quality_gate.py
```

Run notebooks:

```bash
jupyter lab
```

## CI quality gates

GitHub Actions is configured to test Python:

```text
3.10
3.12
3.14
```

The repository gates changes on:

```text
Python compilation
Ruff lint
pytest regression suite
90% coverage threshold
package build
```

CI configuration: `.github/workflows/ci.yml`.

## Seven-phase learning path

| Phase | Problem | Main concepts |
|---|---|---|
| 1 | Why can’t we trust the CSV? | data contracts, inspection |
| 2 | How do we encode the first contract? | `DataFrameModel`, `Field` |
| 3 | What about messy real input? | coercion, nulls, lazy errors |
| 4 | What if columns are individually valid but logically inconsistent? | custom/cross-column checks |
| 5 | How do contracts protect transformations? | `DataFrame[Schema]`, `check_types` |
| 6 | How do we prevent regressions? | test architecture, coverage, CI |
| 7 | Can we explain and extend the system? | architecture, capstone, portfolio |

Start at `START_HERE.md`.

## Educational stability

The current production-facing schema evolves, while earlier notebooks use frozen historical contracts:

```text
Phase2OrderSchema
Phase3OrderSchema
Phase4OrderSchema
```

This keeps old lessons reproducible instead of silently changing their expected behavior.

## Portfolio use

Read `docs/portfolio_guide.md` for:

- a 30-second explanation,
- resume bullet templates,
- files to show in an interview,
- strong technical discussion topics,
- claims you should **not** make without evidence.

## Quick reference

`docs/cheat_sheet.md` contains the complete syntax/decision cheat sheet.

## Final capstone

After completing the seven phases, design a second data entity in:

```text
challenges/07_capstone.md
```

The goal is to prove the design skill transfers beyond the original `orders.csv` example.

## Release

Project version: **1.0.0**

See:

- `CHANGELOG.md`
- `RELEASE_CHECKLIST.md`
- `CONTRIBUTING.md`

## Scope and limitations

This repository demonstrates data-contract design and engineering discipline on small synthetic datasets. It does **not** claim production-scale throughput, deployment reliability, benchmark results, or zero defects. Those require separate operational evidence.
