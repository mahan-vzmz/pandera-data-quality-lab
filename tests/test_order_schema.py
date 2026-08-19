"""Phase 2 tests for the OrderSchema."""

from __future__ import annotations

import pandas as pd
import pandera.pandas as pa
import pytest

from pandera_lab.schemas import OrderSchema


def make_valid_orders() -> pd.DataFrame:
    """Return a small dataframe with Phase-2-valid order data."""
    return pd.DataFrame(
        {
            "order_id": [2001, 2002, 2003],
            "customer_id": ["C001", "C002", "C003"],
            "product_id": ["P001", "P002", "P003"],
            "quantity": [2, 1, 4],
            "unit_price": [100.0, 25.0, 50.0],
            "discount": [0.10, 0.00, 0.25],
            "total": [180.0, 25.0, 150.0],
            "status": ["paid", "shipped", "pending"],
            "order_date": pd.to_datetime(
                ["2026-08-01", "2026-08-02", "2026-08-03"]
            ),
        }
    )


def test_valid_orders_pass() -> None:
    df = make_valid_orders()
    validated = OrderSchema.validate(df)
    pd.testing.assert_frame_equal(validated, df)


def test_duplicate_order_id_fails() -> None:
    df = make_valid_orders()
    df.loc[1, "order_id"] = df.loc[0, "order_id"]

    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)


def test_zero_quantity_fails() -> None:
    df = make_valid_orders()
    df.loc[1, "quantity"] = 0

    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)


def test_negative_quantity_fails() -> None:
    df = make_valid_orders()
    df.loc[1, "quantity"] = -1

    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)


def test_non_positive_unit_price_fails() -> None:
    df = make_valid_orders()
    df.loc[0, "unit_price"] = 0.0

    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)


@pytest.mark.parametrize("bad_discount", [-0.01, 1.01])
def test_discount_outside_unit_interval_fails(bad_discount: float) -> None:
    df = make_valid_orders()
    df.loc[0, "discount"] = bad_discount

    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)


def test_invalid_status_fails() -> None:
    df = make_valid_orders()
    df.loc[0, "status"] = "refunded"

    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)


def test_wrong_total_still_passes_in_phase_2() -> None:
    """Cross-column total validation is intentionally a Phase-4 concern."""
    df = make_valid_orders()
    df.loc[0, "total"] = 999_999.0

    validated = OrderSchema.validate(df)
    assert validated.loc[0, "total"] == 999_999.0


def test_extra_column_is_allowed_in_phase_2() -> None:
    """strict=False is an intentional temporary design decision."""
    df = make_valid_orders()
    df["internal_note"] = ["a", "b", "c"]

    validated = OrderSchema.validate(df)
    assert "internal_note" in validated.columns


def test_order_date_must_already_be_datetime_in_phase_2() -> None:
    """Phase 2 validates dtype; Phase 3 will parse/coerce raw CSV dates."""
    df = make_valid_orders()
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")

    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)
