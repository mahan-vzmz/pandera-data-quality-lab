# Challenge 06 — Reliability and CI

## A. Boundary design

Add one test for each boundary without changing production code:

1. discount exactly `0`
2. discount exactly `1`
3. total error of `0.0049`
4. total error of `0.01`
5. whitespace-only `product_id`

Explain which layer should catch each case.

## B. Regression thinking

Imagine Phase 8 changes `strict="filter"` to `strict=True` on `OrderSchema`.

Which historical notebook would change behavior? Which regression test should protect the old lesson?

## C. Artifact safety

Write an integration test for this sequence:

```text
valid run -> invalid run -> valid run
```

At each point state exactly which files should exist in `clean/` and `reports/`.

## D. Coverage critique

Give an example of a test that increases coverage but provides almost no confidence.

Then rewrite it as a semantic test.

## E. CI review

Read `.github/workflows/ci.yml` and answer:

1. Why is `fail-fast: false` useful in a Python matrix?
2. Why is coverage enforced in a dedicated job rather than every matrix entry?
3. Why is the package build a separate quality gate?
