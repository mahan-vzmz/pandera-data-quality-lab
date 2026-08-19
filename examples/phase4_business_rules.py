"""Demonstrate Phase-4 custom and dataframe-level business rules."""

from pathlib import Path

import pandas as pd

from pandera_lab import (
    expected_order_total,
    load_orders_csv,
    summarize_failure_cases,
    validate_orders,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE = PROJECT_ROOT / "data" / "reference" / "orders_valid.csv"
RAW = PROJECT_ROOT / "data" / "raw" / "orders.csv"


def main() -> None:
    print("=== 1. Validate known-good reference data ===")
    reference_df = pd.read_csv(REFERENCE)
    reference_result = validate_orders(reference_df)
    print("valid:", reference_result.is_valid)

    print("\n=== 2. Break one total deliberately ===")
    wrong_total = reference_df.copy()
    wrong_total.loc[0, "total"] = 999.0

    wrong_result = validate_orders(wrong_total)
    print("valid:", wrong_result.is_valid)
    print(wrong_result.failure_cases.to_string(index=False))

    print("\n=== 3. Show expected totals ===")
    comparison = reference_df[
        ["order_id", "unit_price", "quantity", "discount", "total"]
    ].copy()
    comparison["expected_total"] = expected_order_total(reference_df)
    print(comparison.to_string(index=False))

    print("\n=== 4. Re-run the deliberately messy raw dataset ===")
    raw_df = load_orders_csv(RAW)
    raw_result = validate_orders(raw_df)
    print("valid:", raw_result.is_valid)
    print(summarize_failure_cases(raw_result.failure_cases).to_string(index=False))


if __name__ == "__main__":
    main()
