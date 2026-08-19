"""Phase 3 tests: coercion, nulls, lazy failures, filtering, and reports."""

from __future__ import annotations

import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
)

from pandera_lab.reporting import (
    summarize_failure_cases,
    write_failure_report,
    write_failure_summary,
)
from pandera_lab.validation import validate_orders


def make_valid_raw_text_orders() -> pd.DataFrame:
    """A valid input frame whose typed values arrive as raw strings."""
    return pd.DataFrame(
        {
            "order_id": ["3001", "3002", "3003"],
            "customer_id": ["C301", "C302", "C303"],
            "product_id": ["P301", "P302", "P303"],
            "quantity": ["2", "1", "4"],
            "unit_price": ["100.0", "25.0", "50.0"],
            "discount": ["0.10", "0.00", "0.25"],
            "total": ["180.0", "25.0", "150.0"],
            "status": ["paid", "shipped", "pending"],
            "order_date": ["2026-08-01", "2026-08-02", "2026-08-03"],
            "internal_note": ["a", "b", "c"],
        }
    )


def test_valid_raw_text_values_are_coerced() -> None:
    result = validate_orders(make_valid_raw_text_orders())

    assert result.is_valid
    assert result.data is not None

    validated = result.data

    assert is_integer_dtype(validated["order_id"])
    assert is_integer_dtype(validated["quantity"])
    assert is_float_dtype(validated["unit_price"])
    assert is_float_dtype(validated["discount"])
    assert is_float_dtype(validated["total"])
    assert is_datetime64_any_dtype(validated["order_date"])


def test_extra_column_is_filtered_from_validated_output() -> None:
    result = validate_orders(make_valid_raw_text_orders())

    assert result.is_valid
    assert result.data is not None
    assert "internal_note" not in result.data.columns


def test_lazy_validation_aggregates_multiple_value_failures() -> None:
    df = make_valid_raw_text_orders()

    # Keep these values coercible so Pandera can reach the value/domain checks.
    df.loc[1, "order_id"] = df.loc[0, "order_id"]
    df.loc[0, "quantity"] = "0"
    df.loc[1, "unit_price"] = "-5"
    df.loc[2, "discount"] = "1.2"
    df.loc[0, "status"] = "UNKNOWN"

    result = validate_orders(df)

    assert not result.is_valid
    assert result.data is None

    failed_columns = set(result.failed_columns)
    assert {"order_id", "quantity", "unit_price", "discount", "status"} <= failed_columns


def test_uncoercible_quantity_is_reported() -> None:
    df = make_valid_raw_text_orders()
    df.loc[1, "quantity"] = "two"

    result = validate_orders(df)

    assert not result.is_valid
    assert "quantity" in result.failed_columns


def test_invalid_calendar_date_is_reported() -> None:
    df = make_valid_raw_text_orders()
    df.loc[1, "order_date"] = "2026-02-30"

    result = validate_orders(df)

    assert not result.is_valid
    assert "order_date" in result.failed_columns


def test_missing_required_customer_id_is_reported() -> None:
    df = make_valid_raw_text_orders()
    df.loc[1, "customer_id"] = None

    result = validate_orders(df)

    assert not result.is_valid
    assert "customer_id" in result.failed_columns


def test_failure_summary_counts_errors() -> None:
    df = make_valid_raw_text_orders()
    df.loc[0, "quantity"] = "0"
    df.loc[1, "status"] = "UNKNOWN"

    result = validate_orders(df)
    summary = summarize_failure_cases(result.failure_cases)

    assert not summary.empty
    assert {"column", "check", "failures"} <= set(summary.columns)
    assert int(summary["failures"].sum()) >= 2


def test_failure_reports_are_written(tmp_path) -> None:
    df = make_valid_raw_text_orders()
    df.loc[0, "quantity"] = "0"

    result = validate_orders(df)

    detail_path = write_failure_report(
        result,
        tmp_path / "detail.csv",
    )
    summary_path = write_failure_summary(
        result,
        tmp_path / "summary.csv",
    )

    assert detail_path.exists()
    assert summary_path.exists()

    detail_df = pd.read_csv(detail_path)
    summary_df = pd.read_csv(summary_path)

    assert not detail_df.empty
    assert not summary_df.empty
