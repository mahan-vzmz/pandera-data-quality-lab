# Suggested Answers — Phase 2 Interview Questions

These are concise reference answers, not scripts to memorize.

1. `DataFrameSchema` is the object-based API; `DataFrameModel` is the class-based typed API. Both represent executable dataframe contracts.
2. `Series[int]` expresses that the named dataframe column is expected to have an integer-compatible dtype.
3. `gt=0` validates values. An integer such as `-5` has the right dtype but violates the value rule.
4. `unique=True` rejects repeated values in that field.
5. Because the discount is a fraction in a closed interval: both zero discount and a full discount are allowed by the contract.
6. Use `isin` for a finite explicit domain; it is simpler and more declarative than custom code.
7. No. `-10` can have the correct integer dtype. It is a value/business-rule failure when a positive value is required.
8. Dtype validity and domain validity are different. `"refunded"` is a string but may be outside the supported business states.
9. The equation for `total` depends on several columns, so it is intentionally postponed until dataframe-level checks are introduced.
10. CSVs frequently encode numbers/dates as text and may contain malformed values. Without an ingestion strategy, dtype failures can hide the more useful data-quality story.
11. Allowing extras is flexible but may leak unexpected data downstream; strict rejection is safer but more brittle; filtering can enforce an output shape while tolerating upstream additions.
12. Update the shared allowed-status domain in the schema and add regression tests for the new state.
13. A named constant improves reuse, discoverability, and maintenance when the domain is referenced in multiple places.
14. Boundary tests prove whether the contract is inclusive or exclusive and prevent subtle range mistakes.
15. A data contract is an executable agreement describing the structure, types, allowed values, and business invariants that data must satisfy before downstream code trusts it.
