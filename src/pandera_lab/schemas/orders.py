"""Order dataframe contract.

This file is intentionally incomplete in the starter phase.
Implement the schema incrementally while working through the lessons.
"""

import pandera.pandas as pa
from pandera.typing import Series


class OrderSchema(pa.DataFrameModel):
    """Contract for validated analytical order data."""

    # TODO 1: define order_id
    # TODO 2: define customer_id
    # TODO 3: define product_id
    # TODO 4: define quantity
    # TODO 5: define unit_price
    # TODO 6: define discount
    # TODO 7: define total
    # TODO 8: define status
    # TODO 9: define order_date

    # Later:
    # TODO 10: add a dataframe-level check for total
    # TODO 11: decide how extra columns should be handled
    # TODO 12: decide where coercion belongs

    pass
