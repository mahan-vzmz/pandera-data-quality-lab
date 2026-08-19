# Capstone Reference — Returns Design

A strong design would create a separate `ReturnSchema` rather than extending `OrderSchema`, because a return is a different domain entity.

## Suggested raw boundary

```text
return_id          string/non-blank/unique
order_id           integer or domain identifier, required
returned_quantity  integer > 0, coercible
refund_amount      float >= 0, coercible
reason             finite category domain
return_date        datetime, coercible
strict             "filter"
```

## Cross-dataset integrity

Pandera dataframe-level checks operate naturally within one dataframe. Order existence is a **relational** validation problem. Resolve it at a pipeline/join boundary using the trusted orders dataset, then report missing `order_id` references explicitly.

## Typed output idea

Add:

```text
return_month = YYYY-MM(return_date)
```

and validate the derived field in a separate `EnrichedReturnSchema`.

## Test layers

- helper/unit tests for return formulas/normalization,
- schema tests for fields and categories,
- relational integrity tests against a small order fixture,
- end-to-end CSV pipeline tests,
- stale artifact tests,
- CI regression coverage.
