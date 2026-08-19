"""Validation-report utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from pandera_lab.validation import ValidationResult


def summarize_failure_cases(failure_cases: pd.DataFrame) -> pd.DataFrame:
    """Aggregate raw Pandera failure cases by column and check."""
    if failure_cases.empty:
        return pd.DataFrame(columns=["column", "check", "failures"])

    frame = failure_cases.copy()

    if "column" not in frame.columns:
        frame["column"] = "<dataframe>"
    else:
        frame["column"] = frame["column"].fillna("<dataframe>").astype(str)

    if "check" not in frame.columns:
        frame["check"] = "<unknown>"
    else:
        frame["check"] = frame["check"].fillna("<unknown>").astype(str)

    return (
        frame.groupby(["column", "check"], dropna=False)
        .size()
        .reset_index(name="failures")
        .sort_values(["column", "failures", "check"], ascending=[True, False, True])
        .reset_index(drop=True)
    )


def write_failure_report(
    result: ValidationResult,
    path: str | Path,
) -> Path:
    """Write detailed failure cases to CSV.

    Raises:
        ValueError: if validation succeeded and therefore no failure report exists.
    """
    if result.is_valid:
        raise ValueError("Cannot write a failure report for valid data.")

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.failure_cases.to_csv(destination, index=False)
    return destination


def write_failure_summary(
    result: ValidationResult,
    path: str | Path,
) -> Path:
    """Write an aggregated failure summary to CSV."""
    if result.is_valid:
        raise ValueError("Cannot write a failure summary for valid data.")

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    summarize_failure_cases(result.failure_cases).to_csv(destination, index=False)
    return destination
