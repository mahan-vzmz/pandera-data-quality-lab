"""Reliability, regression, and integration hardening for Phase 6."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pandera.pandas as pa
import pytest

from pandera_lab.pipeline import run_order_pipeline
from pandera_lab.reporting import summarize_failure_cases, write_failure_report
from pandera_lab.schemas import (
    EnrichedOrderSchema,
    Phase2OrderSchema,
    Phase3OrderSchema,
    Phase4OrderSchema,
)
from pandera_lab.transformations import enrich_orders
from pandera_lab.validation import validate_orders


def test_enrichment_is_deterministic_and_does_not_mutate_input(
    valid_raw_orders: pd.DataFrame,
) -> None:
    original = valid_raw_orders.copy(deep=True)

    first = enrich_orders(valid_raw_orders)
    second = enrich_orders(valid_raw_orders)

    pd.testing.assert_frame_equal(valid_raw_orders, original)
    pd.testing.assert_frame_equal(first, second)


def test_enrichment_preserves_row_order_and_order_ids(valid_raw_orders: pd.DataFrame) -> None:
    enriched = enrich_orders(valid_raw_orders)
    assert enriched["order_id"].tolist() == [6001, 6002, 6003]
    assert enriched.index.tolist() == valid_raw_orders.index.tolist()


def test_validated_output_can_be_revalidated_without_semantic_drift(
    valid_raw_orders: pd.DataFrame,
) -> None:
    enriched = enrich_orders(valid_raw_orders)
    revalidated = EnrichedOrderSchema.validate(enriched)
    pd.testing.assert_frame_equal(enriched, revalidated)


def test_failure_summary_is_deterministic(valid_raw_orders: pd.DataFrame) -> None:
    broken = valid_raw_orders.copy()
    broken.loc[0, "quantity"] = "0"
    broken.loc[1, "status"] = "UNKNOWN"

    first = validate_orders(broken)
    second = validate_orders(broken)

    pd.testing.assert_frame_equal(
        summarize_failure_cases(first.failure_cases),
        summarize_failure_cases(second.failure_cases),
    )


def test_cannot_write_failure_report_for_success(valid_raw_orders: pd.DataFrame, tmp_path: Path) -> None:
    result = validate_orders(valid_raw_orders)
    assert result.is_valid

    with pytest.raises(ValueError, match="valid data"):
        write_failure_report(result, tmp_path / "should_not_exist.csv")


def test_historical_phase_boundaries_remain_reproducible() -> None:
    typed = pd.DataFrame(
        {
            "order_id": [7001],
            "customer_id": ["C700"],
            "product_id": ["P700"],
            "quantity": [2],
            "unit_price": [100.0],
            "discount": [0.10],
            "total": [999.0],
            "status": ["paid"],
            "order_date": pd.to_datetime(["2026-08-20"]),
            "extra_source_column": ["allowed in phase 2"],
        }
    )

    phase2 = Phase2OrderSchema.validate(typed)
    assert "extra_source_column" in phase2.columns

    raw_phase3 = typed.assign(
        order_id=["7001"],
        quantity=["2"],
        unit_price=["100.0"],
        discount=["0.10"],
        total=["999.0"],
        order_date=["2026-08-20"],
    )
    phase3 = Phase3OrderSchema.validate(raw_phase3)
    assert "extra_source_column" not in phase3.columns
    assert phase3.loc[0, "total"] == 999.0

    with pytest.raises((pa.errors.SchemaError, pa.errors.SchemaErrors)):
        Phase4OrderSchema.validate(raw_phase3, lazy=True)


def test_pipeline_recovers_cleanly_after_invalid_then_valid_batch(
    valid_raw_orders: pd.DataFrame,
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "orders.csv"
    output_path = tmp_path / "clean" / "orders_enriched.csv"
    report_dir = tmp_path / "reports"

    invalid = valid_raw_orders.copy()
    invalid.loc[0, "status"] = "UNKNOWN"
    invalid.to_csv(input_path, index=False)
    failed = run_order_pipeline(input_path, output_path, report_dir)

    assert not failed.succeeded
    assert not output_path.exists()
    assert failed.detail_report_path is not None
    assert failed.detail_report_path.exists()

    valid_raw_orders.to_csv(input_path, index=False)
    succeeded = run_order_pipeline(input_path, output_path, report_dir)

    assert succeeded.succeeded
    assert output_path.exists()
    assert failed.detail_report_path is not None
    assert not failed.detail_report_path.exists()


def test_pipeline_written_output_matches_direct_transformation(
    valid_raw_orders: pd.DataFrame,
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "orders.csv"
    output_path = tmp_path / "clean" / "orders_enriched.csv"
    report_dir = tmp_path / "reports"
    valid_raw_orders.to_csv(input_path, index=False)

    result = run_order_pipeline(input_path, output_path, report_dir)
    assert result.succeeded

    written = pd.read_csv(output_path, parse_dates=["order_date"])
    direct = enrich_orders(valid_raw_orders).reset_index(drop=True)
    pd.testing.assert_frame_equal(written, direct, check_dtype=False)
