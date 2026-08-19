"""Pandera contract for order data.

Phase 3 scope:
- explicit null policy
- per-field dtype coercion
- datetime coercion
- strict filtering of unexpected columns
- lazy validation compatibility

Still deliberately deferred to Phase 4:
- custom column checks
- dataframe-level / cross-column business rules
- validation of ``total == unit_price * quantity * (1 - discount)``
"""

import pandera.pandas as pa
from pandera.dtypes import DateTime
from pandera.typing import Series


ALLOWED_ORDER_STATUSES = ("pending", "paid", "shipped", "cancelled")


class OrderSchema(pa.DataFrameModel):
    """Validated analytical shape for an order record."""

    order_id: Series[int] = pa.Field(
        unique=True,
        nullable=False,
        coerce=True,
    )

    # Text identifiers are intentionally *not* coerced in Phase 3.
    # A missing identifier should remain visibly missing and fail validation.
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

    # The total formula is a Phase-4 dataframe-level business rule.
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

    class Config:
        # Operational/source-only columns such as ``internal_note`` are accepted
        # at the input boundary but removed from the validated analytical frame.
        strict = "filter"
