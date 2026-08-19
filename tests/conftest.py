"""Shared test fixtures for the final reliability suite."""

from __future__ import annotations

import pandas as pd
import pytest


BASE_ORDER_COLUMNS = [
    "order_id",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount",
    "total",
    "status",
    "order_date",
]

ENRICHED_COLUMNS = BASE_ORDER_COLUMNS + [
    "gross_amount",
    "discount_amount",
    "net_amount",
    "order_month",
    "is_discounted",
]


@pytest.fixture
def valid_typed_orders() -> pd.DataFrame:
    """Return a fully typed dataframe satisfying the final OrderSchema."""
    return pd.DataFrame(
        {
            "order_id": [6001, 6002, 6003],
            "customer_id": ["C601", "C602", "C603"],
            "product_id": ["P601", "P602", "P603"],
            "quantity": [2, 3, 1],
            "unit_price": [100.0, 20.0, 80.0],
            "discount": [0.10, 0.00, 0.25],
            "total": [180.0, 60.0, 60.0],
            "status": ["paid", "shipped", "pending"],
            "order_date": pd.to_datetime(
                ["2026-08-20", "2026-08-21", "2026-09-01"]
            ),
        }
    )


@pytest.fixture
def valid_raw_orders() -> pd.DataFrame:
    """Return valid orders in realistic CSV-like string representation."""
    return pd.DataFrame(
        {
            "order_id": ["6001", "6002", "6003"],
            "customer_id": ["C601", "C602", "C603"],
            "product_id": ["P601", "P602", "P603"],
            "quantity": ["2", "3", "1"],
            "unit_price": ["100.0", "20.0", "80.0"],
            "discount": ["0.10", "0.00", "0.25"],
            "total": ["180.0", "60.0", "60.0"],
            "status": ["paid", "shipped", "pending"],
            "order_date": ["2026-08-20", "2026-08-21", "2026-09-01"],
            "internal_note": ["source-a", "source-b", "source-c"],
        }
    )


@pytest.fixture
def valid_enriched_orders(valid_typed_orders: pd.DataFrame) -> pd.DataFrame:
    """Return an analytics-ready dataframe satisfying EnrichedOrderSchema."""
    return valid_typed_orders.assign(
        gross_amount=[200.0, 60.0, 80.0],
        discount_amount=[20.0, 0.0, 20.0],
        net_amount=[180.0, 60.0, 60.0],
        order_month=["2026-08", "2026-08", "2026-09"],
        is_discounted=[True, False, True],
    )
