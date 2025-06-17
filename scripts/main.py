# work/scripts/main.py
import tkinter as tk
from library.common_funcs import read_config
from scripts.gui.main_window import create_main_window
from scripts.gui.gui_theme import apply_theme


def main() -> None:
    cfg = read_config()

    root = tk.Tk()
    root.geometry("900x600+100+100")     # ← СРАЗУ после создания!
    apply_theme(root, cfg)

    try:
        create_main_window(root, cfg)
        root.mainloop()
    except Exception as exc:
        # покажем ошибку в консоли и во всплывающем окне
        import traceback, tkinter.messagebox as mb
        traceback.print_exc()
        mb.showerror("Unhandled error", str(exc))
        root.destroy()


if __name__ == "__main__":
    main()
