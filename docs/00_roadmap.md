# Learning Roadmap

This repository grows in phases. Each phase introduces a real data problem first and Pandera syntax second.

## Phase 1 — Understand the contract

- Inspect messy order data.
- Separate structural rules from business rules.
- Understand why pandas dtypes alone are insufficient.

## Phase 2 — Build the first schema

- `DataFrameModel`
- `Series[...]`
- `Field`
- `unique`
- numeric constraints
- allowed categories

## Phase 3 — Handle real input problems

- coercion
- nullable values
- date parsing
- lazy validation
- `failure_cases`

## Phase 4 — Business rules

- custom column checks
- `@pa.check`
- `@pa.dataframe_check`
- cross-column total validation

## Phase 5 — Build the pipeline

- ingestion
- validation boundary
- transformation
- error reporting
- clean output
- `@pa.check_types`

## Phase 6 — Test it

- valid cases
- invalid cases
- edge cases
- regression tests

## Phase 7 — Portfolio polish

- architecture diagram
- completed notebooks
- challenge solutions
- interview answers
- GitHub Actions
- final README
