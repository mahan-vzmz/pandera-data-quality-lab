"""End-to-end Phase-5 order pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pandera_lab.ingestion import load_orders_csv
from pandera_lab.reporting import write_failure_report, write_failure_summary
from pandera_lab.transformations import enrich_orders
from pandera_lab.validation import validate_orders


@dataclass(frozen=True)
class PipelineResult:
    """Observable result of one batch pipeline run."""

    succeeded: bool
    input_path: Path
    output_path: Path | None
    detail_report_path: Path | None
    summary_report_path: Path | None
    rows_read: int
    rows_written: int


def _report_paths(input_path: Path, report_dir: Path) -> tuple[Path, Path]:
    stem = input_path.stem
    return (
        report_dir / f"{stem}_validation_errors.csv",
        report_dir / f"{stem}_validation_summary.csv",
    )


def _remove_if_exists(path: Path) -> None:
    path.unlink(missing_ok=True)


def run_order_pipeline(
    input_path: str | Path,
    output_path: str | Path,
    report_dir: str | Path,
) -> PipelineResult:
    """Run ingestion → validation → typed enrichment → persistence.

    Source-data failures are an expected operational outcome: they generate
    structured reports and no trusted output. By contrast, exceptions raised
    by ``enrich_orders`` are intentionally *not* swallowed. At that point the
    input has already passed the source contract, so an output-schema failure
    indicates a transformation/programming defect that should fail loudly.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    report_dir = Path(report_dir)
    detail_report_path, summary_report_path = _report_paths(input_path, report_dir)

    raw_df = load_orders_csv(input_path)
    validation = validate_orders(raw_df)

    if not validation.is_valid:
        # Never leave an old trusted output that could be mistaken for this run.
        _remove_if_exists(output_path)
        report_dir.mkdir(parents=True, exist_ok=True)
        detail = write_failure_report(validation, detail_report_path)
        summary = write_failure_summary(validation, summary_report_path)
        return PipelineResult(
            succeeded=False,
            input_path=input_path,
            output_path=None,
            detail_report_path=detail,
            summary_report_path=summary,
            rows_read=len(raw_df),
            rows_written=0,
        )

    assert validation.data is not None  # narrowed by the successful result

    # Successful current state invalidates stale failure reports from old runs.
    _remove_if_exists(detail_report_path)
    _remove_if_exists(summary_report_path)

    enriched = enrich_orders(validation.data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(output_path, index=False)

    return PipelineResult(
        succeeded=True,
        input_path=input_path,
        output_path=output_path,
        detail_report_path=None,
        summary_report_path=None,
        rows_read=len(raw_df),
        rows_written=len(enriched),
    )
