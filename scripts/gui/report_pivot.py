"""report_pivot.py

Отчёт 3. Сводная таблица.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

from scripts.data_management import load_clients
from scripts.reporting import report_pivot


def open_report_pivot(parent: tk.Tk | tk.Toplevel | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title('Отчёт 3. Сводная таблица')
    win.geometry('1000x600')

    df = load_clients()
    cols = df.columns.tolist()

    # -------- Controls ---------------------------------------------------- #
    ctl = ttk.Frame(win)
    ctl.pack(fill=tk.X, pady=5)

    tkvars = {name: tk.StringVar() for name in ('rows', 'cols', 'values', 'agg')}

    def make_combo(text, var, col):
        ttk.Label(ctl, text=text).grid(row=0, column=col*2, sticky='w', padx=5)
        ttk.Combobox(ctl, textvariable=var, values=cols, width=15).grid(row=0, column=col*2+1, padx=5)

    make_combo('Строки', tkvars['rows'], 0)
    make_combo('Колонки', tkvars['cols'], 1)
    make_combo('Значение', tkvars['values'], 2)

    ttk.Label(ctl, text='Агрегация').grid(row=1, column=0, sticky='w', padx=5)
    ttk.Combobox(ctl, textvariable=tkvars['agg'],
                 values=['count', 'mean', 'sum'], width=10).grid(row=1, column=1, padx=5)

    # -------- Treeview ---------------------------------------------------- #
    tree = ttk.Treeview(win, show='headings')
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_report():
        r, c, v = tkvars['rows'].get(), tkvars['cols'].get(), tkvars['values'].get()
        agg = tkvars['agg'].get() or 'count'
        if not (r and c and v):
            messagebox.showinfo('Ввод', 'Заполните все поля')
            return
        pivot = report_pivot(df, r, c, v, agg)

        tree.delete(*tree.get_children())
        tree['columns'] = pivot.columns.tolist()
        for col in pivot.columns:
            tree.heading(col, text=str(col))
            tree.column(col, width=100, anchor=tk.CENTER)
        for idx, row in pivot.iterrows():
            tree.insert('', tk.END, values=[idx] + list(row))

        win.pivot_df = pivot

    def export_csv():
        if not hasattr(win, 'pivot_df'):
            messagebox.showinfo('Экспорт', 'Сначала сформируйте отчёт')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv',
                                            filetypes=[('CSV', '*.csv')])
        if path:
            win.pivot_df.to_csv(path)
            messagebox.showinfo('Экспорт', f'Сохранено: {path}')

    ttk.Button(ctl, text='Сформировать', command=run_report).grid(row=2, column=0, columnspan=6, pady=5)
    ttk.Button(ctl, text='Экспорт CSV', command=export_csv).grid(row=3, column=0, columnspan=6)
