# Pandera Data Quality Lab

A problem-driven repository for learning **Pandera**, **Pandas**, and practical **data quality engineering** through a realistic e-commerce validation problem.

It is designed to work simultaneously as:

1. a hands-on learning path,
2. a real-world mini data-quality project,
3. a portfolio-ready GitHub repository.

## Scenario

An analytics team receives daily order CSV files from an upstream system.

The files are not fully trustworthy. They may contain:

- strings where numbers are expected,
- unconvertible values,
- nulls,
- duplicate IDs,
- invalid categories,
- invalid dates,
- extra source metadata,
- broken business rules.

The project builds an explicit boundary between:

```text
raw source data
      |
      v
validation + coercion
      |
      +---- invalid -> structured error reports
      |
      v
trusted analytical dataframe
```

## Current status — Phase 3 complete ✅

### Phase 1 — Contract discovery

- inspected messy data
- classified data-quality problems
- defined the order data contract

### Phase 2 — First executable schema

- `DataFrameModel`
- typed `Series`
- `Field`
- uniqueness
- ranges
- categorical domains
- schema tests

### Phase 3 — Real input validation

- controlled per-field coercion
- explicit `nullable=False`
- datetime coercion
- lazy error aggregation
- `failure_cases`
- `ValidationResult`
- detailed CSV error reports
- aggregated error summaries
- extra-column filtering with `strict="filter"`
- reusable ingestion, validation, and reporting modules
- Phase-3 notebook, challenges, interview questions, and tests

## Repository structure

```text
pandera-data-quality-lab/
├── data/
│   ├── raw/
│   ├── reference/
│   └── clean/
├── notebooks/
│   ├── 01_why_data_validation.ipynb
│   ├── 02_build_first_schema.ipynb
│   └── 03_real_input_validation.ipynb
├── docs/
│   ├── 00_roadmap.md
│   ├── 01_order_data_contract.md
│   ├── 02_first_schema.md
│   └── 03_real_input_validation.md
├── challenges/
├── interview/
├── solutions/
├── examples/
├── src/pandera_lab/
│   ├── ingestion.py
│   ├── validation.py
│   ├── reporting.py
│   └── schemas/
├── tests/
└── reports/
```

## Phase-3 contract

```python
class OrderSchema(pa.DataFrameModel):
    order_id: Series[int] = pa.Field(
        unique=True,
        nullable=False,
        coerce=True,
    )

    customer_id: Series[str] = pa.Field(nullable=False)
    product_id: Series[str] = pa.Field(nullable=False)

    quantity: Series[int] = pa.Field(
        gt=0,
        nullable=False,
        coerce=True,
    )

    unit_price: Series[float] = pa.Field(
        gt=0,
        nullable=False,
        coerce=True,
    )

    discount: Series[float] = pa.Field(
        ge=0,
        le=1,
        nullable=False,
        coerce=True,
    )

    total: Series[float] = pa.Field(
        nullable=False,
        coerce=True,
    )

    status: Series[str] = pa.Field(
        isin=ALLOWED_ORDER_STATUSES,
        nullable=False,
    )

    order_date: Series[DateTime] = pa.Field(
        nullable=False,
        coerce=True,
    )

    class Config:
        strict = "filter"
```

## Validation API

```python
from pandera_lab import load_orders_csv, validate_orders

df = load_orders_csv("data/raw/orders.csv")
result = validate_orders(df)

if result.is_valid:
    trusted_df = result.data
else:
    print(result.failure_cases)
```

## Generate an error report

```bash
python examples/phase3_validate_raw.py
```

This writes:

```text
reports/phase3_validation_errors.csv
reports/phase3_validation_summary.csv
```

when the input is invalid.

## Setup

Pandera is pinned to `0.32.1` for reproducibility.

```bash
python -m pip install -r requirements.txt
```

Run notebooks:

```bash
jupyter lab
```

Run tests:

```bash
pytest
```

## Recommended learning order

1. `notebooks/01_why_data_validation.ipynb`
2. `docs/01_order_data_contract.md`
3. `docs/02_first_schema.md`
4. `notebooks/02_build_first_schema.ipynb`
5. `docs/03_real_input_validation.md`
6. `notebooks/03_real_input_validation.ipynb`
7. `challenges/03_messy_input_and_error_reports.md`
8. `interview/03_real_input_validation.md`
9. run `pytest`

## Deliberate remaining gap

Phase 3 still does **not** enforce:

```text
total == unit_price * quantity * (1 - discount)
```

That relationship depends on multiple columns and becomes the core Phase-4 dataframe-level business rule.
