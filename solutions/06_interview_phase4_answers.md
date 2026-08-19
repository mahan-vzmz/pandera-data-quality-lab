# Suggested Answers — Phase 4 Interview Questions

1. Prefer built-in checks when they express the rule directly; they are simpler, standardized, and easier to inspect.
2. A Series representing the targeted column/index.
3. Null means missing; whitespace is present data that may still be semantically invalid.
4. Stable names make structured reports, filtering, testing, and monitoring easier.
5. It gives humans a domain-specific explanation rather than only a generic validator message.
6. When validation depends on multiple columns or whole-dataframe properties.
7. The rule depends simultaneously on `unit_price`, `quantity`, `discount`, and `total`.
8. Typically a boolean Series aligned to rows, or a boolean scalar for whole-dataframe assertions.
9. They are included in the structured failures produced by lazy validation; the exact column field may be dataframe-level rather than a single column.
10. Put calculation/comparison logic in a normal function and test that function with pandas data before testing Pandera integration.
11. Many decimal fractions do not have exact binary floating-point representations.
12. Absolute tolerance limits raw numeric distance; relative tolerance scales acceptable distance with magnitude.
13. Currency discrepancies should not become more permissive simply because an order is expensive.
14. The tolerance should reflect the smallest meaningful currency unit, not an arbitrary technical number.
15. Integer minor units (cents) or decimal/fixed-point types.
16. A secondary error caused by an earlier root failure, which makes diagnostics noisier.
17. Because the formula cannot be meaningfully evaluated and the quantity coercion failure already explains the root cause.
18. At the dataframe-rule layer it means “not evaluated here”; the row is still invalid because a lower-level contract check fails.
19. To keep calculations reusable, independently testable, and separate from schema wiring.
20. Treat rules as versioned code with tests, release notes, and explicit migration/compatibility decisions.
21. Some overlap is useful to protect contracts, but duplicated formulas can drift; centralizing shared logic reduces that risk.
22. Use check names/schema_context/severity metadata or reporting classifications to separate structural/type checks from domain checks.
