# Pandera / Data Quality Interview Questions — Foundations

Try answering these without looking anything up first.

## Conceptual

1. What problem does Pandera solve that pandas alone does not solve automatically?
2. What is a data contract?
3. What is the difference between dtype validation and value validation?
4. What is the difference between validation and coercion?
5. What is the difference between `required` and `nullable`?
6. What does lazy validation change?
7. Why can a column have the correct dtype and still contain invalid business data?

## Design

8. When would you use `strict=True` instead of `strict="filter"`?
9. Should every incoming string representation of a number be coerced automatically? What are the risks?
10. Where should validation happen in a multi-stage data pipeline?

## Scenario

11. An upstream team adds a new column without notifying you. Should your pipeline fail, ignore it, or remove it?
12. A `total` value differs from `price * quantity` by `0.0000001`. Is exact equality a good rule?
13. A 10-million-row dataset has expensive custom checks. How would you reason about validation cost and placement?
14. Your pipeline accepts valid input but produces an invalid output. How could Pandera help detect that bug?
15. When is rejecting bad data safer than automatically cleaning it?
