# Phase 5 — Typed DataFrame Pipelines

The first four phases answered progressively stronger questions:

```text
Phase 1: What is wrong with the data?
Phase 2: What does a valid dataframe look like?
Phase 3: How do we handle messy raw input and report failures?
Phase 4: How do we enforce custom and cross-column business rules?
```

Phase 5 asks:

> How do we make those contracts part of the function boundaries in a real pipeline?

---

## 1. The problem with manual validation everywhere

You can always write:

```python
validated = OrderSchema.validate(df)
result = transform(validated)
EnrichedOrderSchema.validate(result)
```

This works, but every function author must remember both checks.

In a larger pipeline, that creates several risks:

- one function forgets input validation,
- another validates input but not output,
- a mutable dataframe changes between checks,
- function signatures do not communicate their dataframe contract.

Pandera provides a typed runtime boundary for this pattern.

---

## 2. `DataFrame[Schema]` communicates the contract

Phase 5 uses:

```python
from pandera.typing import DataFrame


def enrich_orders(
    df: DataFrame[OrderSchema],
) -> DataFrame[EnrichedOrderSchema]:
    ...
```

Read the signature as:

```text
input:
    dataframe satisfying OrderSchema

output:
    dataframe satisfying EnrichedOrderSchema
```

The annotation documents intent for humans and type-aware tooling.

However, a type annotation by itself is not the main runtime guard in this pattern.

For runtime validation we add:

```python
@pa.check_types(lazy=True)
```

---

## 3. `@pa.check_types` validates both directions

The real transformation is:

```python
@pa.check_types(lazy=True)
def enrich_orders(
    df: DataFrame[OrderSchema],
) -> DataFrame[EnrichedOrderSchema]:
    ...
```

Conceptually:

```text
caller dataframe
      |
      v
validate as OrderSchema
      |
      v
function body
      |
      v
returned dataframe
      |
      v
validate as EnrichedOrderSchema
      |
      v
caller receives trusted result
```

This is stronger than checking only the input.

A function can receive valid data and still contain a bug.

Example:

```python
net_amount = 999.0
```

The dtype is valid, but the output business contract is wrong.

The output schema catches it before the result crosses the function boundary.

---

## 4. Why `lazy=True` on the decorator?

Phase 5 uses:

```python
@pa.check_types(lazy=True)
```

This keeps the same diagnostic philosophy introduced in Phase 3: when the annotated dataframe violates several checks, Pandera can aggregate failures into `SchemaErrors` rather than stopping at the first one.

For batch source validation, we convert those structured failures into operational reports.

For internal transformation contracts, we normally let the exception propagate because it indicates a developer-facing defect.

---

## 5. Input schema vs output schema

### `OrderSchema`

This is the trusted order contract built through Phase 4.

It validates:

- typed/coercible fields,
- null policy,
- unique order IDs,
- allowed ranges,
- status domain,
- non-blank identifiers,
- correct order total.

Its source-boundary policy is:

```python
strict = "filter"
```

That is appropriate for an upstream feed where source-only metadata may be tolerated but not propagated.

### `EnrichedOrderSchema`

Phase 5 introduces a new output contract:

```text
gross_amount
discount_amount
net_amount
order_month
is_discounted
```

The output schema uses:

```python
strict = True
```

Why the difference?

At the internal transformation boundary, an unexpected output column is no longer harmless upstream metadata. It is a code-level contract change or leak.

So:

```text
source boundary:
strict="filter"

trusted internal output:
strict=True
```

This is a useful example of choosing strictness based on boundary semantics rather than using one setting everywhere.

---

## 6. The output contract is semantic, not only structural

A weak output schema could say only:

```text
gross_amount is float
discount_amount is float
net_amount is float
order_month is string
is_discounted is bool
```

That would still allow:

```text
net_amount = 999999.0
```

Phase 5 deliberately makes the output contract stronger.

### Gross amount

```text
gross_amount = unit_price * quantity
```

### Discount amount

```text
discount_amount = gross_amount * discount
```

### Net revenue

```text
net_amount = total
```

### Order month

```text
order_month = YYYY-MM(order_date)
```

### Discount flag

```text
is_discounted = discount > 0
```

These rules use dataframe-level checks in `EnrichedOrderSchema`.

So the output validator catches both:

```text
wrong shape
and
wrong meaning
```

---

## 7. Reusing domain formulas

Phase 5 does not duplicate calculations in the transformation and schema.

The formulas live in:

```text
src/pandera_lab/business_rules.py
```

For example:

```python
expected_gross_amount(df)
expected_discount_amount(df)
```

The transformation uses those helpers to create columns.

The output schema uses related helpers to validate the result.

This keeps domain logic centralized and testable.

---

## 8. The typed transformation

The implementation is intentionally small:

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

