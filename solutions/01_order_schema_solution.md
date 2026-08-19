# Solution — Challenge 01

This solution is intentionally limited to **Phase 2**.

## Rule classification

| Rule | Classification |
|---|---|
| `order_id` integer | dtype |
| `order_id` unique | uniqueness |
| `customer_id` string | dtype |
| `product_id` string | dtype |
| `quantity > 0` | range/value |
| `unit_price > 0` | range/value |
| `0 <= discount <= 1` | range/value |
| allowed `status` values | category/domain |
| valid `order_date` | dtype + parsing concern |
| `total = ...` | dataframe-level business rule |
| `internal_note` | extra-column policy |

## Phase-2 implementation

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
    status: Series[str] = pa.Field(isin=ALLOWED_ORDER_STATUSES)
    order_date: Series[DateTime]

    class Config:
        strict = False
```

## Design answers

### Why `quantity > 0` instead of `>= 0`?

An order line with zero purchased units is not a valid purchase under this contract.

### Why `ge` + `le` for discount?

The rule is a simple closed numeric interval. Built-in checks communicate intent more clearly than a custom lambda.

### What happens to `internal_note` in Phase 2?

It is temporarily accepted because `strict=False`.

This is not the final pipeline decision.

### Why no coercion yet?

Phase 2 defines what valid typed data looks like. Phase 3 will design how raw CSV values become those types.

### What about `"two"` in `quantity`?

It violates the expected integer dtype. Phase 3 will make the coercion/error-reporting behavior explicit.

### Why is the `total` equation absent?

It requires a dataframe-level check across multiple columns and is intentionally deferred to Phase 4.
