"""Pandera contract for order data.

Phase 2 scope:
- DataFrameModel
- typed Series fields
- uniqueness
- numeric range constraints
- allowed status categories

Deliberately deferred to later phases:
- coercion and CSV parsing strategy
- explicit nullable handling
- lazy validation reports
- strict/filter behavior for extra columns
- cross-column validation of ``total``
"""

import pandera.pandas as pa
from pandera.dtypes import DateTime
from pandera.typing import Series


ALLOWED_ORDER_STATUSES = ("pending", "paid", "shipped", "cancelled")


class OrderSchema(pa.DataFrameModel):
    """Column-level data contract for an analytical order record."""

    order_id: Series[int] = pa.Field(unique=True)
    customer_id: Series[str]
    product_id: Series[str]
    quantity: Series[int] = pa.Field(gt=0)
    unit_price: Series[float] = pa.Field(gt=0)
    discount: Series[float] = pa.Field(ge=0, le=1)

    # In Phase 2 we only validate the dtype of total.
    # The relationship:
    # total = unit_price * quantity * (1 - discount)
    # is intentionally deferred to Phase 4.
    total: Series[float]

    status: Series[str] = pa.Field(isin=ALLOWED_ORDER_STATUSES)

    # The schema expects a real pandas datetime dtype.
    # Turning raw CSV strings into datetimes is an ingestion/coercion problem
    # that will be solved in Phase 3.
    order_date: Series[DateTime]

    class Config:
        # Phase 2 deliberately permits extra columns such as ``internal_note``.
        # We will compare strict=False, strict=True, and strict="filter"
        # explicitly in Phase 3.
        strict = False
