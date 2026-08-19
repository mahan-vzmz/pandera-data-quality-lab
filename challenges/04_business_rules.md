# Challenge 04 — Business Rules

Do not open the Phase-4 solution notes until you have attempted these.

## A. Column-level custom rule

Create a custom check for `customer_id` that rejects:

```text
""
" "
"    "
```

but accepts:

```text
"C001"
"CUSTOMER-9"
```

Explain why `nullable=False` alone is not enough.

## B. Exact equality trap

Run:

```python
0.1 * 3
```

and compare it with:

```python
0.3
```

Then explain why a production business rule should not blindly depend on float `==`.

## C. Cross-column rule

Implement:

```text
total = unit_price * quantity * (1 - discount)
```

as a dataframe-level check.

Test these rows:

1. exact correct total
2. representation noise (`0.30000000000000004`)
3. half-cent-scale noise
4. one-cent wrong total
5. obviously wrong total

## D. Cascading-error design

Create:

```text
quantity = "two"
```

while `total` is otherwise numeric.

Your desired report should contain the quantity conversion failure without a misleading total-formula failure.

Explain how you would guard the dataframe-level rule.

## E. Error messages

Compare a custom check with and without:

```python
name="..."
error="..."
```

Which version produces a more operationally useful `failure_cases` table?

## F. Design question

Suppose tomorrow the company changes its pricing rule to:

```text
total = round(unit_price * quantity * (1 - discount), 2) + shipping_fee
```

Where should the calculation live?

Discuss:

- schema method,
- reusable business-rules module,
- transformation layer,
- tests.
