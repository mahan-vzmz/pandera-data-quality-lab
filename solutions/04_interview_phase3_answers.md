# Suggested Answers — Phase 3 Interview Questions

1. Validation asks whether data satisfies a contract; coercion attempts an intentional dtype conversion before/while enforcing that contract.
2. No. Coercion only attempts supported type conversion. Unconvertible or semantically invalid values still fail.
3. `"42"` can normally be coerced to integer `42`.
4. `"forty-two"` cannot be coerced to an integer and should be reported.
5. Per-column coercion makes conversion policy explicit and avoids transforming fields that should remain untouched.
6. It says missing/null values violate the contract for that field.
7. Because whether missing data is acceptable depends on domain meaning, not just storage representation.
8. Define a datetime dtype and either parse in ingestion or enable controlled schema coercion.
9. A format issue is syntactic; an impossible date such as February 30 may look syntactically date-like but is not a real calendar date.
10. Parse before validation when formats are complex, source-specific, locale-dependent, or require normalization rules.
11. Fail-fast stops at the first validation error; lazy validation aggregates multiple failures.
12. `SchemaErrors`.
13. It is structured failure data containing evidence such as failing columns, checks, values, and indices.
14. Structured failures can be aggregated, stored, queried, visualized, and monitored.
15. Store reports over time and group by column/check/source/date to track counts and rates.
16. `False` keeps extras, `True` rejects extras, `"filter"` removes extras from validated output.
17. A security-sensitive API or warehouse table with an exact governed schema.
18. A source feed that may add harmless operational metadata while downstream analytics require a fixed subset.
19. Unexpected or sensitive fields can leak into downstream storage, exports, or analytics.
20. Raw source representation and trusted analytical representation have different responsibilities and failure modes.
21. Because it is a multi-column invariant reserved for the next learning phase.
22. In dataframe-level checks such as `@pa.dataframe_check`.
23. Source/batch id, timestamp, failing column, check, failure value, row/index, counts, severity, and ownership/action metadata.
24. Not always. Some systems reject the batch; others quarantine invalid rows or allow partial processing. The policy depends on business risk and consistency requirements.
