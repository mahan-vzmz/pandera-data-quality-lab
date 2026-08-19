"""Phase 5 tests for typed transformations and pipeline orchestration."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pandera.pandas as pa
import pytest
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_float_dtype,
    is_integer_dtype,
)
from pandera.typing import DataFrame

from pandera_lab.pipeline import run_order_pipeline
from pandera_lab.schemas import EnrichedOrderSchema, OrderSchema
from pandera_lab.transformations import enrich_orders


BASE_ORDER_COLUMNS = [
    "order_id",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount",
    "total",
    "status",
    "order_date",
]

ENRICHED_COLUMNS = BASE_ORDER_COLUMNS + [
    "gross_amount",
    "discount_amount",
    "net_amount",
    "order_month",
    "is_discounted",
]


def make_valid_raw_orders() -> pd.DataFrame:
    """Return valid orders in realistic CSV-like string representation."""
    return pd.DataFrame(
        {
            "order_id": ["5001", "5002", "5003"],
            "customer_id": ["C501", "C502", "C503"],
            "product_id": ["P501", "P502", "P503"],
            "quantity": ["2", "3", "1"],
            "unit_price": ["100.0", "20.0", "80.0"],
            "discount": ["0.10", "0.00", "0.25"],
            "total": ["180.0", "60.0", "60.0"],
            "status": ["paid", "shipped", "pending"],
            "order_date": ["2026-08-20", "2026-08-21", "2026-09-01"],
            "internal_note": ["source-a", "source-b", "source-c"],
        }
    )


def make_valid_enriched_orders() -> pd.DataFrame:
    """Construct a fully typed dataframe satisfying EnrichedOrderSchema."""
    return pd.DataFrame(
        {
            "order_id": [5001, 5002, 5003],
            "customer_id": ["C501", "C502", "C503"],
            "product_id": ["P501", "P502", "P503"],
            "quantity": [2, 3, 1],
            "unit_price": [100.0, 20.0, 80.0],
            "discount": [0.10, 0.00, 0.25],
            "total": [180.0, 60.0, 60.0],
            "status": ["paid", "shipped", "pending"],
            "order_date": pd.to_datetime(
                ["2026-08-20", "2026-08-21", "2026-09-01"]
            ),
            "gross_amount": [200.0, 60.0, 80.0],
            "discount_amount": [20.0, 0.0, 20.0],
            "net_amount": [180.0, 60.0, 60.0],
            "order_month": ["2026-08", "2026-08", "2026-09"],
            "is_discounted": [True, False, True],
        }
    )


def test_enriched_schema_accepts_semantically_correct_output() -> None:
    validated = EnrichedOrderSchema.validate(make_valid_enriched_orders())
    assert validated.columns.tolist() == ENRICHED_COLUMNS


@pytest.mark.parametrize(
    ("column", "bad_value", "check_name"),
    [
        ("gross_amount", 999.0, "gross_amount_matches_formula"),
        ("discount_amount", 999.0, "discount_amount_matches_formula"),
        ("net_amount", 999.0, "net_amount_matches_total"),
        ("order_month", "2026-12", "order_month_matches_date"),
        ("is_discounted", False, "is_discounted_matches_discount"),
    ],
)
def test_enriched_schema_rejects_wrong_derived_values(
    column: str,
    bad_value: object,
    check_name: str,
) -> None:
    df = make_valid_enriched_orders()
    df.loc[0, column] = bad_value

    with pytest.raises(pa.errors.SchemaErrors) as exc_info:
        EnrichedOrderSchema.validate(df, lazy=True)

    failure_checks = exc_info.value.failure_cases["check"].astype(str)
    assert failure_checks.str.contains(check_name).any()


def test_enriched_schema_rejects_unexpected_output_column() -> None:
    df = make_valid_enriched_orders()
    df["debug_column"] = "must not leak"

    with pytest.raises((pa.errors.SchemaError, pa.errors.SchemaErrors)):
        EnrichedOrderSchema.validate(df)


def test_enrich_orders_validates_input_and_returns_typed_output() -> None:
    raw = make_valid_raw_orders()
    original_columns = raw.columns.tolist()

    enriched = enrich_orders(raw)

    # The caller's dataframe is not structurally mutated.
    assert raw.columns.tolist() == original_columns

    # The decorated input contract coerces/filter source values before the body.
    assert enriched.columns.tolist() == ENRICHED_COLUMNS
    assert is_integer_dtype(enriched["order_id"])
    assert is_integer_dtype(enriched["quantity"])
    assert is_float_dtype(enriched["unit_price"])
    assert is_float_dtype(enriched["discount"])
    assert is_float_dtype(enriched["total"])
    assert is_datetime64_any_dtype(enriched["order_date"])
    assert is_bool_dtype(enriched["is_discounted"])

    assert enriched["gross_amount"].tolist() == [200.0, 60.0, 80.0]
    assert enriched["discount_amount"].tolist() == [20.0, 0.0, 20.0]
    assert enriched["net_amount"].tolist() == [180.0, 60.0, 60.0]
    assert enriched["order_month"].tolist() == ["2026-08", "2026-08", "2026-09"]
    assert enriched["is_discounted"].tolist() == [True, False, True]

    # Source-only metadata is filtered by the input OrderSchema.
    assert "internal_note" not in enriched.columns


def test_enrich_orders_rejects_invalid_input_contract() -> None:
    raw = make_valid_raw_orders()
    raw.loc[0, "total"] = "999.0"  # violates Phase-4 total rule

    with pytest.raises(pa.errors.SchemaErrors):
        enrich_orders(raw)


def test_check_types_rejects_semantically_broken_output() -> None:
    @pa.check_types(lazy=True)
    def broken_transform(
        df: DataFrame[OrderSchema],
    ) -> DataFrame[EnrichedOrderSchema]:
        gross = df["unit_price"] * df["quantity"]
        return df.assign(
            gross_amount=gross,
            discount_amount=gross * df["discount"],
            net_amount=999.0,  # valid dtype, invalid output semantics
            order_month=df["order_date"].dt.strftime("%Y-%m"),
            is_discounted=df["discount"].gt(0),
        )

    with pytest.raises(pa.errors.SchemaErrors) as exc_info:
        broken_transform(make_valid_raw_orders())

    failure_checks = exc_info.value.failure_cases["check"].astype(str)
    assert failure_checks.str.contains("net_amount_matches_total").any()


def test_check_types_rejects_missing_output_column() -> None:
    @pa.check_types(lazy=True)
    def incomplete_transform(
        df: DataFrame[OrderSchema],
    ) -> DataFrame[EnrichedOrderSchema]:
        gross = df["unit_price"] * df["quantity"]
        return df.assign(
            gross_amount=gross,
            discount_amount=gross * df["discount"],
            net_amount=df["total"],
            order_month=df["order_date"].dt.strftime("%Y-%m"),
            # is_discounted deliberately omitted
        )

    with pytest.raises(pa.errors.SchemaErrors):
        incomplete_transform(make_valid_raw_orders())


def test_valid_pipeline_writes_trusted_enriched_output(tmp_path: Path) -> None:
    input_path = tmp_path / "valid_orders.csv"
    output_path = tmp_path / "clean" / "orders_enriched.csv"
    report_dir = tmp_path / "reports"
    make_valid_raw_orders().to_csv(input_path, index=False)

    result = run_order_pipeline(
        input_path=input_path,
        output_path=output_path,
        report_dir=report_dir,
    )

    assert result.succeeded
    assert result.rows_read == 3
    assert result.rows_written == 3
    assert result.output_path == output_path
    assert result.detail_report_path is None
    assert result.summary_report_path is None
    assert output_path.exists()

    written = pd.read_csv(output_path)
    assert written.columns.tolist() == ENRICHED_COLUMNS
    assert written["gross_amount"].tolist() == [200.0, 60.0, 80.0]
    assert "internal_note" not in written.columns


def test_invalid_pipeline_writes_reports_and_no_trusted_output(tmp_path: Path) -> None:
    input_path = tmp_path / "invalid_orders.csv"
    output_path = tmp_path / "clean" / "orders_enriched.csv"
    report_dir = tmp_path / "reports"

    invalid = make_valid_raw_orders()
    invalid.loc[0, "status"] = "UNKNOWN"
    invalid.loc[1, "total"] = "999.0"
    invalid.to_csv(input_path, index=False)

    result = run_order_pipeline(
        input_path=input_path,
        output_path=output_path,
        report_dir=report_dir,
    )

    assert not result.succeeded
    assert result.rows_read == 3
    assert result.rows_written == 0
    assert result.output_path is None
    assert result.detail_report_path is not None
    assert result.summary_report_path is not None
    assert result.detail_report_path.exists()
    assert result.summary_report_path.exists()
    assert not output_path.exists()

    detail = pd.read_csv(result.detail_report_path)
    assert not detail.empty
    assert {"status", "DataFrameSchema"} & set(detail["column"].astype(str))


def test_successful_pipeline_removes_stale_failure_reports(tmp_path: Path) -> None:
    input_path = tmp_path / "orders.csv"
    output_path = tmp_path / "clean" / "orders_enriched.csv"
    report_dir = tmp_path / "reports"

    invalid = make_valid_raw_orders()
    invalid.loc[0, "status"] = "UNKNOWN"
    invalid.to_csv(input_path, index=False)

    failed = run_order_pipeline(input_path, output_path, report_dir)
    assert not failed.succeeded
    assert failed.detail_report_path is not None
    assert failed.summary_report_path is not None
    assert failed.detail_report_path.exists()
    assert failed.summary_report_path.exists()

    make_valid_raw_orders().to_csv(input_path, index=False)
    succeeded = run_order_pipeline(input_path, output_path, report_dir)

    assert succeeded.succeeded
    assert output_path.exists()
    assert not failed.detail_report_path.exists()
    assert not failed.summary_report_path.exists()


def test_failed_pipeline_removes_stale_trusted_output(tmp_path: Path) -> None:
    input_path = tmp_path / "orders.csv"
    output_path = tmp_path / "clean" / "orders_enriched.csv"
    report_dir = tmp_path / "reports"

    make_valid_raw_orders().to_csv(input_path, index=False)
    succeeded = run_order_pipeline(input_path, output_path, report_dir)
    assert succeeded.succeeded
    assert output_path.exists()

    invalid = make_valid_raw_orders()
    invalid.loc[0, "quantity"] = "0"
    invalid.to_csv(input_path, index=False)

    failed = run_order_pipeline(input_path, output_path, report_dir)
    assert not failed.succeeded
    assert not output_path.exists()


def test_pipeline_does_not_misclassify_transform_bug_as_source_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A programming defect after successful input validation must propagate."""
    input_path = tmp_path / "orders.csv"
    output_path = tmp_path / "clean" / "orders_enriched.csv"
    report_dir = tmp_path / "reports"
    make_valid_raw_orders().to_csv(input_path, index=False)

    def explode(_df: pd.DataFrame) -> pd.DataFrame:
        raise RuntimeError("simulated transformation defect")

    monkeypatch.setattr("pandera_lab.pipeline.enrich_orders", explode)

    with pytest.raises(RuntimeError, match="simulated transformation defect"):
        run_order_pipeline(input_path, output_path, report_dir)

    assert not output_path.exists()
    assert not report_dir.exists() or not any(report_dir.iterdir())
