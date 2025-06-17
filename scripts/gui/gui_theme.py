"""
gui_theme.py
============
apply_theme(root, cfg) — единая точка смены шрифта и базовых цветов.
Работает сразу для открытых окон; текст не "пропадает".
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, font as tkfont
from configparser import ConfigParser


# ---------- утилита -------------------------------------------------------
def _set_alias(alias: str, family: str, size: int) -> None:
    """Меняет системный alias-шрифт, если он существует."""
    try:
        tkfont.nametofont(alias).configure(family=family, size=size)
    except tk.TclError:
        pass


# ---------- главная функция ----------------------------------------------
def apply_theme(root: tk.Misc, cfg: ConfigParser) -> None:
    fam = cfg["GUI"].get("font_family", "Segoe UI")
    sz  = cfg["GUI"].getint("font_size", 11)
    fg  = cfg["GUI"].get("base_fg", "#000000")
    bg  = cfg["GUI"].get("base_bg", "#F0F0F0")

    # шрифты
    _set_alias("TkDefaultFont", fam, sz)
    _set_alias("TkTextFont",    fam, sz)   # alias для текста на кнопках (Windows)
    _set_alias("TkHeadingFont", fam, sz)

    style = ttk.Style(root)
    style.theme_use("clam")                # предсказуемый базовый стиль

    # фон приложения
    root.configure(background=bg)
    style.configure("TFrame", background=bg)

    # заголовки / подписи
    style.configure("TLabel", background=bg, foreground=fg)

    # Treeview
    style.configure("Treeview", background=bg, fieldbackground=bg, foreground=fg)
    style.configure("Treeview.Heading", background=bg, foreground=fg)

    # Кнопки
    style.configure(
        "TButton",
        background=bg,
        foreground=fg,
        relief="raised",
        padding=6,
        borderwidth=1,
    )
    style.map(
        "TButton",
        foreground=[
            ("disabled", fg), ("pressed", fg),
            ("active", fg), ("!disabled", fg)
        ],
        background=[
            ("disabled", bg), ("pressed", bg),
            ("active", bg), ("!disabled", bg)
        ],
        relief=[("pressed", "sunken"), ("!pressed", "raised")],
    )

    # перекрасить уже открытые дочерние окна
    for w in root.winfo_children():
        if isinstance(w, (tk.Tk, tk.Toplevel, ttk.Frame)):
            w.configure(background=bg)
