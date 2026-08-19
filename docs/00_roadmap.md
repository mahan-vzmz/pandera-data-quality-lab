# Learning Roadmap

This repository grows in phases. Each phase introduces a real data problem first and Pandera syntax second.

## ✅ Phase 1 — Understand the contract

- inspect messy order data
- separate structural rules from business rules
- understand why pandas dtypes alone are insufficient

## ✅ Phase 2 — Build the first schema

- `DataFrameModel`
- `Series[...]`
- `Field`
- uniqueness
- numeric constraints
- allowed categories
- first automated schema tests

## ✅ Phase 3 — Handle real input problems

- per-field coercion
- explicit null policy
- datetime coercion
- `lazy=True`
- `SchemaErrors`
- `failure_cases`
- detailed and summarized error reports
- `strict="filter"` for extra source columns
- reusable ingestion/validation/reporting helpers

## ⏭️ Phase 4 — Business rules

- custom column checks
- `@pa.check`
- `@pa.dataframe_check`
- cross-column total validation
- custom error messages

## Phase 5 — Build the pipeline

- validation contracts between functions
- `DataFrame[Schema]`
- `@pa.check_types`
- clean output
- pipeline orchestration

## Phase 6 — Test it

- edge cases
- regression tests
- data-quality integration tests
- CI

## Phase 7 — Portfolio polish

- architecture diagram
- completed notebooks
- challenge solutions
- interview preparation
- GitHub Actions
- final README
