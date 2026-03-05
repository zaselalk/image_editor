"""Image display canvas widget."""

from __future__ import annotations

import tkinter as tk
from PIL import Image, ImageTk

import config
import services


class ImageCanvas(tk.Frame):
    """
    A dark-background frame that displays a PIL image, scaled to fit.

    The widget owns the ``PhotoImage`` reference to prevent GC collection.
    """

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, bg=config.CANVAS_BG, **kwargs)
        self._label = tk.Label(self, bg=config.CANVAS_BG)
        self._label.pack(expand=True)
        self._photo: ImageTk.PhotoImage | None = None   # GC anchor

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def show(self, image: Image.Image | None) -> None:
        """Render *image* scaled to the current widget size."""
        if image is None:
            self._label.config(image="")
            self._photo = None
            return

        w = max(self.winfo_width(), 600)
        h = max(self.winfo_height(), 400)

        display = services.resize_for_display(image, w, h)
        self._photo = ImageTk.PhotoImage(display)
        self._label.config(image=self._photo)

    def clear(self) -> None:
        self.show(None)
