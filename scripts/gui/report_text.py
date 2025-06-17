"""
report_text.py
--------------
Отчёт 1. Проекция (выбор произвольных колонок и первых N строк).
Функциональный стиль — без классов.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

from scripts.data_management import load_clients
from scripts.reporting import report_projection


# ────────────────────────────────────────────────────────────────────────────
def open_report_text(parent: tk.Tk | tk.Toplevel | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Отчёт 1. Проекция")
    win.geometry("900x600")

    df = load_clients()

    # ---------- Панель управления ---------------------------------------- #
    ctl = ttk.Frame(win)
    ctl.pack(fill=tk.X, pady=5)

    # список колонок (мультивыбор)
    ttk.Label(ctl, text="Колонки").grid(row=0, column=0, sticky="w", padx=5)
    cols_var = tk.StringVar(value=df.columns.tolist())
    list_cols = tk.Listbox(
        ctl,
        listvariable=cols_var,
        selectmode=tk.MULTIPLE,
        height=6,
        exportselection=False,
        width=30,
    )
    list_cols.grid(row=1, column=0, padx=5, sticky="n")

    # количество строк
    ttk.Label(ctl, text="Первые N строк").grid(row=0, column=1, sticky="w", padx=10)
    spin_rows = ttk.Spinbox(
        ctl, from_=1, to=len(df), width=7, justify="center"
    )
    spin_rows.grid(row=1, column=1, sticky="n", padx=10)
    spin_rows.set(100)

    # ---------- Таблица результата --------------------------------------- #
    tree = ttk.Treeview(win, show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    vsb.place(in_=tree, relx=1.0, rely=0, relheight=1.0)
    tree.configure(yscrollcommand=vsb.set)

    # ---------- Функции --------------------------------------------------- #
    def run_report() -> None:
        cols = [df.columns[i] for i in list_cols.curselection()]
        if not cols:
            messagebox.showinfo("Выбор колонок", "Выберите хотя бы одну колонку")
            return

        n = int(spin_rows.get())
        res = report_projection(df, cols, n)

        tree.delete(*tree.get_children())
        tree["columns"] = cols
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        for _, row in res.iterrows():
            tree.insert("", tk.END, values=list(row))

        # сохраняем результат для экспорта
        win.result_df = res

    def export_csv() -> None:
        if not hasattr(win, "result_df"):
            messagebox.showinfo("Экспорт", "Сначала сформируйте отчёт")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if path:
            win.result_df.to_csv(path, index=False)
            messagebox.showinfo("Экспорт", f"Сохранено: {path}")

    # ---------- Кнопки ---------------------------------------------------- #
    btn_frame = ttk.Frame(ctl)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=8)

    ttk.Button(btn_frame, text="Сформировать", command=run_report).pack(side=tk.LEFT, padx=8)
    ttk.Button(btn_frame, text="Экспорт CSV", command=export_csv).pack(side=tk.LEFT, padx=8)
