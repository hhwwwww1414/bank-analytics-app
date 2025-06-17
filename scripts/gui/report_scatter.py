"""report_scatter.py

Отчёт 7. Диаграмма рассеяния.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from scripts.data_management import load_clients
from scripts.reporting import report_scatter
from scripts.gui.gui_helpers import show_matplotlib


def open_report_scatter(parent: tk.Tk | tk.Toplevel | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title('Отчёт 7. Рассеяние')
    win.geometry('900x600')

    df = load_clients()
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(exclude='number').columns.tolist()

    ctl = ttk.Frame(win)
    ctl.pack(fill=tk.X, pady=5)

    var_x = tk.StringVar()
    var_y = tk.StringVar()
    var_cat = tk.StringVar()

    ttk.Label(ctl, text='X').grid(row=0, column=0, padx=5, sticky='w')
    ttk.Combobox(ctl, textvariable=var_x, values=num_cols).grid(row=0, column=1, padx=5)
    ttk.Label(ctl, text='Y').grid(row=0, column=2, padx=5, sticky='w')
    ttk.Combobox(ctl, textvariable=var_y, values=num_cols).grid(row=0, column=3, padx=5)
    ttk.Label(ctl, text='Категория').grid(row=0, column=4, padx=5, sticky='w')
    ttk.Combobox(ctl, textvariable=var_cat, values=cat_cols).grid(row=0, column=5, padx=5)

    plot_frame = ttk.Frame(win)
    plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_report():
        x, y, c = var_x.get(), var_y.get(), var_cat.get()
        if not x or not y or not c:
            messagebox.showinfo('Ввод', 'Выберите x, y и категорию')
            return
        fig = report_scatter(df, x, y, c)
        win.fig = fig
        show_matplotlib(fig, plot_frame)

    def save_png():
        if not hasattr(win, 'fig'):
            messagebox.showinfo('Сохранение', 'Сначала постройте график')
            return
        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png')])
        if path:
            win.fig.savefig(path)
            messagebox.showinfo('Сохранение', f'Сохранено: {path}')

    ttk.Button(ctl, text='Построить', command=run_report).grid(row=1, column=0, columnspan=3, pady=5)
    ttk.Button(ctl, text='Сохранить PNG', command=save_png).grid(row=1, column=3, columnspan=3, pady=5)
