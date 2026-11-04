# Resale engineering implementation

Copy `transactions.py` and `listings.py` into the corresponding existing files under
`packages/homerun_housing/src/homerun_housing/`. The `pipelines/` and `tests/`
files can be merged into your existing repository. No changes to other modules
are required.

Install your `homerun_housing` package in editable mode and install pandas,
pyarrow, pytest as needed:

```bash
python -m pip install -e packages/homerun_housing
python -m pip install pandas pyarrow pytest
```

Run from the repository root:

```bash
python pipelines/build_resale.py --input data/raw/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv --reference-month 2026-11 --lookback-months 3
python -m pytest tests/test_resale.py -q
```

`historical_df` includes completed transactions through the month preceding
`reference_month`. `listings_df` is a subset of it. The listings proxy is
recent transaction activity, *not* observed active listings or asking prices.

Exact duplicate rows are intentionally preserved because publicly published
records do not contain identifiers that permit reliable deduplication.
