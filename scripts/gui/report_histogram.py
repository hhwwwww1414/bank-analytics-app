"""
report_histogram.py
-------------------
Отчёт 5. Категоризированная гистограмма с валидацией типов.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import pandas as pd

from scripts.data_management import load_clients
from scripts.reporting import report_hist
from scripts.gui.gui_helpers import show_matplotlib


# ──────────────────────────────────────────────────────────────────────────
def open_report_histogram(parent: tk.Tk | tk.Toplevel | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Отчёт 5. Гистограмма")
    win.geometry("900x600")

    df = load_clients()

    # безопасные списки
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(
        exclude=["number", "datetime64[ns]", "datetime64[ns, UTC]"]
    ).columns.tolist()

    ctl = ttk.Frame(win)
    ctl.pack(fill=tk.X, pady=5)

    var_num = tk.StringVar()
    var_cat = tk.StringVar()

    ttk.Label(ctl, text="Числовой столбец").grid(row=0, column=0, padx=5, sticky="w")
    ttk.Combobox(ctl, textvariable=var_num, values=num_cols, width=20).grid(
        row=0, column=1, padx=5
    )
    ttk.Label(ctl, text="Категория (цвет)").grid(row=0, column=2, padx=5, sticky="w")
    ttk.Combobox(ctl, textvariable=var_cat, values=cat_cols, width=20).grid(
        row=0, column=3, padx=5
    )

    plot_frame = ttk.Frame(win)
    plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_report() -> None:
        n_col, c_col = var_num.get(), var_cat.get()
        # валидация выбора
        if not n_col or not c_col:
            messagebox.showinfo("Ввод", "Выберите числовой и категориальный столбцы")
            return
        if n_col not in num_cols:
            messagebox.showerror("Тип данных", f"Поле «{n_col}» не числовое")
            return
        if c_col not in cat_cols:
            messagebox.showerror("Тип данных", f"Поле «{c_col}» не категориальное")
            return
        if df[c_col].nunique(dropna=True) > 20:
            messagebox.showerror(
                "Слишком много категорий",
                f"{c_col}: {df[c_col].nunique()} уникальных значений (> 20)",
            )
            return

        try:
            win.config(cursor="watch")
            fig = report_hist(df, n_col, c_col)
        finally:
            win.config(cursor="")  # вернуть курсор

        win.fig = fig
        show_matplotlib(fig, plot_frame)

    def save_png() -> None:
        if not hasattr(win, "fig"):
            messagebox.showinfo("Сохранение", "Сначала постройте график")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if path:
            win.fig.savefig(path)
            messagebox.showinfo("Сохранение", f"Сохранено: {path}")

    ttk.Button(ctl, text="Построить", command=run_report).grid(
        row=1, column=0, columnspan=2, pady=5
    )
    ttk.Button(ctl, text="Сохранить PNG", command=save_png).grid(
        row=1, column=2, columnspan=2, pady=5
    )
