"""Validation boundary used through Phase 4."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import pandera.pandas as pa

from pandera_lab.schemas import OrderSchema


_FAILURE_CASE_COLUMNS = [
    "schema_context",
    "column",
    "check",
    "check_number",
    "failure_case",
    "index",
]


@dataclass(frozen=True)
class ValidationResult:
    """Structured result returned by the validation boundary."""

    is_valid: bool
    data: pd.DataFrame | None
    failure_cases: pd.DataFrame

    @property
    def failed_columns(self) -> tuple[str, ...]:
        """Return unique failing column names when available."""
        if self.failure_cases.empty or "column" not in self.failure_cases.columns:
            return ()

        values = (
            self.failure_cases["column"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        return tuple(sorted(values))


def _empty_failure_cases() -> pd.DataFrame:
    return pd.DataFrame(columns=_FAILURE_CASE_COLUMNS)


def validate_orders(df: pd.DataFrame) -> ValidationResult:
    """Validate orders lazily and return a machine-readable result.

    ``lazy=True`` asks Pandera to aggregate validation failures instead of
    stopping at the first error.
    """
    try:
        validated = OrderSchema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as exc:
        return ValidationResult(
            is_valid=False,
            data=None,
            failure_cases=exc.failure_cases.copy(),
        )

    return ValidationResult(
        is_valid=True,
        data=validated,
        failure_cases=_empty_failure_cases(),
    )
