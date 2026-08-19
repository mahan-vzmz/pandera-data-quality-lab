"""Reusable business-rule and derived-value helpers.

The schema layer declares contracts. This module owns the domain calculations
used by both transformations and dataframe-level validation checks so formulas
are not duplicated across the codebase.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype


# Half a cent: enough to absorb ordinary floating-point representation noise,
# but not enough to accept a one-cent business discrepancy.
TOTAL_ABSOLUTE_TOLERANCE = 0.005


def non_blank_text(series: pd.Series) -> pd.Series:
    """Return True where string values contain non-whitespace characters."""
    return series.astype("string").str.strip().ne("").fillna(False)


def _numeric_column(df: pd.DataFrame, name: str) -> pd.Series:
    """Return a numeric view of a column, using NaN for unparseable values."""
    if name not in df.columns:
        return pd.Series(np.nan, index=df.index, dtype=float)
    return pd.to_numeric(df[name], errors="coerce")


def _all_true(df: pd.DataFrame) -> pd.Series:
    """Return an all-True row mask used to avoid cascading check failures."""
    return pd.Series(True, index=df.index, dtype=bool)


def _numeric_values_match(
    actual: pd.Series,
    expected: pd.Series,
    *,
    atol: float = TOTAL_ABSOLUTE_TOLERANCE,
) -> pd.Series:
    """Compare numeric series only where both values are comparable.

    Unparseable prerequisites deliberately evaluate to True here so their
    column-level dtype/coercion failures remain the authoritative errors.
    """
    actual_numeric = pd.to_numeric(actual, errors="coerce")
    expected_numeric = pd.to_numeric(expected, errors="coerce")
    comparable = actual_numeric.notna() & expected_numeric.notna()

    result = pd.Series(True, index=actual.index, dtype=bool)
    if comparable.any():
        result.loc[comparable] = np.isclose(
            actual_numeric.loc[comparable],
            expected_numeric.loc[comparable],
            rtol=0.0,
            atol=atol,
        )
    return result


def expected_gross_amount(df: pd.DataFrame) -> pd.Series:
    """Calculate gross amount before discount: ``unit_price * quantity``."""
    return _numeric_column(df, "unit_price") * _numeric_column(df, "quantity")


def expected_discount_amount(df: pd.DataFrame) -> pd.Series:
    """Calculate the monetary discount applied to the gross amount."""
    return expected_gross_amount(df) * _numeric_column(df, "discount")


def expected_order_total(df: pd.DataFrame) -> pd.Series:
    """Calculate contractual net order total."""
    return expected_gross_amount(df) * (1 - _numeric_column(df, "discount"))


def total_matches_formula(
    df: pd.DataFrame,
    *,
    atol: float = TOTAL_ABSOLUTE_TOLERANCE,
) -> pd.Series:
    """Validate ``total == unit_price * quantity * (1 - discount)``.

    Rows with unparseable prerequisites are deliberately skipped here so
    column-level coercion/null errors remain the authoritative failures.
    """
    if "total" not in df.columns:
        return _all_true(df)
    return _numeric_values_match(
        df["total"],
        expected_order_total(df),
        atol=atol,
    )


def gross_amount_matches_formula(
    df: pd.DataFrame,
    *,
    atol: float = TOTAL_ABSOLUTE_TOLERANCE,
) -> pd.Series:
    """Validate the derived ``gross_amount`` output field."""
    if "gross_amount" not in df.columns:
        return _all_true(df)
    return _numeric_values_match(
        df["gross_amount"],
        expected_gross_amount(df),
        atol=atol,
    )


def discount_amount_matches_formula(
    df: pd.DataFrame,
    *,
    atol: float = TOTAL_ABSOLUTE_TOLERANCE,
) -> pd.Series:
    """Validate the derived ``discount_amount`` output field."""
    if "discount_amount" not in df.columns:
        return _all_true(df)
    return _numeric_values_match(
        df["discount_amount"],
        expected_discount_amount(df),
        atol=atol,
    )


def net_amount_matches_total(
    df: pd.DataFrame,
    *,
    atol: float = TOTAL_ABSOLUTE_TOLERANCE,
) -> pd.Series:
    """Validate that analytics ``net_amount`` preserves contractual total."""
    if "net_amount" not in df.columns or "total" not in df.columns:
        return _all_true(df)
    return _numeric_values_match(df["net_amount"], df["total"], atol=atol)


def order_month_matches_date(df: pd.DataFrame) -> pd.Series:
    """Validate ``order_month`` as the YYYY-MM representation of order_date."""
    if "order_month" not in df.columns or "order_date" not in df.columns:
        return _all_true(df)

    dates = pd.to_datetime(df["order_date"], errors="coerce")
    expected = dates.dt.strftime("%Y-%m")
    actual = df["order_month"].astype("string")
    comparable = dates.notna() & actual.notna()

    result = _all_true(df)
    if comparable.any():
        result.loc[comparable] = (
            actual.loc[comparable].to_numpy()
            == expected.loc[comparable].to_numpy()
        )
    return result


def is_discounted_matches_discount(df: pd.DataFrame) -> pd.Series:
    """Validate boolean discount flag against ``discount > 0``."""
    if "is_discounted" not in df.columns or "discount" not in df.columns:
        return _all_true(df)

    actual = df["is_discounted"]
    if not is_bool_dtype(actual.dtype):
        # Let the output dtype contract report the root cause.
        return _all_true(df)

    discount = _numeric_column(df, "discount")
    comparable = discount.notna() & actual.notna()
    expected = discount.gt(0)

    result = _all_true(df)
    if comparable.any():
        result.loc[comparable] = (
            actual.loc[comparable].to_numpy()
            == expected.loc[comparable].to_numpy()
        )
    return result
