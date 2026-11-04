import pandas as pd
import pytest
from homerun_housing.transactions import clean_transactions
from homerun_housing.listings import split_resale_transactions


def example():
    return pd.DataFrame({
        'month': ['2026-07', '2026-08', '2026-10', '2026-11'],
        'town': ['YISHUN'] * 4, 'flat_type': ['4 ROOM'] * 4,
        'block': ['123'] * 4, 'street_name': ['YISHUN ST 11'] * 4,
        'storey_range': ['01 TO 03'] * 4, 'floor_area_sqm': [90.0] * 4,
        'flat_model': ['Model A'] * 4, 'lease_commence_date': [1999] * 4,
        'remaining_lease': ['72 years 06 months'] * 4, 'resale_price': [500000] * 4,
    })


def test_split_includes_recent_sales_in_history():
    data = clean_transactions(example())
    history, proxy = split_resale_transactions(data, 3, '2026-11')
    assert len(history) == 3
    assert len(proxy) == 2
    assert history.month.max() == pd.Period('2026-10', freq='M')
    assert (data.remaining_lease_years == 72.5).all()


def test_preserves_exact_duplicates():
    data = pd.concat([example().iloc[:1], example().iloc[:1]], ignore_index=True)
    assert len(clean_transactions(data)) == 2


def test_missing_column_fails():
    with pytest.raises(ValueError, match='Missing required columns'):
        clean_transactions(example().drop(columns=['resale_price']))
