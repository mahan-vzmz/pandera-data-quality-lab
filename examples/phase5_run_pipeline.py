"""Run the Phase-5 pipeline against both valid and invalid batches."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pandera_lab.pipeline import PipelineResult, run_order_pipeline


REFERENCE = PROJECT_ROOT / "data" / "reference" / "orders_valid.csv"
RAW = PROJECT_ROOT / "data" / "raw" / "orders.csv"
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
REPORT_DIR = PROJECT_ROOT / "reports"


def print_result(label: str, result: PipelineResult) -> None:
    print(f"\n=== {label} ===")
    print(f"succeeded:    {result.succeeded}")
    print(f"rows read:    {result.rows_read}")
    print(f"rows written: {result.rows_written}")
    print(f"output:       {result.output_path}")
    print(f"detail report:{result.detail_report_path}")
    print(f"summary:      {result.summary_report_path}")


def main() -> None:
    valid_result = run_order_pipeline(
        input_path=REFERENCE,
        output_path=CLEAN_DIR / "orders_enriched.csv",
        report_dir=REPORT_DIR,
    )
    print_result("VALID REFERENCE BATCH", valid_result)

    invalid_result = run_order_pipeline(
        input_path=RAW,
        output_path=CLEAN_DIR / "raw_orders_enriched.csv",
        report_dir=REPORT_DIR,
    )
    print_result("DELIBERATELY INVALID RAW BATCH", invalid_result)


if __name__ == "__main__":
    main()
