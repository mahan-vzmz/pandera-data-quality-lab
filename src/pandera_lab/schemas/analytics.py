"""Typed output contract for analytics-ready enriched orders."""

from __future__ import annotations

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from pandera_lab.business_rules import (
    discount_amount_matches_formula,
    gross_amount_matches_formula,
    is_discounted_matches_discount,
    net_amount_matches_total,
    order_month_matches_date,
)
from pandera_lab.schemas.orders import OrderSchema


class EnrichedOrderSchema(OrderSchema):
    """Strict semantic contract produced by the Phase-5 transformation."""

    gross_amount: Series[float] = pa.Field(ge=0, nullable=False)
    discount_amount: Series[float] = pa.Field(ge=0, nullable=False)
    net_amount: Series[float] = pa.Field(ge=0, nullable=False)
    order_month: Series[str] = pa.Field(nullable=False)
    is_discounted: Series[bool] = pa.Field(nullable=False)

    @pa.dataframe_check(
        name="gross_amount_matches_formula",
    )
    def gross_amount_is_correct(cls, df: pd.DataFrame) -> Series[bool]:
        return gross_amount_matches_formula(df)

    @pa.dataframe_check(
        name="discount_amount_matches_formula",
    )
    def discount_amount_is_correct(cls, df: pd.DataFrame) -> Series[bool]:
        return discount_amount_matches_formula(df)

    @pa.dataframe_check(
        name="net_amount_matches_total",
    )
    def net_amount_is_correct(cls, df: pd.DataFrame) -> Series[bool]:
        return net_amount_matches_total(df)

    @pa.dataframe_check(
        name="order_month_matches_date",
    )
    def order_month_is_correct(cls, df: pd.DataFrame) -> Series[bool]:
        return order_month_matches_date(df)

    @pa.dataframe_check(
        name="is_discounted_matches_discount",
    )
    def discount_flag_is_correct(cls, df: pd.DataFrame) -> Series[bool]:
        return is_discounted_matches_discount(df)

    class Config:
        # Internal/trusted outputs are exact: unexpected columns are defects.
        strict = True
