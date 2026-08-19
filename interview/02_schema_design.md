# Interview Questions — Phase 2 Schema Design

Try answering aloud before checking any notes.

## Core concepts

1. What is the difference between `DataFrameSchema` and `DataFrameModel`?
2. What does `Series[int]` express?
3. What problem does `pa.Field(gt=0)` solve that `Series[int]` does not?
4. What does `unique=True` validate?
5. Why is `discount` modeled with both `ge=0` and `le=1`?
6. When would `isin(...)` be preferable to a custom lambda check?

## Scenario questions

7. A column contains `-10`, but its dtype is `int64`. Is this a dtype failure? Explain.
8. An order status contains `"refunded"`, which is a valid Python string. Why can a schema still reject it?
9. Why does Phase 2 intentionally allow an incorrect `total` value?
10. Why can validating a raw CSV directly against a strict typed schema produce noisy or misleading failures?
11. What are the trade-offs of allowing extra columns at a data pipeline boundary?
12. If the business adds a new valid status `"returned"`, where should that change be made?

## Design discussion

13. Should allowed statuses live directly inside `Field(isin=...)`, or in a named constant? What are the maintainability implications?
14. Why is it useful to test values exactly on boundaries such as `discount=0` and `discount=1`?
15. How would you explain the phrase **data contract** to a backend engineer who has never used Pandera?
