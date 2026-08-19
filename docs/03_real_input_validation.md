# Phase 3 — Real Input Validation

> **Historical reproducibility:** In Phase 4+ the main `OrderSchema` is stricter. The repository keeps `Phase2OrderSchema` and `Phase3OrderSchema` so the earlier learning behavior can still be reproduced exactly.
Phase 2 defined the contract for already-typed data.

Phase 3 solves a harder problem:

> Real CSV input does not arrive as a perfect analytical dataframe.

A raw file can contain:

- numeric values encoded as text,
- malformed numeric text such as `"two"`,
- missing required values,
- invalid calendar dates,
- extra source-only columns,
- several independent failures at the same time.

## Phase-3 architecture

```text
raw orders.csv
      |
      v
pd.read_csv
      |
      v
raw dataframe
      |
      v
OrderSchema.validate(..., lazy=True)
      |
      +-------------------------+
      |                         |
      v                         v
valid                       invalid
      |                         |
coerced + filtered          failure_cases
      |                         |
      v                         v
analytical dataframe        CSV error report
```

## 1. Coercion is not cleaning

Phase 3 uses `coerce=True` only where type conversion is intentional.

```python
quantity: Series[int] = pa.Field(
    gt=0,
    nullable=False,
    coerce=True,
)
```

This means:

```text
"2"   -> 2      valid conversion
"10"  -> 10     valid conversion
"two" -> error  not convertible
```

Coercion does **not** mean "repair arbitrary bad data".

It means:

> Try to convert the value into the contract's dtype. If conversion is impossible, report a validation failure.

Pandera supports coercion at the field/column and schema levels. In this project we intentionally use **per-field coercion** so the contract clearly states which columns are allowed to change type.

## 2. Why not global `Config.coerce = True`?

A global coercion setting is convenient, but it also applies the conversion policy broadly.

For this learning project, numeric/date fields are explicitly coercible:

```python
order_id
quantity
unit_price
discount
total
order_date
```

Text identifiers such as:

```text
customer_id
product_id
status
```

are not automatically coerced.

This makes missing or malformed identifiers easier to reason about and keeps the input boundary explicit.

## 3. Explicit null policy

Pandera columns are non-nullable by default, but Phase 3 writes the rule explicitly:

```python
customer_id: Series[str] = pa.Field(nullable=False)
```

The reason is pedagogical and architectural: a future reader should not need to remember a library default to understand the business contract.

For the order dataset, all analytical fields are required to contain values.

Examples:

```text
customer_id = null   -> invalid
quantity    = null   -> invalid
order_date  = null   -> invalid
```

## 4. Date parsing through schema coercion

The raw CSV stores dates as text:

```text
2026-08-01
```

but the analytical contract expects a datetime:

```python
order_date: Series[DateTime] = pa.Field(
    nullable=False,
    coerce=True,
)
```

A valid date can be converted.

An impossible date such as:

```text
2026-02-30
```

cannot be converted and becomes a validation failure.

### Why let Pandera parse it?

This is a design choice for the lab.

It keeps the conversion rule and the expected dtype at the same validation boundary and makes conversion failures visible in Pandera's error report.

In other systems, a dedicated ingestion/parser layer may normalize complex date formats before validation. The important engineering principle is to make the boundary explicit.

## 5. `lazy=True`: collect errors instead of stopping early

Fail-fast validation:

```python
OrderSchema.validate(df)
```

raises as soon as validation fails.

For data-quality work, that can be frustrating:

```text
run 1 -> fix quantity
run 2 -> discover status
run 3 -> discover discount
...
```

Phase 3 uses:

```python
OrderSchema.validate(df, lazy=True)
```

so Pandera aggregates validation failures and raises `SchemaErrors`.

The structured table is available as:

```python
error.failure_cases
```

This is the foundation of the project error-reporting layer.

Official Pandera documentation describes `lazy=True` as the mechanism for aggregating errors into a `SchemaErrors` report.

## 6. `failure_cases` is data

This is an important mindset shift.

A validation error is not only console text.

`failure_cases` is a dataframe-like structure that can be:

- filtered,
- grouped,
- counted,
- saved to CSV,
- shown in a dashboard,
- sent to a monitoring system.

The Phase-3 helper:

```python
result = validate_orders(df)
```

returns:

```python
ValidationResult(
    is_valid=...,
    data=...,
    failure_cases=...,
)
```

If valid:

```text
is_valid = True
data = validated dataframe
failure_cases = empty
```

If invalid:

```text
is_valid = False
data = None
failure_cases = Pandera error table
```

## 7. Extra-column policy: `strict="filter"`

The raw source includes:

```text
internal_note
```

That field is useful to the source system but is not part of our analytical contract.

Three possible policies are:

```text
strict=False
    allow and keep extras

strict=True
    reject extras

strict="filter"
    tolerate extras at input, remove them from validated output
```

Phase 3 chooses:

```python
class Config:
    strict = "filter"
```

because the business requirement is:

> Accept the source file even if it contains `internal_note`, but do not let that source-only column leak into the analytical dataframe.

This is a deliberate contract decision, not a universal rule.

## 8. Detailed and summary error reports

Phase 3 contains:

```python
write_failure_report(...)
write_failure_summary(...)
```

The detailed report preserves Pandera's row/check-level evidence.

The summary groups failures by:

```text
column + check
```

so an engineer can quickly answer questions such as:

```text
Which fields are failing?
Which rule fails most often?
Is the problem a conversion error or a business-rule error?
```

## 9. What Phase 3 still does not solve

The raw dataset contains a deliberately incorrect derived total:

```text
total != unit_price * quantity * (1 - discount)
```

Phase 3 still allows this if `total` has a valid float dtype.

Why?

Because that is a **cross-column business rule**, which is intentionally Phase 4.

The learning boundary remains:

```text
Phase 2 -> typed structural contract
Phase 3 -> messy input + error reporting
Phase 4 -> custom and cross-column business rules
```

## 10. Core Phase-3 model

```python
class OrderSchema(pa.DataFrameModel):
    order_id: Series[int] = pa.Field(
        unique=True,
        nullable=False,
        coerce=True,
    )

    customer_id: Series[str] = pa.Field(nullable=False)
    product_id: Series[str] = pa.Field(nullable=False)

    quantity: Series[int] = pa.Field(
        gt=0,
        nullable=False,
        coerce=True,
    )

    unit_price: Series[float] = pa.Field(
        gt=0,
        nullable=False,
        coerce=True,
    )

    discount: Series[float] = pa.Field(
        ge=0,
        le=1,
        nullable=False,
        coerce=True,
    )

    total: Series[float] = pa.Field(
        nullable=False,
        coerce=True,
    )

    status: Series[str] = pa.Field(
        isin=ALLOWED_ORDER_STATUSES,
        nullable=False,
    )

    order_date: Series[DateTime] = pa.Field(
        nullable=False,
        coerce=True,
    )

    class Config:
        strict = "filter"
```

## Phase-3 checkpoint

You should now be able to explain:

1. validation vs coercion,
2. why `"2"` and `"two"` are different validation cases,
3. why nullability is a business-contract decision,
4. fail-fast vs lazy validation,
5. `SchemaError` vs `SchemaErrors`,
6. what `failure_cases` contains,
7. why validation errors can become a report,
8. how `strict="filter"` differs from `strict=True`,
9. why `total` is still not fully validated.
