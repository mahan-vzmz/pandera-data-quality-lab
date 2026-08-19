# Phase 6 Reference — Reliability Design

## Recommended test layers

```text
business_rules.py        -> unit tests
OrderSchema              -> schema contract tests
validation/reporting     -> component tests
enrich_orders            -> typed transformation tests
run_order_pipeline       -> integration tests
Phase2/3/4 schemas       -> historical regression tests
```

## Boundary expectations

- `discount=0`: valid
- `discount=1`: valid if the computed total is zero
- total difference below half a cent: tolerated
- one-cent difference: invalid
- blank identifier: invalid custom column check

## Artifact lifecycle

```text
valid run
  output exists
  failure reports absent

invalid run
  trusted output absent
  failure reports exist

later valid run
  output exists
  stale failure reports absent
```

## Coverage interpretation

Coverage is useful as a **minimum confidence gate**. It is not a correctness metric. Assertions must encode domain meaning.
