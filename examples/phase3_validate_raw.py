"""Validate the deliberately messy raw CSV and produce Phase-3 reports."""

from pathlib import Path

from pandera_lab import (
    load_orders_csv,
    summarize_failure_cases,
    validate_orders,
    write_failure_report,
    write_failure_summary,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_ORDERS = PROJECT_ROOT / "data" / "raw" / "orders.csv"
REPORT_DIR = PROJECT_ROOT / "reports"


def main() -> None:
    raw_df = load_orders_csv(RAW_ORDERS)
    result = validate_orders(raw_df)

    if result.is_valid:
        print("Orders are valid ✅")
        print(result.data)
        return

    print("Orders are invalid ❌")
    print("\nDetailed failure cases:")
    print(result.failure_cases.to_string(index=False))

    print("\nFailure summary:")
    print(summarize_failure_cases(result.failure_cases).to_string(index=False))

    detail_path = write_failure_report(
        result,
        REPORT_DIR / "phase3_validation_errors.csv",
    )
    summary_path = write_failure_summary(
        result,
        REPORT_DIR / "phase3_validation_summary.csv",
    )

    print(f"\nDetailed report: {detail_path}")
    print(f"Summary report:  {summary_path}")


if __name__ == "__main__":
    main()
