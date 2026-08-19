# Start Here

Follow the repository in phase order.

## Phase 1 — Understand the problem

1. `notebooks/01_why_data_validation.ipynb`
2. `docs/01_order_data_contract.md`
3. `challenges/01_order_schema.md`

## Phase 2 — Build the first executable contract

1. `docs/02_first_schema.md`
2. `notebooks/02_build_first_schema.ipynb`
3. `challenges/02_schema_debugging.md`
4. `interview/02_schema_design.md`

## Phase 3 — Validate real messy input

1. Read `docs/03_real_input_validation.md`.
2. Inspect the evolved `src/pandera_lab/schemas/orders.py`.
3. Run `notebooks/03_real_input_validation.ipynb`.
4. Run the example:

```bash
python examples/phase3_validate_raw.py
```

5. Inspect generated files in `reports/`.
6. Solve `challenges/03_messy_input_and_error_reports.md`.
7. Answer `interview/03_real_input_validation.md`.
8. Run:

```bash
pytest
```

## Phase-3 learning boundary

Phase 3 intentionally does **not** add the cross-column `total` rule yet.

A numeric but incorrect total can still pass:

```text
total != unit_price * quantity * (1 - discount)
```

That is the central problem for Phase 4.
