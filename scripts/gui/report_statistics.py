"""
report_statistics.py
--------------------
Отчёт 2. Статистический анализ:
  • для выбранных числовых колонок — count / mean / std / min … max
  • для выбранных категориальных — частоты значений
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from datetime import datetime

import pandas as pd

from scripts.data_management import load_clients
from scripts.reporting import report_statistics


# ──────────────────────────── GUI ─────────────────────────────────────────
def open_report_statistics(parent: tk.Misc | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Отчёт 2. Статистика")
    win.geometry("1000x650")

    df = load_clients()
    numeric_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    # ---------- Панель выбора -------------------------------------------
    ctl = ttk.Frame(win)
    ctl.pack(fill=tk.X, pady=5)

    ttk.Label(ctl, text="Числовые:").grid(row=0, column=0, sticky="w", padx=5)
    list_num = tk.Listbox(
        ctl,
        listvariable=tk.StringVar(value=numeric_cols),
        selectmode=tk.MULTIPLE,
        height=6,
        exportselection=False,
    )
    list_num.grid(row=1, column=0, padx=5)

    ttk.Label(ctl, text="Категориальные:").grid(row=0, column=1, sticky="w", padx=5)
    list_cat = tk.Listbox(
        ctl,
        listvariable=tk.StringVar(value=cat_cols),
        selectmode=tk.MULTIPLE,
        height=6,
        exportselection=False,
    )
    list_cat.grid(row=1, column=1, padx=5)

    # ---------- Treeview результата -------------------------------------
    tree = ttk.Treeview(win, show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ---------- Формирование отчёта -------------------------------------
    def run_report() -> None:
        ncols = [numeric_cols[i] for i in list_num.curselection()]
        ccols = [cat_cols[i] for i in list_cat.curselection()]

        if not ncols and not ccols:
            messagebox.showinfo("Выбор", "Выберите хотя бы одну колонку")
            return

        stats_df, freq_dict = report_statistics(df, ncols, ccols)

        tree.delete(*tree.get_children())
        tree["columns"] = ["metric"] + stats_df.columns.tolist()
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor=tk.CENTER)

        for metric, row in stats_df.iterrows():
            tree.insert("", tk.END, values=[metric] + list(row))

        win.stats_df = stats_df
        win.freq_dict = freq_dict

    # ---------- Экспорт --------------------------------------------------
    GRAPHICS_DIR = Path(__file__).parent.parent.parent / "graphics"
    GRAPHICS_DIR.mkdir(exist_ok=True)

    def export_excel() -> None:
        if not hasattr(win, "stats_df"):
            messagebox.showinfo("Экспорт", "Сначала сформируйте отчёт")
            return

        default = GRAPHICS_DIR / f"statistics_{datetime.now():%Y%m%d}.xlsx"
        path = filedialog.asksaveasfilename(
            initialdir=GRAPHICS_DIR,
            initialfile=default.name,
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
        )
        if not path:
            return

        try:
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                win.stats_df.to_excel(writer, sheet_name="numeric")
                for name, frame in win.freq_dict.items():
                    frame.to_excel(writer, sheet_name=f"freq_{name}")
        except ImportError:
            messagebox.showerror(
                "openpyxl отсутствует",
                "Для экспорта в .xlsx установите пакет:\n\n    pip install openpyxl",
            )
        else:
            messagebox.showinfo("Экспорт", f"Сохранено: {path}")

    # ---------- Кнопки ---------------------------------------------------
    ttk.Button(ctl, text="Сформировать", command=run_report).grid(
        row=2, column=0, columnspan=2, pady=5
    )
    ttk.Button(ctl, text="Экспорт Excel", command=export_excel).grid(
        row=3, column=0, columnspan=2, pady=2
    )
