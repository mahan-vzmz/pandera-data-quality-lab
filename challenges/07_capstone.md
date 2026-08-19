# Challenge 07 — Final Capstone

You are taking ownership of a new `returns.csv` source.

Design the extension without copying the order schema blindly.

## Requirements

The source contains:

```text
return_id
order_id
returned_quantity
refund_amount
reason
return_date
```

Business rules:

- `return_id` is unique and non-blank.
- `order_id` is required.
- `returned_quantity > 0`.
- `refund_amount >= 0`.
- `reason` is one of `damaged`, `wrong_item`, `changed_mind`, `other`.
- `return_date` is a datetime.
- unexpected operational columns should be filtered.

## Your tasks

1. Define the raw trust boundary.
2. Decide which fields should use coercion.
3. Define null policy.
4. Add at least one custom check.
5. Design how relational integrity against orders would be checked.
6. Define a typed analytics output schema with one derived field.
7. Write unit, contract, and integration test cases.
8. Explain source failure vs programmer defect behavior.
9. Add a CI-safe test dataset.
10. Present the design in five interview-style minutes.

Do not add the feature to the final repository before you can explain each decision.
