# Interview Questions — Phase 5 Typed Pipelines

## DataFrame typing

1. What does `DataFrame[OrderSchema]` mean in a Pandera function signature?
2. Does a Python type annotation alone guarantee runtime dataframe validity?
3. What does `@pa.check_types` validate?
4. Can `@pa.check_types` validate a function's return dataframe as well as its inputs?
5. What changes when `lazy=True` is passed to `check_types`?
6. Why might a pipeline deliberately validate the same dataframe at more than one function boundary?

## Input vs output contracts

7. Why should a transformation often have different input and output schemas?
8. Why is checking output dtype/column presence alone sometimes insufficient?
9. Give an example of a semantically wrong output that still has the correct dtype.
10. Why does `EnrichedOrderSchema` validate formulas for derived fields?
11. What is schema inheritance useful for in this project?
12. What risk does schema inheritance introduce if base contracts change unexpectedly?

## Strictness

13. Explain the difference between `strict="filter"` on the source contract and `strict=True` on the enriched output.
14. Why can allowing upstream extra columns be reasonable?
15. Why can allowing internal transformation extra columns be dangerous?

## Pipeline architecture

16. What is the difference between an operational data-quality failure and a programming defect?
17. Why does the pipeline convert source validation errors into reports?
18. Why does the pipeline intentionally not swallow output-schema exceptions?
19. What information is captured by `PipelineResult`?
20. Why should a failed current run remove a stale trusted output?
21. Why should a successful current run remove stale failure reports?
22. What are the risks of partial or ambiguous pipeline artifacts?

## Persistence and trust boundaries

23. Does writing a validated dataframe to CSV permanently preserve its pandas dtypes?
24. When the CSV is loaded again later, where should validation happen?
25. How would Parquet change the dtype-persistence discussion compared with CSV?

## Design and scaling

26. Is double validation always desirable? Discuss correctness vs performance.
27. How would you approach validation for a dataframe with hundreds of millions of rows?
28. When might sampling be acceptable, and what kinds of invariants should never rely only on sampling?
29. How could you expose pipeline/data-quality results to observability systems?
30. How would you test that a transformation's output contract catches a bug rather than merely testing the happy path?

## Advanced decorator behavior

31. Does `@pa.check_types` automatically act as a full runtime type checker for every ordinary Python annotation such as `int`, `str`, and `Path`?
32. What is `with_pydantic=True` for, and why is it not needed for the core Phase-5 dataframe lesson?
