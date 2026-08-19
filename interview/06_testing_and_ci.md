# Interview Questions — Testing and CI

1. What is the difference between unit, contract, integration, and regression tests in a data pipeline?
2. Why should business-rule helpers be tested outside Pandera schemas too?
3. What makes a good dataframe fixture?
4. What does code coverage measure, and what does it fail to measure?
5. Why can 100% coverage still hide a broken business rule?
6. Why test historical schemas in an educational repository?
7. What operational bug can stale output files cause?
8. Why should a transformation bug propagate instead of becoming a source-data report?
9. What does a Python CI matrix protect against?
10. Why test the minimum supported Python version?
11. Why run a package build in CI?
12. Why run a linter if tests already pass?
13. What are the trade-offs of a strict 90% coverage threshold?
14. How would you design a flaky-data test so it remains deterministic?
15. What checks would you require before merging a change to a data contract?
