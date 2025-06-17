"""
settings_window.py – изменённый вариант: список системных шрифтов,
пресеты цветов и немедленное применение.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from pathlib import Path
from configparser import ConfigParser

from scripts.gui.gui_theme import apply_theme

CFG_PATH = Path(__file__).parent.parent / "app_config.ini"

PRESETS = {
    "light":  ("#000000", "#F0F0F0"),
    "dark":   ("#EAEAEA", "#2B2B2B"),
    "blue":   ("#FFFFFF", "#3B4B5B"),
    "olive":  ("#000000", "#D7E1C5"),
    "maroon": ("#FFFFFF", "#702632"),
}


def _load_cfg() -> ConfigParser:
    c = ConfigParser()
    c.read(CFG_PATH, encoding="utf-8")
    return c


def _save_cfg(c: ConfigParser) -> None:
    with CFG_PATH.open("w", encoding="utf-8") as f:
        c.write(f)


# ──────────────────────────────────────────────────────────────────────────
def open_settings_window(root: tk.Tk) -> None:
    win = tk.Toplevel(root)
    win.title("Настройки")
    win.geometry("460x330")
    win.resizable(False, False)

    cfg = _load_cfg()

    # ---------- GUI ------------------------------------------------------
    frm = ttk.LabelFrame(win, text="GUI")
    frm.pack(fill=tk.X, padx=10, pady=8)

    fonts_available = sorted(set(tkfont.families()))
    var_font = tk.StringVar(value=cfg["GUI"].get("font_family", "Arial"))
    var_size = tk.IntVar(value=cfg["GUI"].getint("font_size", 11))
    var_fg   = tk.StringVar(value=cfg["GUI"].get("base_fg",  "#000000"))
    var_bg   = tk.StringVar(value=cfg["GUI"].get("base_bg",  "#F0F0F0"))

    ttk.Label(frm, text="Шрифт").grid(row=0, column=0, sticky="w", padx=5, pady=3)
    ttk.Combobox(frm, textvariable=var_font, values=fonts_available, width=25
                 ).grid(row=0, column=1, padx=5)

    ttk.Label(frm, text="Размер").grid(row=1, column=0, sticky="w", padx=5, pady=3)
    ttk.Spinbox(frm, from_=8, to=22, textvariable=var_size, width=6
                ).grid(row=1, column=1, padx=5)

    ttk.Label(frm, text="Тема").grid(row=2, column=0, sticky="w", padx=5, pady=3)
    var_preset = tk.StringVar()
    cb = ttk.Combobox(frm, textvariable=var_preset,
                      values=list(PRESETS.keys()), state="readonly", width=12)
    cb.grid(row=2, column=1, padx=5)

    def on_choose(_):
        fg, bg = PRESETS[var_preset.get()]
        var_fg.set(fg)
        var_bg.set(bg)
    cb.bind("<<ComboboxSelected>>", on_choose)

    frm.columnconfigure(1, weight=1)

    # ---------- ПУТИ -----------------------------------------------------
    paths = ttk.LabelFrame(win, text="Пути")
    paths.pack(fill=tk.X, padx=10, pady=8)

    var_data = tk.StringVar(value=cfg["PATHS"].get("data_dir", "data"))
    var_graph = tk.StringVar(value=cfg["PATHS"].get("graphics_dir", "graphics"))
    var_out = tk.StringVar(value=cfg["PATHS"].get("output_dir", "output"))

    def _row(lbl, var, r):
        ttk.Label(paths, text=lbl).grid(row=r, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(paths, textvariable=var).grid(row=r, column=1, padx=5, sticky="we")
    _row("Данные",   var_data, 0)
    _row("Графика",  var_graph, 1)
    _row("Отчёты",   var_out, 2)
    paths.columnconfigure(1, weight=1)

    # ---------- Сохранить -----------------------------------------------
    def save_apply():
        cfg["GUI"]["font_family"] = var_font.get()
        cfg["GUI"]["font_size"]   = str(var_size.get())
        cfg["GUI"]["base_fg"]     = var_fg.get()
        cfg["GUI"]["base_bg"]     = var_bg.get()

        cfg["PATHS"]["data_dir"]      = var_data.get()
        cfg["PATHS"]["graphics_dir"]  = var_graph.get()
        cfg["PATHS"]["output_dir"]    = var_out.get()

        _save_cfg(cfg)
        apply_theme(root, cfg)                 # применяем ко ВСЕМ открытым окнам
        messagebox.showinfo("Настройки", "Сохранено и применено")
        win.destroy()

    ttk.Button(win, text="Сохранить", command=save_apply).pack(pady=10)
