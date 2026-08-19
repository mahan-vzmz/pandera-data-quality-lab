# Phase 3 Reference Notes

Use this after completing the Phase-3 challenge.

## Key distinctions

### `"4"` vs `"four"`

```text
"4"
 -> coercible to integer
 -> type conversion succeeds
 -> normal value checks continue

"four"
 -> cannot be converted to integer
 -> coercion/type failure
```

### Coercion vs business rules

```text
quantity = "-2"
```

can be converted to an integer, so coercion succeeds.

But:

```text
quantity > 0
```

fails.

This is a value/business-rule failure, not a conversion failure.

## Nullability

`nullable=False` means missing values are not valid under the contract.

It should not be copied blindly to every dataset. For example, optional middle names or nullable cancellation dates may legitimately permit missing values.

## Lazy validation

The project uses:

```python
OrderSchema.validate(df, lazy=True)
```

because batch data-quality work benefits from seeing many independent failures in one run.

The resulting:

```python
SchemaErrors
```

contains structured:

```python
failure_cases
```

that can be inspected and exported.

## Extra columns

Phase 3 chooses:

```python
strict = "filter"
```

because source-only metadata is tolerated at ingestion but must not become part of the analytical contract.

### Alternatives

```text
strict=False
```

keeps unexpected columns.

```text
strict=True
```

rejects the entire dataframe when an unexpected column appears.

Neither is universally correct; the boundary requirement determines the policy.

## Preprocessing before Pandera

Pre-validation preprocessing may be preferable when:

- dates arrive in several locale-specific formats,
- decimal separators vary by source,
- nested JSON must be normalized,
- encrypted or encoded fields need decoding,
- source-specific sentinel values such as `"N/A*"`, `"-9999"`, or `"UNKNOWN_DATE"` require controlled normalization.

The important rule is to keep preprocessing explicit and tested instead of hiding arbitrary cleaning inside validation logic.

## Phase 4 reminder

The following is still missing intentionally:

```text
total == unit_price * quantity * (1 - discount)
```

It needs a dataframe-level business rule.
