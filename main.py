"""
Entry point for the Python Image Editor.

Keep this file minimal — all application logic lives in the packages below:

  config.py          ← app-wide constants
  core/              ← ImageModel, UndoStack, custom exceptions
  operations/        ← ImageOperation ABC, filters, transforms
  services/          ← image I/O (load / save / resize)
  ui/                ← AppWindow controller, toolbar, canvas, dialogs
"""

import tkinter as tk

from ui.app_window import AppWindow


def main() -> None:
    root = tk.Tk()
    AppWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

