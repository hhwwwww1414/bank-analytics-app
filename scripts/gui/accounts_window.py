"""
accounts_window.py  – полноценный CRUD для справочника «Счета»
(функциональный стиль; аналогичен clients_window.py)
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd

from scripts.data_management import (
    load_accounts, save_accounts, load_clients
)

# ────────────────────────────────────────────────────────────────────────────
def refresh_tree(tree: ttk.Treeview, df: pd.DataFrame) -> None:
    tree.delete(*tree.get_children())
    for _, row in df.iterrows():
        tree.insert("", tk.END, iid=row["account_id"], values=list(row))

def add_account(tree: ttk.Treeview) -> None:
    df_acc = load_accounts()
    df_cli = load_clients()
    try:
        cid = int(simpledialog.askinteger("Клиент", "client_id:", parent=tree))
        if cid not in df_cli["client_id"].values:
            messagebox.showerror("Ошибка", "Такого клиента нет")
            return
        acc_type = simpledialog.askstring("Тип", "Дебетовый / Кредитный:", parent=tree)
        balance = float(simpledialog.askfloat("Баланс", "Сумма (€):", parent=tree))
    except (TypeError, ValueError):
        return
    new_id = df_acc["account_id"].max() + 1
    new_row = {
        "account_id": new_id,
        "client_id": cid,
        "account_type": acc_type,
        "balance": balance,
        "currency": "EUR",
        "open_date": pd.Timestamp.today().floor("D"),
    }
    df_acc = pd.concat([df_acc, pd.DataFrame([new_row])], ignore_index=True)
    save_accounts(df_acc)
    refresh_tree(tree, df_acc)

def delete_selected(tree: ttk.Treeview) -> None:
    ids = [int(i) for i in tree.selection()]
    if not ids:
        return
    if not messagebox.askyesno("Удаление", f"Удалить {len(ids)} счёт(а)?"):
        return
    df = load_accounts()
    df = df[~df["account_id"].isin(ids)].reset_index(drop=True)
    save_accounts(df)
    refresh_tree(tree, df)

def edit_selected(tree: ttk.Treeview) -> None:
    sel = tree.selection()
    if len(sel) != 1:
        messagebox.showinfo("Редактирование", "Выберите один счёт")
        return
    aid = int(sel[0])
    df = load_accounts()
    row = df.loc[df["account_id"] == aid].squeeze()
    try:
        new_balance = float(simpledialog.askfloat(
            "Баланс", "Новый баланс (€):", initialvalue=row["balance"], parent=tree))
    except (TypeError, ValueError):
        return
    df.loc[df["account_id"] == aid, "balance"] = new_balance
    save_accounts(df)
    refresh_tree(tree, df)

# ────────────────────────────────────────────────────────────────────────────
def open_accounts_window(parent: tk.Tk | tk.Toplevel | None = None) -> None:
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Справочник счетов")
    win.geometry("900x450")

    df = load_accounts()

    columns = df.columns.tolist()
    tree = ttk.Treeview(win, columns=columns, show="headings", height=16)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor=tk.CENTER)
    vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    vsb.place(in_=tree, relx=1.0, rely=0, relheight=1.0)
    tree.configure(yscrollcommand=vsb.set)

    refresh_tree(tree, df)

    btns = ttk.Frame(win)
    btns.pack(fill=tk.X, pady=5)
    ttk.Button(btns, text="➕ Добавить", command=lambda: add_account(tree)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btns, text="✏️  Редактировать", command=lambda: edit_selected(tree)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btns, text="🗑 Удалить", command=lambda: delete_selected(tree)).pack(side=tk.LEFT, padx=5)
