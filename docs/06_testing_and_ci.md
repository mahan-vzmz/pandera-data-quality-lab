# Phase 6 — Testing, Reliability, and CI

A data contract is useful only if changes to the code cannot silently weaken it.

## 1. What should be tested?

This project now separates tests by responsibility:

```text
pure domain helpers
    -> focused unit tests

Pandera schemas
    -> contract tests

validation/reporting
    -> component tests

typed transformation
    -> input/output contract tests

full CSV pipeline
    -> integration tests

frozen Phase 2/3/4 schemas
    -> educational regression tests
```

### Why this matters

A single end-to-end test can tell you that something broke, but often not **where**. Focused tests reduce diagnosis time.

## 2. Fixtures are test contracts too

`tests/conftest.py` centralizes canonical examples:

- `valid_typed_orders`
- `valid_raw_orders`
- `valid_enriched_orders`

Fixtures should be small, readable, deterministic, and valid for a clear reason.

A fixture is not a dumping ground for huge production samples.

## 3. Unit tests for business rules

Functions in `business_rules.py` are mostly pure calculations. They are ideal for isolated tests.

Important cases include:

- normal expected totals,
- floating-point tolerance boundaries,
- blank identifiers,
- impossible/unparseable prerequisites,
- derived analytics semantics.

Testing these functions directly means a Pandera error message change does not hide a bug in the domain formula.

## 4. Regression tests

The repository intentionally keeps:

```text
Phase2OrderSchema
Phase3OrderSchema
Phase4OrderSchema
```

because learning material is cumulative.

A regression test proves that later production changes do not rewrite history:

- Phase 2 permits extra columns and does not validate the total formula.
- Phase 3 filters extra columns but still does not validate the total formula.
- Phase 4 validates the total formula.

## 5. Integration tests

The pipeline test boundary is:

```text
CSV -> validation -> transformation -> output/report artifacts
```

Integration tests verify operational behavior that unit tests cannot:

- invalid data must remove stale trusted output,
- a later successful run must remove stale failure reports,
- written output must match direct transformation semantics,
- programming defects must propagate rather than become data-quality reports.

## 6. Coverage is a guardrail, not proof

The final release uses a 90% line/branch-aware coverage gate.

Coverage can answer:

> Did tests execute this code?

It cannot answer:

> Did tests verify the correct business requirement?

A high-coverage bad test suite is still a bad test suite. Boundary cases and semantic assertions matter more than chasing 100%.

## 7. Linting

Ruff is configured for high-signal correctness rules:

```text
E4 / E7 / E9
F
```

The project deliberately avoids enabling a huge style rule set merely to create noise in an educational repository.

## 8. Quality gates in CI

A robust CI workflow runs multiple checks on every push and PR:

- **Compilation**: `python -m compileall` verifies syntax across the entire codebase.
- **Linting**: `ruff check .` catches errors and style defects early.
- **Testing & Coverage**: `pytest` executes tests and enforces the 90% coverage threshold.

## 9. CI matrix

The workflow tests supported Python versions:

```text
3.10
3.12
```

This samples the lower supported boundary and modern stable CPython generations for the pinned Pandera release.

The workflow uses current major GitHub actions:

```yaml
actions/checkout@v4
actions/setup-python@v5
```

## 10. Local and CI parity

Run locally:

```bash
python scripts/quality_gate.py
```

The closer local checks are to CI checks, the fewer “works on my machine” surprises appear.

## Interview-level takeaway

A reliable data-quality system needs **tests for the validator itself**, not only validators for the data.
