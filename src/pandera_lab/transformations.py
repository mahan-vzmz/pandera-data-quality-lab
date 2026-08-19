"""Typed dataframe transformations for Phase 5."""

from __future__ import annotations

import pandera.pandas as pa
from pandera.typing import DataFrame

from pandera_lab.business_rules import (
    expected_discount_amount,
    expected_gross_amount,
)
from pandera_lab.schemas import EnrichedOrderSchema, OrderSchema


@pa.check_types(lazy=True)
def enrich_orders(
    df: DataFrame[OrderSchema],
) -> DataFrame[EnrichedOrderSchema]:
    """Create analytics features from a validated order dataframe.

    ``@pa.check_types`` validates/coerces the annotated input before the
    function body and validates the annotated output before returning it.
    The function uses ``assign`` so it does not add columns to the caller's
    dataframe in place.
    """
    gross_amount = expected_gross_amount(df)
    discount_amount = expected_discount_amount(df)

    return df.assign(
        gross_amount=gross_amount.astype(float),
        discount_amount=discount_amount.astype(float),
        net_amount=df["total"].astype(float),
        order_month=df["order_date"].dt.strftime("%Y-%m"),
        is_discounted=df["discount"].gt(0),
    )
