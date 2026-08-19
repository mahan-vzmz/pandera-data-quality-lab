# Contributing

## Development setup

```bash
python -m pip install -e ".[dev]"
```

## Before submitting a change

Run:

```bash
python scripts/quality_gate.py
```

At minimum, a contract change should include:

1. a failing test that demonstrates the required behavior,
2. the implementation,
3. updated learning documentation if semantics changed,
4. a regression check for any affected historical phase.

## Educational stability rule

Do not rewrite earlier phase behavior by editing historical classes in `schemas/history.py` unless the lesson itself was incorrect.

If the final `OrderSchema` evolves, add a new current behavior while keeping earlier lessons reproducible.

## Data files

Keep committed datasets small and synthetic. Do not commit private, customer, or credential-bearing data.
