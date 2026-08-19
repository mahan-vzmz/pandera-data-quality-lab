# Phase 4 Completion Notes

Phase 4 adds the project's first domain-specific cross-column invariant.

## Added
- `src/pandera_lab/business_rules.py`
- custom non-blank identifier checks
- `total_matches_formula` dataframe-level check
- half-cent float tolerance
- cascading-error guard
- Phase-4 notebook
- Phase-4 tests
- challenge, interview questions, and solutions
- Phase-4 example script

## Changed
- wrong totals now fail validation
- data contract now explicitly rejects blank identifiers
- project version is `0.4.0`

## Deliberately deferred
- `DataFrame[Schema]`
- `@pa.check_types`
- input/output transformation contracts
- end-to-end pipeline orchestration

Those are Phase 5.
