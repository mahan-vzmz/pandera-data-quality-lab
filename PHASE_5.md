# Phase 5 — Typed Pipeline Integration

Phase 5 connects Pandera schemas directly to transformation function signatures and builds the first end-to-end pipeline.

## Added in this phase

- `EnrichedOrderSchema` as a strict output contract
- `DataFrame[OrderSchema]` input annotations
- `DataFrame[EnrichedOrderSchema]` return annotations
- `@pa.check_types(lazy=True)` runtime input/output validation
- semantic output checks for every derived analytics column
- `enrich_orders` typed transformation
- `PipelineResult`
- `run_order_pipeline`
- valid-batch persistence
- invalid-batch validation reports
- stale artifact cleanup
- Phase-4 historical schema freeze
- Phase-5 tests, lesson, notebook, challenges, interview prep, and solutions
- project version `0.5.0`

## Phase-5 architecture

```text
CSV
 |
 v
load_orders_csv
 |
 v
validate_orders
 |---------------- invalid ----------------> failure reports
 |
 valid
 v
trusted OrderSchema dataframe
 |
 v
@pa.check_types
 |
 v
enrich_orders
 |
 v
EnrichedOrderSchema output validation
 |
 v
trusted enriched CSV
```

## Important distinction

The batch validation layer and the typed transformation layer solve different problems.

### Source-data failure

Examples:

- bad status
- duplicate order id
- invalid date
- wrong total

These are expected operational data-quality problems. The pipeline writes structured reports and produces no trusted output.

### Transformation contract failure

Example:

- `enrich_orders` returns a wrong `net_amount`
- a required derived column is missing
- an unexpected debug column leaks into output

These indicate a programming defect. The pipeline intentionally does not convert them into an ordinary source-data report.

## Deliberately deferred to Phase 6

- broader reliability/edge-case suite
- regression fixture organization
- CI / GitHub Actions
- coverage automation
- release-quality test matrix
