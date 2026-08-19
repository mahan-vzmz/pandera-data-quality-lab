# Phase 2 — Build the First Order Schema

Phase 1 answered: **what should a valid order look like?**

Phase 2 turns that contract into executable Pandera code.

## Learning goals

By the end of this phase you should be able to explain and use:

- `pa.DataFrameModel`
- `Series[...]`
- `pa.Field`
- `unique=True`
- `gt`, `ge`, `le`
- `isin`
- the difference between a **dtype rule** and a **value rule**
- why some validation concerns are deliberately deferred

## The Phase-2 schema

```python
import pandera.pandas as pa
from pandera.dtypes import DateTime
from pandera.typing import Series


ALLOWED_ORDER_STATUSES = (
    "pending",
    "paid",
    "shipped",
    "cancelled",
)


class OrderSchema(pa.DataFrameModel):
    order_id: Series[int] = pa.Field(unique=True)
    customer_id: Series[str]
    product_id: Series[str]
    quantity: Series[int] = pa.Field(gt=0)
    unit_price: Series[float] = pa.Field(gt=0)
    discount: Series[float] = pa.Field(ge=0, le=1)
    total: Series[float]
    status: Series[str] = pa.Field(
        isin=ALLOWED_ORDER_STATUSES
    )
    order_date: Series[DateTime]

    class Config:
        strict = False
```

## Read the model as a contract

### `order_id`

```python
order_id: Series[int] = pa.Field(unique=True)
```

This combines two different rules:

1. dtype rule: values belong to an integer column
2. uniqueness rule: two rows cannot share an order id

### `quantity`

```python
quantity: Series[int] = pa.Field(gt=0)
```

`int` is the type rule.

`gt=0` is a value rule.

This distinction matters:

- `-3` is a valid integer dtype
- but it violates the business rule

### `discount`

```python
discount: Series[float] = pa.Field(ge=0, le=1)
```

The business contract uses a fraction:

```text
0 <= discount <= 1
```

Therefore:

- `0.00` is valid
- `1.00` is valid
- `-0.01` is invalid
- `1.20` is invalid

### `status`

```python
status: Series[str] = pa.Field(
    isin=("pending", "paid", "shipped", "cancelled")
)
```

This is a categorical domain rule.

A string like `"refunded"` has the correct dtype but violates the allowed domain.

## Why is `total` only a float?

In Phase 2:

```python
total: Series[float]
```

is intentional.

The stronger business rule is:

```text
total = unit_price * quantity * (1 - discount)
```

That rule needs multiple columns at the same time, so it belongs to a dataframe-level check. We postpone it until Phase 4 so the learning stages remain separate.

A deliberately wrong `total` therefore still passes the Phase-2 schema.

That is not a bug in the project. It is a teaching boundary.

## Why does `order_date` expect datetime but not parse strings?

The data contract says that `order_date` is a date, so the schema expresses a datetime dtype:

```python
order_date: Series[DateTime]
```

However, a raw CSV normally provides text.

Converting text such as:

```text
2026-08-01
```

into a datetime is a parsing/coercion problem.

Phase 2 only defines the expected final dtype. Phase 3 will decide how raw CSV input should be converted and how invalid dates such as `2026-02-30` should be reported.

## Why `strict=False` for now?

The raw dataset contains:

```text
internal_note
```

which is not part of the analytical contract.

Phase 2 intentionally keeps:

```python
strict = False
```

so we can focus on the first schema.

Later we will compare:

```text
strict=False
strict=True
strict="filter"
```

and choose the correct behavior at the pipeline boundary.

## Phase-2 boundary

### Implemented now

- expected columns
- expected dtypes
- unique order ids
- quantity > 0
- unit_price > 0
- 0 <= discount <= 1
- allowed order statuses

### Deferred

- raw CSV coercion
- invalid datetime parsing
- explicit null strategy
- lazy validation / `failure_cases`
- extra-column filtering
- cross-column total calculation

This separation is important in real engineering work: solve one validation boundary at a time instead of mixing ingestion, cleaning, data contracts, and business logic into one large schema.
