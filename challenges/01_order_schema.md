# Challenge 01 — Design the Order Schema

Do not look for a finished solution yet.

## Part A — Classify the rules

For every requirement in `docs/01_order_data_contract.md`, classify it as one of:

- dtype rule
- nullability rule
- uniqueness rule
- range rule
- category rule
- dataframe-level business rule

## Part B — Inspect the raw data

Find at least **10 distinct validation problems** in `data/raw/orders.csv`.

For each problem, record:

1. row/index
2. column(s)
3. violated rule
4. expected behavior

## Part C — Implement the first model

Open:

```text
src/pandera_lab/schemas/orders.py
```

Implement the basic `OrderSchema` using only concepts you already know.

Suggested first iteration:

- define the columns
- define dtypes
- define uniqueness
- define numeric ranges
- define allowed `status` values

Do **not** solve date parsing or cross-column `total` validation until the basic schema works.

## Part D — Questions to answer before coding

1. Should `quantity` use `gt=0` or `ge=0`? Why?
2. Should `discount` use one custom check or `ge` + `le`?
3. What should happen to `internal_note`?
4. Should `coerce=True` be applied at the field level or model level?
5. What should happen when one row contains the string `"two"` in `quantity`?
