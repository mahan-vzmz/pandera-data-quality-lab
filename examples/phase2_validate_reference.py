"""Run the Phase-2 schema against the known-good reference CSV."""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pandera_lab.schemas import Phase2OrderSchema as OrderSchema


REFERENCE = PROJECT_ROOT / "data" / "reference" / "orders_valid.csv"


def main() -> None:
    df = pd.read_csv(REFERENCE, parse_dates=["order_date"])
    validated = OrderSchema.validate(df)

    print("Phase-2 validation passed.")
    print(validated)


if __name__ == "__main__":
    main()
