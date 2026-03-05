"""Status bar widget."""

import tkinter as tk


class StatusBar(tk.Label):
    """A simple sunken label at the bottom of the window."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(
            parent,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            **kwargs,
        )

    def set(self, message: str) -> None:
        self.config(text=message)

    def clear(self) -> None:
        self.config(text="Ready")
