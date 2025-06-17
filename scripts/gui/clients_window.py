"""
clients_window.py
-----------------
Полноценное CRUD-окно для справочника «Клиенты».
Функциональный стиль, без классов.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd

from scripts.data_management import load_clients, save_clients


# ────────────────────────────────────────────────────────────────────────────
def refresh_tree(tree: ttk.Treeview, df: pd.DataFrame) -> None:
    tree.delete(*tree.get_children())
    for _, row in df.iterrows():
        tree.insert("", tk.END, iid=row["client_id"], values=list(row))


def add_client(tree: ttk.Treeview) -> None:
    df = load_clients()
    try:
        first = simpledialog.askstring("Имя", "Имя клиента:")
        last = simpledialog.askstring("Фамилия", "Фамилия клиента:")
        age = int(simpledialog.askinteger("Возраст", "Возраст:"))
        gender = simpledialog.askstring("Пол", "М / Ж:")
        city = simpledialog.askstring("Город", "Город:")
        income = float(simpledialog.askfloat("Доход", "Годовой доход (€):"))
    except (TypeError, ValueError):
        return
    new_id = df["client_id"].max() + 1
    new_row = {
        "client_id": new_id,
        "last_name": last,
        "first_name": first,
        "age": age,
        "gender": gender,
        "city": city,
        "income": income,
        "reg_date": pd.Timestamp.today().floor("D"),
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_clients(df)
    refresh_tree(tree, df)


def delete_selected(tree: ttk.Treeview) -> None:
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Удаление", "Не выбрана запись")
        return
    if messagebox.askyesno("Подтверждение", "Удалить выбранные записи?"):
        df = load_clients()
        ids = [int(i) for i in sel]
        df = df[~df["client_id"].isin(ids)].reset_index(drop=True)
        save_clients(df)
        refresh_tree(tree, df)


def edit_selected(tree: ttk.Treeview) -> None:
    sel = tree.selection()
    if len(sel) != 1:
        messagebox.showinfo("Редактирование", "Выберите одну запись")
        return
    cid = int(sel[0])
    df = load_clients()
    row = df.loc[df["client_id"] == cid].squeeze()
    new_city = simpledialog.askstring("Город", "Новый город:", initialvalue=row["city"])
    try:
        new_income = float(
            simpledialog.askfloat("Доход", "Новый доход (€):", initialvalue=row["income"])
        )
    except (TypeError, ValueError):
        return
    df.loc[df["client_id"] == cid, ["city", "income"]] = [new_city, new_income]
    save_clients(df)
    refresh_tree(tree, df)


# ────────────────────────────────────────────────────────────────────────────
def open_clients_window(parent: tk.Tk | tk.Toplevel | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Справочник клиентов")
    win.geometry("900x500")

    df = load_clients()

    columns = list(df.columns)
    tree = ttk.Treeview(win, columns=columns, show="headings", height=18)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor=tk.CENTER)

    refresh_tree(tree, df)

    # вертикальный скролл
    vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    vsb.place(in_=tree, relx=1.0, rely=0, relheight=1.0)
    tree.configure(yscrollcommand=vsb.set)

    # панель кнопок
    btns = ttk.Frame(win)
    btns.pack(fill=tk.X, pady=5)

    ttk.Button(btns, text="➕ Добавить", command=lambda: add_client(tree)).pack(
        side=tk.LEFT, padx=5
    )
    ttk.Button(btns, text="✏️  Редактировать", command=lambda: edit_selected(tree)).pack(
        side=tk.LEFT, padx=5
    )
    ttk.Button(btns, text="🗑 Удалить", command=lambda: delete_selected(tree)).pack(
        side=tk.LEFT, padx=5
    )
