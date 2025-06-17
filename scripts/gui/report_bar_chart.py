"""
report_bar_chart.py
-------------------
Кластеризованная столбчатая диаграмма.

 • X  – категориальный столбец   (обязателен)
 • Y  – числовой столбец         (обязателен)
 • Hue – группировка (категор.)  (необязательна)

Если Hue не указан, строится простой bar-chart с агрегатом (count / mean / sum).
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import pandas as pd

from scripts.data_management import load_clients
from scripts.gui.gui_helpers import show_matplotlib

AGG_FUNCS = {"count": "count", "mean": "mean", "sum": "sum"}


# ---------- построение ----------------------------------------------------
def _make_bar(df: pd.DataFrame, x: str, y: str, hue: str | None, agg: str):
    if hue:                                      # с группировкой
        grp = getattr(df.groupby([x, hue])[y], AGG_FUNCS[agg])().unstack()
        ax = grp.plot(kind="bar", figsize=(8, 5))
        ax.legend(title=hue)
    else:                                        # без Hue
        grp = getattr(df.groupby(x)[y], AGG_FUNCS[agg])()
        ax = grp.plot(kind="bar", figsize=(8, 5))
    ax.set_xlabel(x)
    ax.set_ylabel(f"{agg}({y})")
    plt.tight_layout()
    return ax.get_figure()


# ---------- GUI -----------------------------------------------------------
def open_report_bar_chart(parent: tk.Misc | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Отчёт 4. Столбчатая диаграмма")
    win.geometry("1000x650")

    df = load_clients()
    num_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    ctrl = ttk.Frame(win)
    ctrl.pack(fill=tk.X, pady=5)

    var_x = tk.StringVar()
    var_y = tk.StringVar()
    var_hue = tk.StringVar()
    var_agg = tk.StringVar(value="count")

    # --- виджеты выбора ---------------------------------------------------
    def _combo(label, var, values, col):
        ttk.Label(ctrl, text=label).grid(row=0, column=col, sticky="w", padx=5)
        ttk.Combobox(ctrl, textvariable=var, values=values, width=15
                     ).grid(row=0, column=col + 1, padx=5)

    _combo("X (категория)",   var_x,   cat_cols, 0)
    _combo("Y (число)",       var_y,   num_cols, 2)
    _combo("Hue (группировка)", var_hue, [""] + cat_cols, 4)
    _combo("Агрегат",         var_agg, list(AGG_FUNCS), 6)

    plot_frame = ttk.Frame(win)
    plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- построение -------------------------------------------------------
    def run():
        x, y, hue, agg = var_x.get(), var_y.get(), var_hue.get(), var_agg.get()
        if not (x and y):
            messagebox.showinfo("Поля", "Заполните X и Y")
            return
        fig = _make_bar(df, x, y, hue or None, agg)
        win.fig = fig
        show_matplotlib(fig, plot_frame)

    def save_png():
        if not hasattr(win, "fig"):
            messagebox.showinfo("Сохранение", "Сначала постройте график")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if path:
            win.fig.savefig(path)
            messagebox.showinfo("PNG", f"Сохранено: {path}")

    ttk.Button(ctrl, text="Построить", command=run).grid(row=1, column=0, columnspan=3, pady=5)
    ttk.Button(ctrl, text="Сохранить PNG", command=save_png).grid(row=1, column=4, columnspan=3, pady=5)
