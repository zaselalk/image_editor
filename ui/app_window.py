"""
Main application window.

Acts as the **Controller** in the MVC pattern:
  - Owns a single ``ImageModel`` (the Model).
  - Composes UI widgets (the View) and wires them together.
  - Handles user commands and delegates to services / operations.
"""

from __future__ import annotations

import tkinter as tk

import config
import services
from core import ImageModel, NoImageError
from operations import OperationCommand, FILTER_REGISTRY
from operations.base import ImageOperation
from ui.canvas import ImageCanvas
from ui.toolbar import Toolbar
from ui.status_bar import StatusBar
import ui.dialogs as dialogs


class AppWindow:
    """Root application window and controller."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._model = ImageModel()

        self._setup_window()
        self._build_ui()
        self._wire_model()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup_window(self) -> None:
        self._root.title(config.APP_TITLE)
        self._root.geometry(config.APP_GEOMETRY)
        self._root.minsize(640, 480)

    def _build_ui(self) -> None:
        # Toolbar (passes *self* as the controller)
        self._toolbar = Toolbar(self._root, controller=self)
        self._toolbar.pack(side=tk.TOP, fill=tk.X)

        # Image canvas
        self._canvas = ImageCanvas(self._root)
        self._canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Status bar
        self._status = StatusBar(self._root)
        self._status.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind resize so the display scales with the window
        self._root.bind("<Configure>", self._on_resize)

    def _wire_model(self) -> None:
        """Observe model changes to keep the view in sync."""
        self._model.add_observer(self._on_model_changed)

    # ------------------------------------------------------------------
    # Controller actions (called by toolbar / keyboard shortcuts)
    # ------------------------------------------------------------------

    def open_image(self) -> None:
        path = dialogs.ask_open_image()
        if not path:
            return
        try:
            image = services.load(path)
            self._model.load(path, image)
            self._toolbar.set_image_loaded(True)
            self._status.set(f"Opened: {path}  ({image.width}×{image.height})")
        except Exception as exc:
            dialogs.show_error("Open Error", str(exc))

    def save_image(self) -> None:
        if not self._model.has_image:
            return
        path = dialogs.ask_save_image()
        if not path:
            return
        try:
            services.save(self._model.image, path)
            self._status.set(f"Saved: {path}")
        except Exception as exc:
            dialogs.show_error("Save Error", str(exc))

    def apply_filter(self, name: str) -> None:
        """Apply a named filter from the registry."""
        if not self._model.has_image:
            return
        operation_cls = FILTER_REGISTRY.get(name)
        if operation_cls is None:
            return
        self._run_operation(operation_cls())

    def apply_transform(self, operation: ImageOperation) -> None:
        if not self._model.has_image:
            return
        self._run_operation(operation)

    def undo(self) -> None:
        label = self._model.undo()
        if label:
            self._status.set(f"Undone: {label}")
        else:
            self._status.set("Nothing to undo.")
        self._refresh_undo_redo()

    def redo(self) -> None:
        label = self._model.redo()
        if label:
            self._status.set(f"Redone: {label}")
        else:
            self._status.set("Nothing to redo.")
        self._refresh_undo_redo()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_operation(self, operation: ImageOperation) -> None:
        try:
            command = OperationCommand(self._model, operation)
            self._model.apply(command)
            self._status.set(f"Applied: {operation.name}")
        except NoImageError:
            dialogs.show_warning("No Image", "Please open an image first.")
        except Exception as exc:
            dialogs.show_error("Operation Error", str(exc))
        self._refresh_undo_redo()

    def _refresh_undo_redo(self) -> None:
        self._toolbar.refresh_undo_redo(
            self._model.history.can_undo,
            self._model.history.can_redo,
        )

    # ------------------------------------------------------------------
    # Model observer
    # ------------------------------------------------------------------

    def _on_model_changed(self) -> None:
        """Called whenever the model image is updated."""
        self._canvas.show(self._model.image)
        self._refresh_undo_redo()

    # ------------------------------------------------------------------
    # Window events
    # ------------------------------------------------------------------

    def _on_resize(self, event: tk.Event) -> None:
        self._root.after(80, lambda: self._canvas.show(self._model.image))
