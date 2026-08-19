# Master Interview — Reference Answers

These are concise anchors, not memorization scripts.

1. Pandas manipulates data; Pandera expresses and enforces executable assumptions about dataframe structure and values.
2. A data contract is an explicit agreement describing what data must look like before downstream code trusts it.
3. `DataFrameSchema` is object-based; `DataFrameModel` is class/type-annotation based.
4. Dtype asks what representation a column has; a value rule asks whether values are allowed by the domain.
5. Validation checks; coercion performs intentional type conversion; cleaning changes data according to repair/normalization policy.
6. `required` concerns column presence; `nullable` concerns missing values inside a present column.
7. `unique=True` is a direct column invariant; complex uniqueness may require combinations of columns or domain context.
8. Use built-ins when they express the rule declaratively; custom checks for domain-specific logic.
9. When a rule needs multiple columns at once.
10. Binary floats cannot represent many decimals exactly; use domain-appropriate tolerance or decimal arithmetic.
11. Let prerequisite dtype/null errors be authoritative and skip derivative checks when inputs are not comparable.
12. Validate each dataframe first, then validate relationships at a pipeline/join boundary.
13. It aggregates multiple errors instead of stopping at the first.
14. Singular fail-fast exception vs aggregated lazy-validation exception.
15. It converts failures into structured data that can be grouped, stored, monitored, or reported.
16. Keep extras, reject extras, or filter extras respectively.
17. It may silently convert fields that should remain strict identifiers or categories.
18. It documents a dataframe’s schema type at a function boundary.
19. It validates annotated dataframe inputs and outputs at runtime.
20. Transformation output can have stronger/different guarantees than input.
21. Bad source data is expected operations; bad output after valid input means code violated its postcondition.
22. Otherwise downstream consumers may mistake old trusted data for the current failed run.
23. Raw input is untrusted; validated `OrderSchema` data is trusted for transformation; enriched validated output is trusted for persistence.
24. Test valid examples, each independent invalid rule, boundaries, coercion, nulls, and interactions.
25. Call the pure formula/helper directly with deterministic data.
26. They differ by scope: isolated logic, contract behavior, component flow, and preservation of previous behavior.
27. Executing a line does not prove the assertion was meaningful.
28. Compilation/static checks, tests, coverage guardrail, packaging/build checks, and supported-version compatibility.
29. Dependencies and language behavior can differ between the lower bound and newer interpreters.
30. Freeze historical schemas/notebook semantics and evolve the current schema separately.
31. Choose based on boundary ownership: exact governed interfaces may reject; tolerant source feeds may filter.
32. It is a business-risk policy. Financial/transactional pipelines often prefer quarantine/rejection over silent partial processing.
33. In an explicit ingestion/normalization layer when formats are complex or source-specific.
34. Measure validation stages, row counts, checks, memory, I/O, and actual bottlenecks before changing semantics.
35. Potential schema drift; confirm whether business requirements changed before classifying it as bad data.
36. Persist summarized failure metrics by source/check/time and alert on rate changes.
37. Contract concepts remain, but dtype semantics, execution model, and backend-specific APIs/performance change.
38. It demonstrates schema contracts, reporting, typed transformations, tests, and CI design; it does not claim production scale, benchmarks, or zero defects.
