"""Raw input loading utilities.

Phase 3 intentionally keeps CSV loading simple. The raw dataframe is allowed to
contain text representations of numbers/dates. Pandera owns the typed contract
and coercion decisions for the analytical boundary.
"""

from pathlib import Path

import pandas as pd


def load_orders_csv(path: str | Path) -> pd.DataFrame:
    """Load an orders CSV without pre-cleaning or date parsing.

    This preserves the raw-input problem so that schema coercion and error
    reporting remain observable during validation.
    """
    return pd.read_csv(Path(path))
