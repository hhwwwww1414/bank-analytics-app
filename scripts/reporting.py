"""reporting.py

Семь функций генерации отчетов.
Каждая функция принимает необходимый набор DataFrame'ов и параметров,
формирует результат (таблицу или matplotlib.figure.Figure) и возвращает его.
"""

import pandas as pd
import matplotlib.pyplot as plt


# 1. Текстовый простой отчет (проекция)
def report_projection(df: pd.DataFrame, columns: list[str], n_rows: int | None = None) -> pd.DataFrame:
    """Проекция: возвращает указанные столбцы и, при n_rows>0, первые n_rows строк."""
    if n_rows:
        return df[columns].head(n_rows)
    return df[columns]


# 2. Статистический отчет
def report_statistics(
    df: pd.DataFrame,
    numeric_cols: list[str],
    categorical_cols: list[str]
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    """
    Возвращает:
     - stats_df: индекс = numeric_cols, колонки = ['count','mean','std','min','max']
     - freq_dict: для каждого cat_col — DataFrame с индексом уровней
       и колонками ['count','percent']
    """
    if not numeric_cols and not categorical_cols:
        raise ValueError("Выберите хотя бы одну числовую или категориальную колонку")

    # numeric statistics
    stats_df = df[numeric_cols].agg(['count', 'mean', 'std', 'min', 'max']).T

    # categorical frequencies
    freq_dict: dict[str, pd.DataFrame] = {}
    total = len(df)
    for col in categorical_cols:
        vc = df[col].value_counts(dropna=False)
        freq_df = vc.rename_axis(col).rename('count').to_frame()
        freq_df['percent'] = (freq_df['count'] / total) * 100
        freq_dict[col] = freq_df

    return stats_df, freq_dict


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
    for cat in df[category_col].unique():
        subset = df[df[category_col] == cat]
        ax.scatter(subset[x], subset[y], label=str(cat))
    ax.legend()
    return fig
