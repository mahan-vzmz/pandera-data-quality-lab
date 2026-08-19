# Pandera Data Quality Lab

A problem-driven learning repository for **Pandera**, **Pandas**, and practical **data quality engineering**.

The repository is intentionally designed as:

1. a hands-on Pandera learning path,
2. a real-world mini data-quality project,
3. a portfolio-ready GitHub repository.

## Real-world scenario

An e-commerce analytics team receives daily order CSV files. The files are not fully trustworthy: columns may have incorrect types, identifiers may be duplicated, business rules may be violated, and derived values such as `total` may be incorrect.

The project builds a **data quality layer** that validates data before downstream analytics use it.

## Learning philosophy

> Problem → inspect → define a contract → validate → understand failures → improve the pipeline

The goal is not to memorize syntax. The goal is to learn how to design **data contracts**.

## Repository map

```text
pandera-data-quality-lab/
├── data/
│   ├── raw/
│   ├── reference/
│   └── clean/
├── notebooks/
│   ├── 01_why_data_validation.ipynb
│   └── 02_build_first_schema.ipynb
├── docs/
│   ├── 00_roadmap.md
│   ├── 01_order_data_contract.md
│   └── 02_first_schema.md
├── challenges/
├── interview/
├── solutions/
├── examples/
├── src/pandera_lab/
│   └── schemas/
├── tests/
└── reports/
```

## Current status — Phase 2 complete ✅

### Phase 1

- inspected the deliberately messy order dataset
- defined the order data contract
- classified structural and business rules

### Phase 2

- implemented `OrderSchema` with `DataFrameModel`
- added dtype expectations
- added `unique=True` for order IDs
- added numeric range checks
- added allowed order statuses
- added automated pytest coverage
- added an interactive Phase-2 notebook
- added debugging exercises and interview questions

### Intentionally not solved yet

Phase 3 will address:

- raw CSV coercion
- null handling
- invalid date parsing
- lazy validation
- `failure_cases`
- explicit handling of extra columns

Phase 4 will add the cross-column `total` business rule.

## Setup

Create and activate a virtual environment, then:

```bash
python -m pip install -r requirements.txt
```

Run the notebooks:

```bash
jupyter lab
```

Run the test suite:

```bash
pytest
```

Run the small Phase-2 example:

```bash
python examples/phase2_validate_reference.py
```

## Recommended learning order

1. `notebooks/01_why_data_validation.ipynb`
2. `docs/01_order_data_contract.md`
3. `challenges/01_order_schema.md`
4. `docs/02_first_schema.md`
5. `notebooks/02_build_first_schema.ipynb`
6. `challenges/02_schema_debugging.md`
7. `interview/02_schema_design.md`
8. run `pytest`

## Core Phase-2 contract

```python
class OrderSchema(pa.DataFrameModel):
    order_id: Series[int] = pa.Field(unique=True)
    customer_id: Series[str]
    product_id: Series[str]
    quantity: Series[int] = pa.Field(gt=0)
    unit_price: Series[float] = pa.Field(gt=0)
    discount: Series[float] = pa.Field(ge=0, le=1)
    total: Series[float]
    status: Series[str] = pa.Field(isin=ALLOWED_ORDER_STATUSES)
    order_date: Series[DateTime]
```

This is intentionally an **intermediate contract**, not the final production schema.
