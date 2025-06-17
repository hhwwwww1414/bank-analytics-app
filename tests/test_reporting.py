import pandas as pd
import numpy as np

import pytest

from scripts.reporting import report_projection, report_statistics

@pytest.fixture
def sample_df():
    # Создаём DataFrame с числовыми, категориальными и датой
    df = pd.DataFrame({
        'client_id': [1, 2, 3, 4],
        'age': [30, 40, 50, 60],
        'gender': ['M', 'F', 'M', 'F'],
        'city': ['Москва', 'Казань', 'Москва', 'Екб'],
        'income': [1000.0, 2000.0, 3000.0, 4000.0],
        'reg_date': pd.to_datetime(['2020-01-01', '2021-06-15', '2020-01-01', '2022-12-31']),
    })
    return df

def test_report_projection_all(sample_df):
    df = sample_df
    # без ограничения по строкам
    proj = report_projection(df, ['client_id', 'income'], n_rows=0)
    assert list(proj.columns) == ['client_id', 'income']
    assert len(proj) == len(df)

def test_report_projection_limit(sample_df):
    df = sample_df
    proj2 = report_projection(df, ['age'], n_rows=2)
    assert len(proj2) == 2
    assert list(proj2['age']) == [30, 40]

def test_report_statistics_numeric_and_categorical(sample_df):
    df = sample_df
    # Вычисляем статистику по age и income, частоты по gender и city
    stats_df, freq = report_statistics(df, ['age', 'income'], ['gender', 'city'])
    # Проверяем, что в stats_df есть основные метрики
    for col in ['count', 'mean', 'std', 'min', 'max']:
        assert col in stats_df.columns
    # У нас две числовые строки в индексе
    assert set(stats_df.index) == {'age', 'income'}
    # Проверяем частоты — суммы должны совпадать с числом строк
    for cat in ['gender', 'city']:
        assert cat in freq
        total = freq[cat]['count'].sum()
        assert total == len(df)

def test_report_statistics_no_select_raises(sample_df):
    df = sample_df
    # Если ни numeric, ни categorical не переданы — в reporting будет пусто
    with pytest.raises(ValueError):
        report_statistics(df, [], [])
