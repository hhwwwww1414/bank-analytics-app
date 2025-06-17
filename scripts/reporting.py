"""reporting.py

Семь функций генерации отчетов.
Каждая функция принимает необходимый набор DataFrame'ов и параметров,
формирует результат (таблицу или matplotlib.figure.Figure) и возвращает его.
"""

import pandas as pd
import matplotlib.pyplot as plt


# 1. Текстовый простой отчет (проекция)
def report_projection(df: pd.DataFrame, columns: list[str], n_rows: int | None = None) -> pd.DataFrame:
    return df.loc[:n_rows, columns] if n_rows else df[columns]


# 2. Статистический отчет
def report_statistics(df: pd.DataFrame, numeric_cols: list[str], categorical_cols: list[str]) -> pd.DataFrame:
    stats_numeric = df[numeric_cols].describe().T
    freq_tables = {col: df[col].value_counts(normalize=False).to_frame('freq') for col in categorical_cols}
    return stats_numeric, freq_tables


# 3. Сводная таблица
def report_pivot(df: pd.DataFrame, rows: str, cols: str, values: str, aggfunc: str = 'count') -> pd.DataFrame:
    return pd.pivot_table(df, index=rows, columns=cols, values=values, aggfunc=aggfunc, fill_value=0)


# 4. Кластеризованная столбчатая диаграмма
def report_bar(df: pd.DataFrame, x: str, hue: str):
    fig, ax = plt.subplots()
    grouped = df.groupby([x, hue]).size().unstack(fill_value=0)
    grouped.plot(kind='bar', ax=ax)
    return fig


# 5. Категоризированная гистограмма
def report_hist(df: pd.DataFrame, numeric_col: str, category_col: str):
    fig, ax = plt.subplots()
    for category, subset in df.groupby(category_col):
        subset[numeric_col].plot(kind='hist', alpha=0.5, ax=ax, label=str(category))
    ax.legend()
    return fig


# 6. Диаграмма Box-Plot
def report_box(df: pd.DataFrame, numeric_col: str, category_col: str):
    fig, ax = plt.subplots()
    df.boxplot(column=numeric_col, by=category_col, ax=ax)
    fig.suptitle('')
    return fig


# 7. Диаграмма рассеивания
def report_scatter(df: pd.DataFrame, x: str, y: str, category_col: str):
    fig, ax = plt.subplots()
    categories = df[category_col].unique()
    for cat in categories:
        subset = df[df[category_col] == cat]
        ax.scatter(subset[x], subset[y], label=str(cat))
    ax.legend()
    return fig
