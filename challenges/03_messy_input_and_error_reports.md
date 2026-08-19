# Challenge 03 — Messy Input and Error Triage

> **Historical reproducibility:** In Phase 4+ the main `OrderSchema` is stricter. The repository keeps `Phase2OrderSchema` and `Phase3OrderSchema` so the earlier learning behavior can still be reproduced exactly.
Use the Phase-3 project code.

## A. Predict coercion behavior

Predict PASS or FAIL before executing.

1. `quantity = "4"`
2. `quantity = "4.0"`
3. `quantity = "four"`
4. `unit_price = "25.50"`
5. `discount = "0.2"`
6. `order_date = "2026-08-20"`
7. `order_date = "2026-02-30"`

Explain which failures are **conversion failures** and which are **value-rule failures**.

## B. Null policy

Create a valid raw dataframe and independently set each field to `None`.

Record which field fails and how it appears in `failure_cases`.

Then answer:

> Should every column in every real dataset be `nullable=False`?

Explain why the correct answer depends on the business contract.

## C. Lazy validation

Create one dataframe containing at least five independent failures:

- duplicate `order_id`
- `quantity = 0`
- negative `unit_price`
- `discount > 1`
- unsupported `status`

Run the Phase-3 validation helper.

Confirm that multiple columns appear in:

```python
result.failure_cases
```

## D. Error report

Write:

```text
reports/challenge03_errors.csv
reports/challenge03_summary.csv
```

Then answer:

1. Which column has the most failures?
2. Which failures are schema/type-related?
3. Which failures are data/business-rule-related?

## E. Extra-column policy

Add:

```text
source_file
debug_flag
internal_note
```

to otherwise valid data.

Validate it and inspect the returned dataframe.

Explain why Phase 3 uses:

```python
strict = "filter"
```

instead of `True` or `False`.

## F. Architecture question

The ingestion function currently does only:

```python
pd.read_csv(...)
```

Propose one situation where complex preprocessing **should** happen before Pandera validation instead of relying on `coerce=True`.
