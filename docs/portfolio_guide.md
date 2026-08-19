# Portfolio Guide

This repository is strongest when presented as a **data-contract and reliability project**, not merely “I learned a Python library.”

## 30-second project explanation

> I built a staged data-quality pipeline around unreliable e-commerce CSV data. Pandera schemas enforce structure, coercion, nullability, uniqueness, categorical and cross-column business rules. Invalid source batches produce structured reports, while internal transformations use typed input/output dataframe contracts. I added regression/integration tests, coverage and lint gates, package-build checks, and a Python-version CI matrix.

## Resume bullet examples

Adapt these to your real usage; do not invent production scale or performance numbers.

- Built a schema-driven Python data-quality pipeline with Pandera and pandas, validating raw CSV inputs, business invariants, and typed transformation outputs.
- Implemented structured lazy-validation reporting, stale-artifact safety, and explicit separation between source-data failures and transformation defects.
- Added unit, contract, regression, and end-to-end tests plus automated lint, coverage, package-build, and multi-version GitHub Actions gates.
- Created a seven-phase educational repository with Jupyter notebooks, challenges, interview questions, and reusable documentation.

## What to show in an interview

Open these files in order:

1. `README.md` — problem and architecture
2. `src/pandera_lab/schemas/orders.py` — source contract
3. `src/pandera_lab/business_rules.py` — domain logic
4. `src/pandera_lab/transformations.py` — typed transformation
5. `src/pandera_lab/pipeline.py` — operational semantics
6. `tests/test_phase6_reliability.py` — reliability thinking
7. `.github/workflows/ci.yml` — automation

## Strong discussion topics

- why coercion is not cleaning,
- why `strict="filter"` is appropriate at one boundary and `strict=True` at another,
- why financial comparisons use tolerance,
- how cascading validation errors are prevented,
- why output-schema failure is a code defect,
- why old educational schemas are frozen,
- why coverage is not correctness.

## Avoid weak claims

Do not claim:

- “production ready” without deployment/operations evidence,
- a coverage percentage until CI has measured it,
- performance at millions of rows without benchmarks,
- zero bugs.

A strong portfolio explanation distinguishes **implemented guarantees** from **future production concerns**.

## Natural next extensions

If you later want to expand the project:

- add customer/product relational integrity checks,
- persist data-quality metrics over time,
- add observability/alerting,
- benchmark validation on large datasets,
- explore Pandera Polars/PySpark backends,
- add row quarantine rather than batch-only rejection.
