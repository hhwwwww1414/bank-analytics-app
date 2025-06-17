import pandas as pd
import pytest

from scripts.reporting import report_projection, report_statistics

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'client_id': [1, 2, 3, 4],
        'age': [30, 40, 50, 60],
        'gender': ['M', 'F', 'M', 'F'],
        'city': ['Москва', 'Казань', 'Москва', 'Екб'],
        'income': [1000.0, 2000.0, 3000.0, 4000.0],
        'reg_date': pd.to_datetime([
            '2020-01-01', '2021-06-15', '2020-01-01', '2022-12-31'
        ]),
    })

def test_report_projection_all(sample_df):
    proj = report_projection(sample_df, ['client_id', 'income'], n_rows=None)
    assert list(proj.columns) == ['client_id', 'income']
    assert len(proj) == 4

def test_report_projection_limit(sample_df):
    proj2 = report_projection(sample_df, ['age'], n_rows=2)
    assert len(proj2) == 2
    assert list(proj2['age']) == [30, 40]

def test_report_statistics_numeric_and_categorical(sample_df):
    stats_df, freq = report_statistics(
        sample_df, ['age', 'income'], ['gender', 'city']
    )
    # numeric stats
    for col in ['count', 'mean', 'std', 'min', 'max']:
        assert col in stats_df.columns
    assert set(stats_df.index) == {'age', 'income'}

    # categorical freqs
    for cat in ['gender', 'city']:
        assert cat in freq
        df_freq = freq[cat]
        assert 'count' in df_freq.columns and 'percent' in df_freq.columns
        assert df_freq['count'].sum() == len(sample_df)

def test_report_statistics_empty_raises(sample_df):
    with pytest.raises(ValueError):
        report_statistics(sample_df, [], [])
