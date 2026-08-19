# Phase 5 Reference Notes

## Typed transformation

```python
@pa.check_types(lazy=True)
def enrich_orders(
    df: DataFrame[OrderSchema],
) -> DataFrame[EnrichedOrderSchema]:
    gross_amount = expected_gross_amount(df)
    discount_amount = expected_discount_amount(df)

    return df.assign(
        gross_amount=gross_amount.astype(float),
        discount_amount=discount_amount.astype(float),
        net_amount=df["total"].astype(float),
        order_month=df["order_date"].dt.strftime("%Y-%m"),
        is_discounted=df["discount"].gt(0),
    )
```

## Why the output schema is strict

The source boundary uses:

```python
strict = "filter"
```

because harmless source metadata can be tolerated and removed.

The enriched internal output uses:

```python
strict = True
```

because an unexpected field now represents an undocumented transformation output or data leak.

## Source failure vs transform failure

### Source failure

Expected operational problem:

```text
invalid input
-> validation report
-> no trusted output
```

### Transform failure

Developer defect:

```text
valid input
-> transformation produces invalid output
-> @check_types raises
-> fail loudly
```

The latter should not be mislabeled as bad upstream data.

## Why output checks are semantic

The following output is structurally valid:

```text
net_amount = 999.0
```

because it is a float.

But the business meaning is invalid when:

```text
net_amount != total
```

Therefore `EnrichedOrderSchema` uses dataframe-level checks for derived values.

## Pipeline stale-state rule

A pipeline run represents current batch state.

If today's batch fails, yesterday's successful output must not remain at the same current-output path.

If today's batch succeeds, yesterday's failure reports for that batch name must not remain and look current.

This is why Phase 5 removes stale artifacts in both directions.

## Challenge D example

A scratch extension could be:

```python
class ExtendedSchema(EnrichedOrderSchema):
    large_order: Series[bool]

    @pa.dataframe_check(name="large_order_matches_revenue")
    def large_order_is_correct(cls, df):
        return df["large_order"] == df["net_amount"].ge(100)
```

and a decorated transformation would assign:

```python
large_order=df["net_amount"].ge(100)
```

## Performance note

Repeated validation buys stronger runtime contracts, especially with mutable pandas dataframes.

For very large workloads, optimize only after measurement. Possible strategies include:

- validate once at a strong external boundary and keep smaller internal guards,
- validate critical invariants fully while sampling low-risk checks,
- move to partitioned/distributed validation,
- separate inexpensive structural checks from expensive statistical checks,
- record validation depth as an explicit architecture decision.

Do not silently remove correctness guarantees without measuring cost and documenting risk.
