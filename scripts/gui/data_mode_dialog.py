"""
Окно выбора источника данных + генерация синтетических.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from scripts.app_state import mode, DataMode
from scripts.generator_synth import SynthParams, generate

def open_data_mode_dialog(root: tk.Tk) -> None:
    dlg = tk.Toplevel(root)
    dlg.title("Источник данных")
    dlg.grab_set()
    dlg.resizable(False, False)

    choice = tk.StringVar(value="REAL" if mode is DataMode.REAL else "SYNTH")

    ttk.Radiobutton(dlg, text="Реальные (Bank Marketing)",
                    variable=choice, value="REAL").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Radiobutton(dlg, text="Синтетические", variable=choice,
                    value="SYNTH").grid(row=1, column=0, sticky="w", padx=10)

    # --- блок настроек синтетики ----------------------------------------- #
    frame = ttk.LabelFrame(dlg, text="Параметры синтетики")
    frame.grid(row=2, column=0, padx=10, pady=8, sticky="ew")

    var_n   = tk.IntVar(value=1000)
    var_seed = tk.IntVar(value=42)

    ttk.Label(frame, text="Число клиентов").grid(row=0, column=0, sticky="w")
    ttk.Entry(frame, textvariable=var_n, width=10).grid(row=0, column=1, padx=5)
    ttk.Label(frame, text="Seed").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=var_seed, width=10).grid(row=1, column=1, padx=5)

    # включать/выключать блок
    def toggle_params(*_):
        state = "normal" if choice.get() == "SYNTH" else "disabled"
        for child in frame.winfo_children():
            child.configure(state=state)
    choice.trace_add("write", toggle_params)
    toggle_params()

    def ok():
        from scripts import app_state  # локальный импорт, чтобы изменить global variable
        app_state.mode = DataMode.REAL if choice.get() == "REAL" else DataMode.SYNTH
        if app_state.mode is DataMode.SYNTH:
            generate(SynthParams(n_clients=var_n.get(), seed=var_seed.get()))
        dlg.destroy()
        messagebox.showinfo("Источник данных", f"Режим установлен: {app_state.mode.name}\n"
                                               "Закройте и откройте таблицы/отчёты заново.")

    ttk.Button(dlg, text="Принять", command=ok).grid(row=3, column=0, pady=8)
