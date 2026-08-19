"""Frozen historical schemas used by earlier educational notebooks.

The production-facing schemas evolve with the repository. These classes
preserve the exact learning boundary of earlier phases so old notebooks stay
reproducible as later phases add stricter contracts and pipeline behavior.
"""

from __future__ import annotations

import pandas as pd
import pandera.pandas as pa
from pandera.dtypes import DateTime
from pandera.typing import Series

from pandera_lab.business_rules import non_blank_text, total_matches_formula


ALLOWED_ORDER_STATUSES = ("pending", "paid", "shipped", "cancelled")


class Phase2OrderSchema(pa.DataFrameModel):
    """Schema as taught at the end of Phase 2."""

    order_id: Series[int] = pa.Field(unique=True)
    customer_id: Series[str]
    product_id: Series[str]
    quantity: Series[int] = pa.Field(gt=0)
    unit_price: Series[float] = pa.Field(gt=0)
    discount: Series[float] = pa.Field(ge=0, le=1)
    total: Series[float]
    status: Series[str] = pa.Field(isin=ALLOWED_ORDER_STATUSES)
    order_date: Series[DateTime]

    class Config:
        strict = False


class Phase3OrderSchema(pa.DataFrameModel):
    """Schema as taught at the end of Phase 3, before business rules."""

    order_id: Series[int] = pa.Field(unique=True, nullable=False, coerce=True)
    customer_id: Series[str] = pa.Field(nullable=False)
    product_id: Series[str] = pa.Field(nullable=False)
    quantity: Series[int] = pa.Field(gt=0, nullable=False, coerce=True)
    unit_price: Series[float] = pa.Field(gt=0, nullable=False, coerce=True)
    discount: Series[float] = pa.Field(
        ge=0,
        le=1,
        nullable=False,
        coerce=True,
    )
    total: Series[float] = pa.Field(nullable=False, coerce=True)
    status: Series[str] = pa.Field(
        isin=ALLOWED_ORDER_STATUSES,
        nullable=False,
    )
    order_date: Series[DateTime] = pa.Field(nullable=False, coerce=True)

    class Config:
        strict = "filter"


class Phase4OrderSchema(pa.DataFrameModel):
    """Schema as taught at the end of Phase 4, including business rules."""

    order_id: Series[int] = pa.Field(unique=True, nullable=False, coerce=True)
    customer_id: Series[str] = pa.Field(nullable=False)
    product_id: Series[str] = pa.Field(nullable=False)
    quantity: Series[int] = pa.Field(gt=0, nullable=False, coerce=True)
    unit_price: Series[float] = pa.Field(gt=0, nullable=False, coerce=True)
    discount: Series[float] = pa.Field(
        ge=0,
        le=1,
        nullable=False,
        coerce=True,
    )
    total: Series[float] = pa.Field(nullable=False, coerce=True)
    status: Series[str] = pa.Field(
        isin=ALLOWED_ORDER_STATUSES,
        nullable=False,
    )
    order_date: Series[DateTime] = pa.Field(nullable=False, coerce=True)

    @pa.check(
        "customer_id",
        name="customer_id_not_blank",
        error="customer_id must contain non-whitespace characters",
    )
    def customer_id_not_blank(cls, customer_id: Series[str]) -> Series[bool]:
        return non_blank_text(customer_id)

    @pa.check(
        "product_id",
        name="product_id_not_blank",
        error="product_id must contain non-whitespace characters",
    )
    def product_id_not_blank(cls, product_id: Series[str]) -> Series[bool]:
        return non_blank_text(product_id)

    @pa.dataframe_check(
        name="total_matches_formula",
        error=(
            "total must equal unit_price * quantity * (1 - discount) "
            "within the configured currency tolerance"
        ),
    )
    def total_matches_business_formula(
        cls,
        df: pd.DataFrame,
    ) -> Series[bool]:
        return total_matches_formula(df)

    class Config:
        strict = "filter"
