"""Build both resale data products. Run from repository root."""

from pathlib import Path
import argparse
import pandas as pd
from homerun_housing.transactions import clean_transactions
from homerun_housing.listings import split_resale_transactions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="Raw data.gov.sg resale CSV")
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--lookback-months", type=int, default=3)
    parser.add_argument("--reference-month", default=None, help="YYYY-MM (excluded as incomplete)")
    args = parser.parse_args()

    cleaned = clean_transactions(pd.read_csv(args.input))
    print(f"Input: {len(cleaned):,} records, exact duplicate rows preserved: {cleaned.duplicated().sum():,}")
    historical_df, listings_df = split_resale_transactions(
        cleaned, lookback_months=args.lookback_months, reference_month=args.reference_month
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, frame in (
        ("resale_transactions_historical.parquet", historical_df),
        ("resale_supply_proxy.parquet", listings_df),
    ):
        target = args.output_dir / filename
        frame.assign(month=frame["month"].astype(str)).to_parquet(target, index=False)
        print(f"Saved {target}: {len(frame):,} rows ({frame['month'].min()} to {frame['month'].max()})")


if __name__ == "__main__":
    main()
