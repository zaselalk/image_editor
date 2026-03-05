"""Toolbar widget with buttons and a Filters drop-down menu."""

from __future__ import annotations
from typing import Callable

import tkinter as tk

import config
from operations import FILTER_REGISTRY, RotateCW, RotateCCW, FlipHorizontal, FlipVertical


class Toolbar(tk.Frame):
    """
    The top toolbar.

    All button callbacks are injected by the controller (``app_window.py``)
    so this widget has zero business logic.
    """

    def __init__(self, parent: tk.Widget, controller, **kwargs) -> None:
        super().__init__(parent, bg=config.TOOLBAR_BG, height=50, **kwargs)
        self._controller = controller
        self._image_buttons: list[tk.Widget] = []
        self._build()

    # ------------------------------------------------------------------
    # Build UI
    # ------------------------------------------------------------------

    def _build(self) -> None:
        self._btn_open = tk.Button(
            self, text="📂 Open", command=self._controller.open_image,
            bg="#4CAF50", fg="white",
        )
        self._btn_open.pack(side=tk.LEFT, padx=6, pady=8)

        self._btn_save = tk.Button(
            self, text="💾 Save", command=self._controller.save_image,
        )
        self._btn_save.pack(side=tk.LEFT, padx=6, pady=8)

        # Undo / Redo
        self._btn_undo = tk.Button(self, text="↩ Undo", command=self._controller.undo)
        self._btn_undo.pack(side=tk.LEFT, padx=6, pady=8)

        self._btn_redo = tk.Button(self, text="↪ Redo", command=self._controller.redo)
        self._btn_redo.pack(side=tk.LEFT, padx=6, pady=8)

        # Filters drop-down
        self._filter_var = tk.StringVar(value="✨ Filters ▾")
        self._filter_menu_btn = tk.Menubutton(
            self, textvariable=self._filter_var, relief=tk.RAISED,
        )
        filter_menu = tk.Menu(self._filter_menu_btn, tearoff=False)
        for name in FILTER_REGISTRY:
            filter_menu.add_command(
                label=name,
                command=lambda n=name: self._controller.apply_filter(n),
            )
        self._filter_menu_btn["menu"] = filter_menu
        self._filter_menu_btn.pack(side=tk.LEFT, padx=6, pady=8)

        # Transform buttons
        tk.Button(
            self, text="↻", width=2, command=lambda: self._controller.apply_transform(RotateCW()),
        ).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(
            self, text="↺", width=2, command=lambda: self._controller.apply_transform(RotateCCW()),
        ).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(
            self, text="⇔", width=2, command=lambda: self._controller.apply_transform(FlipHorizontal()),
        ).pack(side=tk.LEFT, padx=2, pady=8)
        tk.Button(
            self, text="⇕", width=2, command=lambda: self._controller.apply_transform(FlipVertical()),
        ).pack(side=tk.LEFT, padx=2, pady=8)

        # Collect image-dependent widgets for bulk enable/disable
        self._image_buttons = [
            self._btn_save, self._btn_undo, self._btn_redo, self._filter_menu_btn,
        ]
        self.set_image_loaded(False)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def set_image_loaded(self, loaded: bool) -> None:
        state = tk.NORMAL if loaded else tk.DISABLED
        for widget in self._image_buttons:
            widget.config(state=state)

    def refresh_undo_redo(self, can_undo: bool, can_redo: bool) -> None:
        self._btn_undo.config(state=tk.NORMAL if can_undo else tk.DISABLED)
        self._btn_redo.config(state=tk.NORMAL if can_redo else tk.DISABLED)
