"""
main_window.py
--------------
Главное окно приложения: выбор источника данных, справочники, 7 отчётов,
окно настроек.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
import sys

from scripts.gui.clients_window import open_clients_window
from scripts.gui.accounts_window import open_accounts_window
from scripts.gui import (
    report_text,
    report_statistics,
    report_pivot,
    report_bar_chart,
    report_histogram,
    report_boxplot,
    report_scatter,
)
from scripts.gui.settings_window import open_settings_window
from scripts.gui.data_mode_dialog import open_data_mode_dialog


# ────────────────────────────────────────────────────────────────────────────
def create_main_window(root: tk.Tk, cfg) -> None:
    """Строит главное меню программы."""

    root.title("Информационно-аналитическое приложение")
    root.geometry("800x620")

    # --- выбор источника данных ----------------------------------------- #
    ttk.Button(
        root,
        text="📂 Источник данных",
        command=lambda: open_data_mode_dialog(root),
    ).pack(pady=5)

    # --- справочники ----------------------------------------------------- #
    ttk.Button(root, text="Справочник клиентов",
               command=open_clients_window).pack(pady=5)
    ttk.Button(root, text="Справочник счетов",
               command=open_accounts_window).pack(pady=5)

    ttk.Separator(root, orient="horizontal").pack(fill=tk.X, pady=10)

    # --- отчёты ---------------------------------------------------------- #
    reports = [
        ("1. Проекция",             report_text.open_report_text),
        ("2. Статистика",           report_statistics.open_report_statistics),
        ("3. Сводная таблица",      report_pivot.open_report_pivot),
        ("4. Столбчатая диаграмма", report_bar_chart.open_report_bar_chart),
        ("5. Гистограмма",          report_histogram.open_report_histogram),
        ("6. Box-Plot",             report_boxplot.open_report_boxplot),
        ("7. Рассеяние",            report_scatter.open_report_scatter),
    ]

    for title, cmd in reports:
        ttk.Button(root, text=title, command=cmd).pack(pady=2)

    ttk.Separator(root, orient="horizontal").pack(fill=tk.X, pady=10)

    # --- настройки ------------------------------------------------------- #
    ttk.Button(root, text="⚙ Настройки",
               command=lambda: open_settings_window(root)).pack(pady=5)

    # Версия / выход
    ttk.Label(root, text=f"Python {sys.version.split()[0]}").pack(side=tk.BOTTOM, pady=4)
