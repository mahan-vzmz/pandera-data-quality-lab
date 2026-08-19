"""Pandera contract for order data.

Phase 4 adds custom business rules on top of the Phase-3 raw-input boundary:

- ``@pa.check`` for custom single-column rules
- ``@pa.dataframe_check`` for cross-column invariants
- custom check names and error messages
- floating-point-safe total validation
"""

from __future__ import annotations

import pandas as pd
import pandera.pandas as pa
from pandera.dtypes import DateTime
from pandera.typing import Series

from pandera_lab.business_rules import non_blank_text, total_matches_formula


ALLOWED_ORDER_STATUSES = ("pending", "paid", "shipped", "cancelled")


class OrderSchema(pa.DataFrameModel):
    """Trusted analytical contract for an order record."""

    order_id: Series[int] = pa.Field(
        unique=True,
        nullable=False,
        coerce=True,
    )

    customer_id: Series[str] = pa.Field(nullable=False)
    product_id: Series[str] = pa.Field(nullable=False)

    quantity: Series[int] = pa.Field(
        gt=0,
        nullable=False,
        coerce=True,
    )

    unit_price: Series[float] = pa.Field(
        gt=0,
        nullable=False,
        coerce=True,
    )

    discount: Series[float] = pa.Field(
        ge=0,
        le=1,
        nullable=False,
        coerce=True,
    )

    total: Series[float] = pa.Field(
        nullable=False,
        coerce=True,
    )

    status: Series[str] = pa.Field(
        isin=ALLOWED_ORDER_STATUSES,
        nullable=False,
    )

    order_date: Series[DateTime] = pa.Field(
        nullable=False,
        coerce=True,
    )

    @pa.check(
        "customer_id",
        name="customer_id_not_blank",
    )
    def customer_id_not_blank(
        cls,
        customer_id: Series[str],
    ) -> Series[bool]:
        """Reject empty or whitespace-only customer identifiers."""
        return non_blank_text(customer_id)

    @pa.check(
        "product_id",
        name="product_id_not_blank",
    )
    def product_id_not_blank(
        cls,
        product_id: Series[str],
    ) -> Series[bool]:
        """Reject empty or whitespace-only product identifiers."""
        return non_blank_text(product_id)

    @pa.dataframe_check(
        name="total_matches_formula",
    )
    def total_matches_business_formula(
        cls,
        df: pd.DataFrame,
    ) -> Series[bool]:
        """Validate the derived order total across multiple columns."""
        return total_matches_formula(df)

    class Config:
        # Source-only metadata can arrive, but it must not leak downstream.
        strict = "filter"
