# Challenge 05 — Typed Pipeline Contracts

Complete these after the Phase-5 notebook.

## A. Read the function contract

Given:

```python
@pa.check_types(lazy=True)
def enrich_orders(
    df: DataFrame[OrderSchema],
) -> DataFrame[EnrichedOrderSchema]:
    ...
```

Explain, in your own words:

1. what the input annotation communicates,
2. what the return annotation communicates,
3. what the decorator adds at runtime,
4. why `lazy=True` changes failure behavior.

## B. Predict the failure boundary

For each scenario, decide whether the failure should be classified as:

```text
source-data failure
transformation/output-contract failure
no failure
```

1. raw CSV contains `status="UNKNOWN"`
2. raw CSV contains a correct order but `internal_note` is present
3. transformation forgets `is_discounted`
4. transformation returns `net_amount=999.0`
5. transformation adds an unexpected `debug_column`
6. valid output CSV is later re-read without parsing `order_date`

Explain each answer.

## C. Break the output deliberately

Create a local decorated function that returns every required enriched field but sets:

```python
gross_amount = 1.0
```

for every row.

Confirm that the output fails because of:

```text
gross_amount_matches_formula
```

not merely because of dtype or missing-column validation.

## D. Add a new output feature

Add a scratch schema and transformation field:

```text
large_order: bool
```

Business rule:

```text
large_order = net_amount >= 100
```

Requirements:

- type must be boolean,
- returned value must match the rule,
- a semantically wrong boolean must be rejected by the output schema.

Do this in a scratch file/notebook first rather than modifying the main project.

## E. Pipeline state correctness

Run a valid batch first so an output file exists.

Then run an invalid batch using the same output path.

Explain why leaving the old output file in place would be dangerous.

Repeat in reverse:

1. invalid run creates reports,
2. valid run follows,
3. verify old reports are removed.

## F. Architecture discussion

Answer:

> If `@pa.check_types` already validates the `OrderSchema` input to `enrich_orders`, why does `run_order_pipeline` call `validate_orders` before it?

Your answer should discuss:

- operational error reports,
- expected vs unexpected failure semantics,
- function boundaries,
- mutable dataframes,
- observability.

## G. Performance trade-off

The current pipeline can validate a dataframe more than once.

Propose when this is acceptable and when you might need a different strategy for very large data.

Do **not** remove validation just for speed; explain what evidence and risk analysis you would need first.
