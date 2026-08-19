# Interview Questions — Phase 4

## Custom checks

1. When should you use a built-in Pandera check instead of a custom check?
2. What does `@pa.check("column")` receive?
3. Why is a whitespace-only string different from a null value?
4. What benefit does a named custom check provide in error reporting?
5. What does the `error=` argument improve?

## DataFrame-level checks

6. When is `@pa.dataframe_check` required?
7. Why can the `total` formula not be represented as a simple `Field(gt=...)` constraint?
8. What should a dataframe-level check return for row-wise validation?
9. How do dataframe-level failures appear in lazy validation reports?
10. How would you unit-test a cross-column invariant independently of Pandera?

## Floating point and financial validation

11. Why can exact equality be unsafe for float calculations?
12. What is the difference between absolute and relative tolerance?
13. Why does this project use `rtol=0` for the money rule?
14. Why is a half-cent tolerance more meaningful here than an arbitrary tolerance such as `0.1`?
15. What alternative numeric representations are often used in financial systems?

## Error quality and architecture

16. What is a cascading validation failure?
17. Why might you skip a total check when `quantity` is unparseable?
18. Is returning `True` for a skipped prerequisite row dishonest? Explain the validation-layer reasoning.
19. Why extract calculation logic into `business_rules.py`?
20. How would you version business rules when requirements change?
21. Should data validation duplicate transformation logic? What are the trade-offs?
22. How would you distinguish schema failures from business-rule failures in monitoring?
