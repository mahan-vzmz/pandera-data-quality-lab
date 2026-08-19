"""Run the Phase-2 schema against the known-good reference CSV."""

from pathlib import Path

import pandas as pd

from pandera_lab.schemas import OrderSchema


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE = PROJECT_ROOT / "data" / "reference" / "orders_valid.csv"


def main() -> None:
    df = pd.read_csv(REFERENCE, parse_dates=["order_date"])
    validated = OrderSchema.validate(df)

    print("Phase-2 validation passed.")
    print(validated)


if __name__ == "__main__":
    main()
