# Pandera Data Quality Lab

A problem-driven learning repository for **Pandera**, **Pandas**, and practical **data quality engineering**.

The repository is intentionally designed as both:

1. a hands-on Pandera learning path,
2. a real-world mini data-quality project,
3. a portfolio-ready GitHub repository.

## Real-world scenario

An e-commerce analytics team receives daily order data as CSV files. The files are not fully trustworthy: columns may have incorrect types, identifiers may be duplicated, business rules may be violated, and derived values such as `total` may be incorrect.

Your job is to build a **data quality layer** that validates the data before downstream analytics use it.

## Learning philosophy

Each topic follows this loop:

> Problem → inspect the data → define a contract → validate → understand failures → improve the pipeline

The goal is not to memorize Pandera syntax. The goal is to learn how to design **data contracts**.

## Repository map

```text
pandera-data-quality-lab/
├── data/
│   ├── raw/                 # Intentionally messy input data
│   ├── reference/           # Small known-good datasets
│   └── clean/               # Future validated outputs
├── notebooks/               # Interactive lessons
├── docs/                    # Conceptual lesson notes
├── challenges/              # Exercises without solutions
├── interview/               # Interview and scenario questions
├── solutions/               # Added gradually after exercises are solved
├── src/pandera_lab/         # Production-style Python package
│   └── schemas/             # Pandera DataFrameModels
├── tests/                   # pytest tests
└── reports/                 # Validation error reports
```

## Phase 1: foundations

Start here:

1. Read [`START_HERE.md`](START_HERE.md).
2. Open [`notebooks/01_why_data_validation.ipynb`](notebooks/01_why_data_validation.ipynb).
3. Inspect [`data/raw/orders.csv`](data/raw/orders.csv).
4. Read the contract in [`docs/01_order_data_contract.md`](docs/01_order_data_contract.md).
5. Complete [`challenges/01_order_schema.md`](challenges/01_order_schema.md).

Do **not** rush into the solution. First try to identify every problem in the raw dataset yourself.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run JupyterLab:

```bash
jupyter lab
```

Run tests later with:

```bash
pytest
```

## What this repository will eventually demonstrate

- Schema-based dataframe validation
- Dtype validation and coercion
- Nullable / required / unique constraints
- Built-in and custom checks
- Cross-column business rules
- Lazy validation and failure reports
- `DataFrameModel` and `Field`
- `@pa.check` and `@pa.dataframe_check`
- Function input/output contracts with `@pa.check_types`
- Validation pipeline architecture
- Automated tests
- Interview preparation
- Portfolio-quality documentation

## Current status

**Starter phase.** The repository contains the project structure and deliberately dirty order data. The main `OrderSchema` is intentionally unfinished so it can be implemented as the first practical task.
