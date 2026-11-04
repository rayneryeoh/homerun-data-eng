"""Cleaning and validation of data.gov.sg HDB resale transactions (2017+)."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = (
    "month", "town", "flat_type", "block", "street_name", "storey_range",
    "floor_area_sqm", "flat_model", "lease_commence_date",
    "remaining_lease", "resale_price",
)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Return a validated, consistently typed copy of resale transactions.

    'month' is stored as a pandas monthly Period. Keep identical rows: this
    public dataset has no unit/transaction ID, so deduplication is unsafe.
    """
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    result = df.copy()
    if result.empty:
        raise ValueError("Transaction dataset is empty")

    for column in ("town", "flat_type", "block", "street_name", "storey_range", "flat_model"):
        result[column] = result[column].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
        if result[column].isna().any() or result[column].eq("").any():
            raise ValueError(f"Missing or blank values in {column}")

    # Accept CSV-style YYYY-MM strings and already parsed datetime/Period values.
    if isinstance(result["month"].dtype, pd.PeriodDtype):
        result["month"] = result["month"].dt.asfreq("M")
    else:
        result["month"] = pd.to_datetime(result["month"].astype("string"), format="%Y-%m", errors="raise").dt.to_period("M")

    for column in ("floor_area_sqm", "resale_price"):
        result[column] = pd.to_numeric(result[column], errors="raise")
        if result[column].isna().any() or result[column].le(0).any():
            raise ValueError(f"{column} must contain strictly positive numeric values")

    result["lease_commence_date"] = pd.to_numeric(
        result["lease_commence_date"], errors="raise"
    ).astype("int64")
    if result["lease_commence_date"].lt(1900).any() or result["lease_commence_date"].gt(2100).any():
        raise ValueError("Unexpected lease_commence_date year")

    # e.g. '61 years 04 months' -> 61 + 4/12. Retain the original column too.
    lease = result["remaining_lease"].astype("string").str.strip()
    parts = lease.str.extract(r"^(\d+) years?(?:\s+(\d+) months?)?$")
    if parts[0].isna().any():
        raise ValueError("Unrecognised remaining_lease format")
    years = pd.to_numeric(parts[0])
    months = pd.to_numeric(parts[1]).fillna(0)
    if months.ge(12).any():
        raise ValueError("remaining_lease months must be between 0 and 11")
    result["remaining_lease"] = lease
    result["remaining_lease_years"] = years + months / 12

    # No drop_duplicates(): indistinguishable rows might be different flat sales.
    return result.reset_index(drop=True)
