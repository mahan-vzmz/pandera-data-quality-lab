# Order Data Contract

This document defines the business expectations for a valid order record.

The goal is to translate this contract into Pandera code gradually.

## Expected columns

| Column | Expected meaning | Expected type |
|---|---|---|
| `order_id` | Unique order identifier | integer |
| `customer_id` | Customer identifier | string |
| `product_id` | Product identifier | string |
| `quantity` | Number of purchased units | integer |
| `unit_price` | Price per unit before discount | float |
| `discount` | Fractional discount | float |
| `total` | Final order value | float |
| `status` | Current order state | string |
| `order_date` | Order creation date | datetime |

## Column-level business rules

### `order_id`

- required
- integer
- unique

### `customer_id`

- required
- non-null string

### `product_id`

- required
- non-null string

### `quantity`

- integer
- greater than zero

### `unit_price`

- float
- greater than zero

### `discount`

- float
- must satisfy:

```text
0 <= discount <= 1
```

### `status`

Allowed values:

```text
pending
paid
shipped
cancelled
```

### `order_date`

- must be a valid date

## Cross-column business rule

The `total` column must match:

```text
total = unit_price * quantity * (1 - discount)
```

Because floating-point calculations can have tiny precision differences, later we will discuss whether exact equality is always the best validation strategy.

## Extra columns

The raw dataset currently contains an `internal_note` column that is **not part of the analytical contract**.

Do not immediately decide what to do with it.

Think about the trade-off between:

- `strict=True`
- `strict=False`
- `strict="filter"`

We will make that decision explicitly when implementing the schema.
