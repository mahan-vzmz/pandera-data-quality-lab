# Learning Roadmap — Complete

## ✅ Phase 1 — Understand the contract
- messy-data inspection
- structural vs business rules
- explicit data-contract thinking

## ✅ Phase 2 — Build the first schema
- `DataFrameModel`, `Series`, `Field`
- dtype, uniqueness, ranges, categories

## ✅ Phase 3 — Handle real input
- coercion and null policy
- datetime conversion
- lazy validation and `failure_cases`
- error reporting
- extra-column filtering

## ✅ Phase 4 — Business rules
- `@pa.check`
- `@pa.dataframe_check`
- cross-column totals
- tolerance and cascading-error prevention

## ✅ Phase 5 — Typed pipeline
- `DataFrame[Schema]`
- `@pa.check_types`
- separate input/output contracts
- trusted output and orchestration

## ✅ Phase 6 — Reliability and CI
- shared fixtures
- unit/contract/integration/regression tests
- 90% coverage gate
- Ruff
- package build gate
- GitHub Actions matrix

## ✅ Phase 7 — Portfolio and release
- final architecture
- cheat sheet
- capstone
- master interview preparation
- contribution/release docs
- version `1.0.0`

The learning path is complete. Future work should be treated as project extensions rather than hidden “missing phases.”
