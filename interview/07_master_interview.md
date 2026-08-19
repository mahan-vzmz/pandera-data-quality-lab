# Master Interview — Pandera and Data Quality

## Fundamentals

1. What problem does Pandera solve that pandas alone does not?
2. Explain a data contract.
3. `DataFrameSchema` vs `DataFrameModel`?
4. dtype validation vs value validation?
5. validation vs cleaning vs coercion?
6. `nullable` vs `required`?
7. `unique=True` vs a custom uniqueness business rule?

## Rules

8. Built-in Check vs custom `@pa.check`?
9. When do you need `@pa.dataframe_check`?
10. Why should financial equality avoid raw floating-point `==`?
11. How do you prevent cascading validation errors?
12. How would you validate relationships across two different dataframes?

## Input quality

13. What does `lazy=True` change?
14. `SchemaError` vs `SchemaErrors`?
15. Why is `failure_cases` operationally useful?
16. Compare `strict=False`, `True`, and `"filter"`.
17. When is schema-wide coercion risky?

## Pipeline architecture

18. What does `DataFrame[Schema]` communicate?
19. What does `@pa.check_types` enforce at runtime?
20. Why use separate input and output schemas?
21. Why should source-data errors and transformation bugs have different failure handling?
22. Why remove stale output after a failed batch?
23. What is the trust level of data at each pipeline stage?

## Testing and delivery

24. How do you test a schema?
25. How do you test a cross-column formula independently of Pandera?
26. Unit vs contract vs integration vs regression tests?
27. Why is coverage not correctness?
28. What belongs in a CI quality gate?
29. Why test multiple Python versions?
30. How do you keep an educational repository stable while the production schema evolves?

## Design scenarios

31. The upstream team adds 20 unexpected columns. What policy do you choose and why?
32. A batch is 99.9% valid. Do you reject it, quarantine rows, or partially process it?
33. A date source uses three locale formats. Where do you normalize it?
34. Your validator becomes slow on 100M rows. What do you measure before optimizing?
35. A new business status appears unexpectedly. Is that bad data or schema drift?
36. How would you add data-quality trend monitoring?
37. What changes if the dataframe backend moves from pandas to Polars or Spark?
38. What guarantees does this repository provide, and what does it deliberately not claim?
