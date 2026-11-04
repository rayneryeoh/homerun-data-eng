"""Recent resale transactions used as a proxy for resale-market supply."""

from __future__ import annotations

import pandas as pd


def split_resale_transactions(
    df: pd.DataFrame,
    lookback_months: int = 3,
    reference_month: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (historical_df, listings_df).

    Historical includes all transactions through the last complete month.
    Listings is a *subset* from the latest `lookback_months` complete months;
    its records represent completed sales, NOT observed active advertisements.

    The reference month is excluded, even if records exist for that month.
    """
    if not isinstance(lookback_months, int) or isinstance(lookback_months, bool) or lookback_months < 1:
        raise ValueError("lookback_months must be a positive integer")
    if "month" not in df.columns:
        raise ValueError("Missing required column: month")

    data = df.copy()
    if not isinstance(data["month"].dtype, pd.PeriodDtype):
        data["month"] = pd.to_datetime(
            data["month"].astype("string"), format="%Y-%m", errors="raise"
        ).dt.to_period("M")
    else:
        data["month"] = data["month"].dt.asfreq("M")

    current_month = (
        pd.Period(reference_month, freq="M")
        if reference_month is not None
        else pd.Timestamp.now(tz="Asia/Singapore").to_period("M")
    )
    end_month = current_month - 1
    start_month = end_month - lookback_months + 1

    historical_df = data.loc[data["month"] <= end_month].copy()
    listings_df = historical_df.loc[
        historical_df["month"].between(start_month, end_month)
    ].copy()

    return historical_df.reset_index(drop=True), listings_df.reset_index(drop=True)
