"""Phase 4 tests for custom and cross-column business rules."""

from __future__ import annotations

import pandas as pd
import pandera.pandas as pa

from pandera_lab.business_rules import (
    TOTAL_ABSOLUTE_TOLERANCE,
    expected_order_total,
)
from pandera_lab.schemas import OrderSchema
from pandera_lab.validation import validate_orders


def make_valid_orders() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["4001", "4002", "4003"],
            "customer_id": ["C401", "C402", "C403"],
            "product_id": ["P401", "P402", "P403"],
            "quantity": ["2", "3", "1"],
            "unit_price": ["100.0", "0.1", "25.0"],
            "discount": ["0.10", "0.00", "0.20"],
            "total": ["180.0", "0.3", "20.0"],
            "status": ["paid", "shipped", "pending"],
            "order_date": ["2026-08-20", "2026-08-21", "2026-08-22"],
            "internal_note": ["x", "y", "z"],
        }
    )


def test_expected_total_helper() -> None:
    df = make_valid_orders()
    expected = expected_order_total(df)

    assert expected.iloc[0] == 180.0
    assert abs(expected.iloc[1] - 0.3) < 1e-12
    assert expected.iloc[2] == 20.0


def test_valid_business_rules_pass() -> None:
    result = validate_orders(make_valid_orders())

    assert result.is_valid
    assert result.data is not None


def test_blank_customer_id_fails_custom_column_check() -> None:
    df = make_valid_orders()
    df.loc[0, "customer_id"] = "   "

    result = validate_orders(df)

    assert not result.is_valid
    assert "customer_id" in result.failed_columns
    assert result.failure_cases["check"].astype(str).str.contains(
        "customer_id_not_blank"
    ).any()


def test_blank_product_id_fails_custom_column_check() -> None:
    df = make_valid_orders()
    df.loc[0, "product_id"] = ""

    result = validate_orders(df)

    assert not result.is_valid
    assert "product_id" in result.failed_columns


def test_wrong_total_fails_dataframe_check() -> None:
    df = make_valid_orders()
    df.loc[0, "total"] = "179.50"

    result = validate_orders(df)

    assert not result.is_valid
    assert result.failure_cases["check"].astype(str).str.contains(
        "total_matches_formula"
    ).any()


def test_floating_point_representation_noise_passes() -> None:
    """0.1 * 3 is not represented exactly in binary floating point."""
    df = make_valid_orders()
    df.loc[1, "total"] = "0.30000000000000004"

    result = validate_orders(df)

    assert result.is_valid


def test_sub_half_cent_difference_is_tolerated() -> None:
    df = make_valid_orders()
    df.loc[0, "total"] = str(180.0 + TOTAL_ABSOLUTE_TOLERANCE / 2)

    result = validate_orders(df)

    assert result.is_valid


def test_one_cent_business_error_fails() -> None:
    df = make_valid_orders()
    df.loc[0, "total"] = "180.01"

    result = validate_orders(df)

    assert not result.is_valid
    assert result.failure_cases["check"].astype(str).str.contains(
        "total_matches_formula"
    ).any()


def test_uncoercible_quantity_does_not_create_cascading_total_failure() -> None:
    df = make_valid_orders()
    df.loc[0, "quantity"] = "two"

    result = validate_orders(df)

    assert not result.is_valid
    assert "quantity" in result.failed_columns

    total_failures = result.failure_cases["check"].astype(str).str.contains(
        "total_matches_formula"
    )
    assert not total_failures.any()


def test_wrong_total_raises_schema_error_in_fail_fast_mode() -> None:
    df = make_valid_orders()
    df.loc[0, "total"] = "999.0"

    try:
        OrderSchema.validate(df)
    except pa.errors.SchemaError as exc:
        assert "total" in str(exc).lower()
    else:
        raise AssertionError("Expected OrderSchema.validate to reject wrong total.")