Notice the design choice:

```python
df.assign(...)
```

rather than adding columns directly to the caller's dataframe.

This reduces surprising mutation at the transformation boundary.

---

## 9. Does `@check_types` replace the Phase-3 validation layer?

No.

This distinction is one of the most important lessons in Phase 5.

### Operational batch validation

```python
result = validate_orders(raw_df)
```

is designed to:

- handle untrusted source data,
- collect failures,
- produce `failure_cases`,
- write detailed and summary reports,
- support batch-level operational decisions.

### Typed transformation validation

```python
@pa.check_types
```

is designed to protect internal function contracts.

They overlap in schema validation, but their responsibilities are different.

The project intentionally performs validation again at decorated function boundaries. DataFrames are mutable, and a function boundary should not have to trust that an object stayed valid merely because it passed a check earlier.

---

## 10. End-to-end orchestration

The Phase-5 pipeline is:

```python
run_order_pipeline(
    input_path,
    output_path,
    report_dir,
)
```

Flow:

```text
1. read raw CSV
2. validate raw batch lazily
3. if invalid:
       remove stale trusted output
       write detailed report
       write summary report
       return failed PipelineResult
4. if valid:
       remove stale failure reports
       call typed enrich_orders
       validate output automatically
       write trusted CSV
       return successful PipelineResult
```

---

## 11. Why stale artifact cleanup matters

Imagine yesterday's run was valid:

```text
data/clean/orders_enriched.csv
```

Today the source batch is invalid.

If the pipeline leaves yesterday's file in place, another system or a human could mistakenly treat it as today's successful output.

Phase 5 removes stale trusted output when the current batch fails.

The reverse is also true:

- yesterday failed and produced reports,
- today succeeds,
- old failure reports should not look like current failures.

So a successful run removes stale reports for that input batch name.

This is not Pandera syntax. It is pipeline correctness.

---

## 12. Expected data failure vs programming defect

This is another important boundary.

### Expected source-data failure

```text
status = UNKNOWN
quantity = 0
wrong total
invalid date
```

Pipeline behavior:

```text
no trusted output
+ detailed report
+ summary report
```

### Programming / transformation defect

Suppose the source data is valid but the code returns:

```text
net_amount = 999999
```

`EnrichedOrderSchema` rejects it.

The pipeline intentionally does **not** catch that as if the source file were bad.

Why?

Because the upstream data already passed its contract. The failure was introduced by our code.

The correct response is loud failure, debugging, and fixing the transformation.

---

## 13. Persistence is another boundary

The pipeline writes the validated enriched dataframe to CSV.

Remember that CSV does not preserve pandas dtype metadata.

For example, after re-reading:

```python
pd.read_csv("orders_enriched.csv")
```

`order_date` may again be a string-like column until parsing/validation happens.

A persisted CSV being produced from a validated dataframe does not mean every future re-read is automatically typed.

Data contracts should be enforced at the boundary where data is trusted again.

---

## 14. The complete Phase-5 mental model

```text
UNTRUSTED WORLD
raw CSV
   |
   v
batch validation/reporting
   |
   | invalid ----------------> operational reports
   |
   v
TRUSTED INTERNAL WORLD
OrderSchema dataframe
   |
   v
@check_types input guard
   |
   v
enrich_orders
   |
   v
@check_types output guard
   |
   v
EnrichedOrderSchema dataframe
   |
   v
trusted persisted output
```

---

## Phase-5 checkpoint

You should now be able to explain:

1. what `DataFrame[Schema]` communicates,
2. why `@pa.check_types` is needed for runtime function-boundary validation,
3. how input and output schemas differ,
4. why output validation catches transformation bugs,
5. why `strict="filter"` and `strict=True` can both be correct at different boundaries,
6. why batch validation/reporting still exists even with decorated functions,
7. why a source-data failure and a transformation defect should not be handled identically,
8. what `PipelineResult` communicates,
9. why stale output/report cleanup is part of correctness,
10. why persistence creates another future validation boundary.

## Next phase

Phase 6 focuses on reliability engineering:

- broader edge cases,
- integration/regression fixtures,
- test organization,
- GitHub Actions,
- automated CI verification.

---

## Advanced note — `check_types` is not a general-purpose Python type checker

Pandera's `@pa.check_types` focuses on Pandera-aware dataframe annotations.

If a decorated function also has ordinary parameters such as:

```python
def transform(df: DataFrame[OrderSchema], threshold: int):
    ...
```

you should not assume that Pandera will enforce the ordinary `int` annotation in the same way it enforces the dataframe schema. Pandera provides a `with_pydantic=True` option when Pydantic-backed validation of ordinary annotated inputs is desired.

In this repository, Phase 5 deliberately keeps the focus on dataframe contracts and does not add Pydantic as another concept/dependency.
