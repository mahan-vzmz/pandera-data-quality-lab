# Interview Questions — Phase 3

## Coercion and typing

1. What is the difference between validation and coercion?
2. Does `coerce=True` mean Pandera cleans arbitrary bad data?
3. What should happen when an integer field receives `"42"`?
4. What should happen when the same field receives `"forty-two"`?
5. Why might a team prefer per-column coercion over schema-wide coercion?

## Nulls and parsing

6. What does `nullable=False` express?
7. Why is nullability a business-rule decision rather than merely a technical dtype concern?
8. How would you validate a raw CSV date column?
9. What is the difference between an invalid date format and an impossible calendar date?
10. When would you parse dates before Pandera instead of using Pandera coercion?

## Error handling

11. What is the difference between fail-fast validation and `lazy=True`?
12. What exception does lazy Pandera validation aggregate errors into?
13. What is `failure_cases`, and why is it useful in production?
14. Why is saving validation failures as structured data better than logging only an exception string?
15. How could a team monitor data quality trends using `failure_cases`?

## Extra columns

16. Compare `strict=False`, `strict=True`, and `strict="filter"`.
17. Give a scenario where `strict=True` is the safest choice.
18. Give a scenario where `strict="filter"` is better.
19. What risk exists when `strict=False` allows unexpected columns downstream?

## Architecture

20. Why does this project separate raw ingestion from the validated analytical dataframe?
21. Why does Phase 3 still not validate the `total` formula?
22. Where should cross-column business rules live?
23. What information would you include in a production data-quality report?
24. Should an invalid batch always stop a pipeline? Discuss strict rejection, quarantine, and partial-processing strategies.
