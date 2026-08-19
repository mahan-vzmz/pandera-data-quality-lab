"""Validate the messy raw CSV with the frozen Phase-3 contract."""

import sys
from pathlib import Path

import pandas as pd
import pandera.pandas as pa

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pandera_lab import (
    load_orders_csv,
    summarize_failure_cases,
    write_failure_report,
    write_failure_summary,
)
from pandera_lab.schemas import Phase3OrderSchema
from pandera_lab.validation import ValidationResult


RAW_ORDERS = PROJECT_ROOT / "data" / "raw" / "orders.csv"
REPORT_DIR = PROJECT_ROOT / "reports"


def validate_phase3(df: pd.DataFrame) -> ValidationResult:
    """Validate with the historical Phase-3 schema."""
    try:
        validated = Phase3OrderSchema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as exc:
        return ValidationResult(
            is_valid=False,
            data=None,
            failure_cases=exc.failure_cases.copy(),
        )

    return ValidationResult(
        is_valid=True,
        data=validated,
        failure_cases=pd.DataFrame(),
    )


def main() -> None:
    raw_df = load_orders_csv(RAW_ORDERS)
    result = validate_phase3(raw_df)

    if result.is_valid:
        print("Orders are valid [OK]")
        print(result.data)
        return

    print("Orders are invalid [FAIL]")
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
