# Suggested Answers — Phase 6 Interview Questions

1. Unit tests isolate small logic; contract tests enforce schemas; integration tests exercise component boundaries; regression tests preserve previously intended behavior.
2. Direct helper tests isolate the formula from Pandera integration and error-report formatting.
3. Small, deterministic, readable, semantically valid, and easy to modify for one failure at a time.
4. Coverage measures executed code paths; it does not prove that assertions express correct requirements.
5. A test can execute every branch while asserting only that no exception occurred.
6. Later schema evolution should not silently change earlier lessons.
7. A stale “successful” file may be consumed as if it belonged to a failed current batch.
8. After valid input, a bad output indicates code defects and should be visible to engineering, not hidden as bad source data.
9. It catches interpreter-specific compatibility and dependency behavior differences.
10. The lower bound is part of the public compatibility contract.
11. Tests do not guarantee that package metadata or wheel/sdist construction works.
12. Static checks catch issues such as undefined names and suspicious syntax before runtime tests reach them.
13. It discourages untested code but can incentivize meaningless tests or become brittle if set without understanding exclusions.
14. Use fixed inputs, fixed seeds where randomness is required, and no network/time dependencies.
15. Lint, focused tests, full regression/integration tests, coverage gate, package build, and review of contract/documentation changes.
