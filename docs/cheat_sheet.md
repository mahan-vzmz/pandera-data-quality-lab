# Pandera Cheat Sheet

## Imports

```python
import pandera.pandas as pa
from pandera.typing import DataFrame, Series
```

## Object-based schema

```python
schema = pa.DataFrameSchema({
    "age": pa.Column(int, pa.Check.ge(18)),
})
```

## Class-based schema

```python
class UserSchema(pa.DataFrameModel):
    user_id: Series[int] = pa.Field(unique=True, coerce=True)
    age: Series[int] = pa.Field(ge=18, le=65)
```

## Common `Field` rules

```text
nullable=False
unique=True
coerce=True
gt=0
ge=0
lt=100
le=100
isin=[...]
```

## Validate

```python
UserSchema.validate(df)
```

## Lazy validation

```python
try:
    UserSchema.validate(df, lazy=True)
except pa.errors.SchemaErrors as exc:
    print(exc.failure_cases)
```

## Custom column check

```python
@pa.check("customer_id", name="not_blank")
def not_blank(cls, s: Series[str]) -> Series[bool]:
    return s.str.strip().ne("")
```

## Cross-column check

```python
@pa.dataframe_check(name="valid_total")
def valid_total(cls, df):
    return df["total"] == df["price"] * df["quantity"]
```

## Extra columns

```text
strict=False      keep extras
strict=True       reject extras
strict="filter"  drop extras
```

## Typed function contract

```python
@pa.check_types(lazy=True)
def transform(
    df: DataFrame[InputSchema],
) -> DataFrame[OutputSchema]:
    ...
```

## Mental model

```text
structure -> dtype/coercion -> null/unique -> value rules
-> custom rules -> cross-column rules -> function contracts
-> tests/CI
```

## Design questions before writing a schema

1. What is the trust boundary?
2. Which columns are required?
3. Which conversions are legitimate?
4. Which nulls are meaningful?
5. Which rules are single-column vs cross-column?
6. Should unexpected columns fail, pass, or be filtered?
7. What should happen to an invalid batch?
8. Who consumes the failure report?
