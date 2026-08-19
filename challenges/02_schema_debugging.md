# Challenge 02 — Debug the First Schema

Use `OrderSchema` from Phase 2.

Do not use `coerce=True`, `lazy=True`, or dataframe-level checks yet.

## Challenge A — Predict before running

For each case, predict **PASS** or **FAIL** and explain why.

1. `quantity = -2`
2. `discount = 1.0`
3. `discount = 1.01`
4. `status = "PAID"`
5. duplicate `order_id`
6. wrong `total` but correct dtype
7. an extra column named `source_system`
8. `order_date` stored as `"2026-08-01"` strings

Then verify each prediction with code.

## Challenge B — Boundary values

Create tests for:

```text
quantity = 1
unit_price = 0.01
discount = 0
discount = 1
```

Which boundaries are included and why?

## Challenge C — Explain the architecture

Write a short answer:

> Why should date parsing and coercion be handled as a separate design concern from the Phase-2 business checks?

## Challenge D — Find the deliberate gaps

Find at least three business/data-quality problems in `data/raw/orders.csv` that the Phase-2 model is **not yet designed to solve cleanly**.

For each gap, assign it to a future phase.
