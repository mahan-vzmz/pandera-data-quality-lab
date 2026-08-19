# Phase 4 — Custom and Cross-Column Business Rules

Phase 3 made the input boundary robust:

- coercion,
- null handling,
- date parsing,
- lazy validation,
- structured error reports,
- extra-column filtering.

But one deliberately wrong row could still pass:

```text
unit_price = 75
quantity   = 2
discount   = 0.10
total      = 100
```

The expected value is:

```text
75 * 2 * (1 - 0.10) = 135
```

Every individual column can have the correct dtype and valid range while the **relationship between columns is wrong**.

That is the central Phase-4 problem.

## 1. Two kinds of custom rule

Pandera's class-based API supports custom checks as methods on `DataFrameModel`.

### Column-level

```python
@pa.check("customer_id")
def customer_id_not_blank(cls, customer_id):
    ...
```

The function receives one Series.

Use it when the rule only needs one field.

### DataFrame-level

```python
@pa.dataframe_check
def total_matches_business_formula(cls, df):
    ...
```

The function receives the whole DataFrame.

Use it when the rule needs multiple columns.

Pandera's official DataFrameModel documentation describes both decorators and notes that these methods are treated as class methods.

## 2. Why add a custom `@pa.check` when `Field` already has many checks?

Built-in constraints should remain the default when they express the rule clearly:

```python
pa.Field(gt=0)
pa.Field(isin=[...])
```

Custom checks are useful when the rule is domain-specific.

Phase 4 adds:

```text
customer_id must not be empty/whitespace-only
product_id must not be empty/whitespace-only
```

A non-null string such as:

```text
"   "
```

is technically not `None`, but it is not a meaningful identifier.

The model uses:

```python
@pa.check(
    "customer_id",
    name="customer_id_not_blank",
    error="customer_id must contain non-whitespace characters",
)
```

The `name` makes structured reports easier to query. The custom `error` makes failures more understandable to humans.

## 3. The cross-column total rule

The contractual formula is:

```text
total = unit_price * quantity * (1 - discount)
```

That cannot be validated from `total` alone.

The model therefore uses:

```python
@pa.dataframe_check(
    name="total_matches_formula",
    error="...",
)
def total_matches_business_formula(cls, df):
    return total_matches_formula(df)
```

The decorator converts the method into a DataFrame-level Pandera check.

## 4. Why not exact `==` for money represented as floats?

Binary floating point cannot exactly represent every decimal value.

For example:

```python
0.1 * 3
```

is commonly represented internally as something near:

```text
0.30000000000000004
```

So this can be fragile:

```python
df["total"] == expected
```

Phase 4 uses:

```python
np.isclose(...)
```

with:

```text
rtol = 0
atol = 0.005
```

The absolute tolerance is half a cent.

This design:

- tolerates ordinary floating-point representation noise,
- does not accept a full one-cent discrepancy.

### Production note

For financial systems, fixed-point integer cents or decimal arithmetic may be more appropriate than binary floats. This repository keeps floats because the original dataset contract is float-based and the goal is to teach Pandera validation design.

## 5. Avoid cascading failures

Consider this raw value:

```text
quantity = "two"
```

Phase 3 already knows this cannot be coerced to an integer.

A naive total check might then try:

```text
unit_price * "two"
```

or produce an additional misleading:

```text
total formula failed
```

That gives two errors for one root cause.

The project avoids this.

`total_matches_formula()` converts the prerequisites using:

```python
pd.to_numeric(..., errors="coerce")
```

and builds a mask of rows whose formula inputs are comparable.

If a prerequisite is unparseable, the dataframe-level total check returns `True` for that row and lets the **column-level validation** own the failure.

Conceptually:

```text
quantity = "two"
      |
      +--> quantity coercion error  ✅ useful
      |
      +--> total formula error      ❌ skipped as cascading noise
```

This is an important data-quality engineering pattern.

## 6. Business rules live in a helper module

Phase 4 adds:

```text
src/pandera_lab/business_rules.py
```

with:

```python
expected_order_total(...)
total_matches_formula(...)
non_blank_text(...)
```

Why?

Because formula logic should be:

- independently testable,
- reusable outside the schema,
- easy to explain,
- separate from declarative schema structure.

The schema should connect rules to fields/dataframes, not become the only place where business calculations exist.

## 7. Structured error reporting still works

The Phase-3 validation boundary remains:

```python
result = validate_orders(df)
```

If the total rule fails, the `failure_cases` table now includes a check named:

```text
total_matches_formula
```

The existing reporting code can aggregate this with all other validation failures.

That is a major benefit of integrating business rules into Pandera instead of scattering manual `if` statements across the pipeline.

## 8. Phase-4 model excerpt

```python
class OrderSchema(pa.DataFrameModel):
    ...

    @pa.check(
        "customer_id",
        name="customer_id_not_blank",
        error="customer_id must contain non-whitespace characters",
    )
    def customer_id_not_blank(cls, customer_id):
        return non_blank_text(customer_id)

    @pa.check(
        "product_id",
        name="product_id_not_blank",
        error="product_id must contain non-whitespace characters",
    )
    def product_id_not_blank(cls, product_id):
        return non_blank_text(product_id)

    @pa.dataframe_check(
        name="total_matches_formula",
        error=(
            "total must equal unit_price * quantity * "
            "(1 - discount) within the configured currency tolerance"
        ),
    )
    def total_matches_business_formula(cls, df):
        return total_matches_formula(df)
```

## 9. The raw dataset now reveals a new failure

Row `1006` in the deliberately messy CSV contains:

```text
unit_price = 75
quantity = 2
discount = 0.10
total = 100
```

Phase 3 could not reject it because every individual value was type-compatible.

Phase 4 rejects it using `total_matches_formula`.

## 10. Decision guide

```text
Can Field(...) express the rule clearly?
        |
       yes
        |
        v
Use built-in Field/Check
        |
       no
        v
Does the rule need one column?
        |
     yes|no
        |
        +--> @pa.check
        |
        +--> @pa.dataframe_check
```

## Phase-4 checkpoint

You should now be able to explain:

1. built-in Check vs custom Check,
2. `@pa.check`,
3. `@pa.dataframe_check`,
4. why cross-column rules need the DataFrame,
5. why exact float equality can be dangerous,
6. how tolerance should reflect business meaning,
7. why cascading validation failures should be avoided,
8. why business calculations can live outside the schema,
9. how custom check names improve `failure_cases`.
