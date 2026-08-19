# Start Here

## If you are new to this repository

Follow the material in order.

### Phase 1 — Understand the problem

1. Open `notebooks/01_why_data_validation.ipynb`.
2. Inspect `data/raw/orders.csv`.
3. Read `docs/01_order_data_contract.md`.
4. Try `challenges/01_order_schema.md`.

### Phase 2 — Build the first executable contract

1. Read `docs/02_first_schema.md`.
2. Open `src/pandera_lab/schemas/orders.py`.
3. Run `notebooks/02_build_first_schema.ipynb`.
4. Solve `challenges/02_schema_debugging.md`.
5. Review `interview/02_schema_design.md`.
6. Run:

```bash
pytest
```

## Important learning boundary

The Phase-2 schema is deliberately incomplete from a production perspective.

Do not "fix" these yet unless you are intentionally moving into Phase 3/4:

- coercion
- invalid raw dates
- structured lazy error reports
- extra-column filtering
- cross-column validation of `total`

These gaps are part of the learning design.
