"""gui_helpers.py

Вспомогательные функции для вставки matplotlib в Tkinter.
"""
from __future__ import annotations

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def show_matplotlib(fig, container: tk.Widget) -> FigureCanvasTkAgg:
    """Embed figure into container and return canvas."""
    for child in container.winfo_children():
        child.destroy()
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.pack(fill=tk.BOTH, expand=True)
    return canvas
