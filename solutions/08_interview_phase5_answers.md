# Suggested Answers — Phase 5 Interview Questions

1. It annotates a dataframe expected to satisfy `OrderSchema`.
2. No. Runtime validation in this pattern is provided by Pandera's decorator or explicit schema validation.
3. Annotated Pandera dataframe inputs and outputs.
4. Yes; the return annotation can be validated before the result reaches the caller.
5. Validation aggregates multiple failures and raises a lazy error report rather than stopping at the first failure.
6. Dataframes are mutable and each boundary should defend its own contract; earlier validation does not prove the object stayed valid forever.
7. Transformations usually add, remove, or change fields, so postconditions differ from preconditions.
8. A correctly typed value can still violate business meaning.
9. `net_amount=999.0` is a float but can disagree with `total`.
10. To turn output validation into a semantic postcondition rather than only a shape check.
11. It lets the enriched contract reuse all trusted order fields and rules while adding output-specific fields/checks.
12. A base-schema change propagates to subclasses; historical contracts or independently versioned APIs may need freezing/versioning.
13. `"filter"` tolerates source extras but removes them; `True` rejects any undeclared output column.
14. Upstream systems often attach harmless operational metadata outside the analytical contract.
15. Internal extras may indicate undocumented behavior, sensitive-data leakage, or accidental API expansion.
16. Data-quality failures originate in untrusted source data; programming defects are introduced by our code despite valid input.
17. Reports are operational artifacts that can be triaged, monitored, and sent to data owners.
18. Hiding a transformation bug as a source-data problem would misdiagnose ownership and allow code defects to masquerade as bad feeds.
19. Success state, input/output paths, report paths, and row counts.
20. Otherwise consumers may mistake an old successful artifact for the current failed batch.
21. Otherwise consumers/operators may mistake old errors for a current successful batch.
22. Ambiguous artifacts can cause stale-data consumption, false alarms, inconsistent downstream state, and hard-to-debug incidents.
23. No. CSV is text-oriented and does not persist pandas dtype metadata in the same way an in-memory dataframe has it.
24. At the next trust boundary after loading/parsing it.
25. Parquet preserves richer typed column metadata, reducing some parsing ambiguity, but business/schema validation is still necessary.
26. No. It trades compute for stronger boundary guarantees. Measure cost and risk before changing validation depth.
27. Use partitioning/distributed execution, staged checks, efficient invariants, monitoring, and architecture appropriate to the scale.
28. Sampling may suit exploratory/expensive statistical checks; uniqueness, referential constraints, financial totals, and critical row-level invariants often require full coverage.
29. Emit counts/rates by schema/check/source/batch, publish reports/metrics, and connect them to logs, dashboards, alerts, or lineage systems.
30. Create deliberately broken output implementations/fixtures and assert the output schema fails for the intended semantic check.
31. No. Its core job is Pandera-aware validation of supported typed dataframe/series annotations; ordinary built-in annotations should not be assumed to receive equivalent enforcement by default.
32. `with_pydantic=True` enables Pydantic-backed validation for ordinary annotated inputs while Pandera still handles dataframe contracts. Phase 5 avoids it so the lesson stays focused on dataframe input/output contracts rather than introducing a second validation framework.
