# Start Here

## Mission

You are working as a junior data engineer on an e-commerce analytics pipeline.

Every day a file named `orders.csv` arrives from an upstream system. The analytics team discovered that bad data sometimes reaches reports, so your task is to introduce a reliable validation layer.

For now, **do not clean the data manually**.

Your first job is to answer:

> What does a valid order look like, and which rows in the raw dataset violate that contract?

## Step 1 — Open the first notebook

Open:

```text
notebooks/01_why_data_validation.ipynb
```

Run the cells from top to bottom.

## Step 2 — Explore the raw dataset

File:

```text
data/raw/orders.csv
```

The dataset intentionally contains multiple categories of data-quality problems.

Try to identify problems related to:

- data types
- missing values
- duplicate identifiers
- allowed categories
- numeric ranges
- cross-column relationships
- dates

Do not worry if you cannot find all of them yet.

## Step 3 — Read the business contract

Read:

```text
docs/01_order_data_contract.md
```

Separate the requirements into two groups:

### Column-level rules

Rules that can be checked using a single column.

### DataFrame-level rules

Rules that require comparing multiple columns.

## Step 4 — First implementation task

Open:

```text
src/pandera_lab/schemas/orders.py
```

It contains a TODO skeleton for `OrderSchema`.

Do not implement everything at once. We will build it progressively and test each decision.

## Learning rule

Whenever a validation fails, do not immediately fix the row. First answer:

1. Which contract was violated?
2. Is this a structural, dtype, null, uniqueness, range, category, or business-rule error?
3. Should the pipeline reject the data, coerce it, filter it, or clean it elsewhere?

That distinction is more important than memorizing a Pandera method name.
