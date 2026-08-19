# Phase 4 Reference Notes

## 1. Custom column check

A field can be non-null but still meaningless:

```text
customer_id = "   "
```

So Phase 4 adds:

```python
@pa.check(
    "customer_id",
    name="customer_id_not_blank",
    error="customer_id must contain non-whitespace characters",
)
def customer_id_not_blank(cls, customer_id):
    return non_blank_text(customer_id)
```

## 2. Cross-column total check

The contractual formula is:

```text
total = unit_price * quantity * (1 - discount)
```

The DataFrameModel connects it using:

```python
@pa.dataframe_check(
    name="total_matches_formula",
    error="...",
)
def total_matches_business_formula(cls, df):
    return total_matches_formula(df)
```

## 3. Floating-point tolerance

The helper uses:

```python
np.isclose(
    actual,
    expected,
    rtol=0.0,
    atol=0.005,
)
```

The half-cent absolute tolerance is intentionally tied to currency meaning.

A one-cent discrepancy should fail.

## 4. Cascading failures

The total helper first converts its prerequisites with:

```python
pd.to_numeric(..., errors="coerce")
```

Rows with unparseable inputs are not evaluated for the total formula.

This keeps the report focused on the root failure.

## 5. Reusable formula

```python
expected_order_total(df)
```

is outside the schema so it can be:

- unit-tested,
- reused in transformations,
- reused in diagnostics,
- changed in one place when the contract evolves.

## 6. Key architectural principle

The schema owns:

```text
WHEN the rule must be enforced
```

The business-rules module owns:

```text
HOW the business calculation works
```

That separation keeps the DataFrameModel declarative and easier to maintain.
