"""ImageModel — central state holder for the loaded image and its edit history."""

from __future__ import annotations
from typing import Callable

from PIL import Image

from core.history import UndoStack, Command
from core.exceptions import NoImageError
import config


class ImageModel:
    """
    Holds the authoritative (full-resolution) PIL image and delegates
    all mutations through the UndoStack so every change is reversible.

    Observers are notified via a simple callback list whenever the
    active image changes.
    """

    def __init__(self) -> None:
        self._image: Image.Image | None = None
        self._file_path: str | None = None
        self._history: UndoStack = UndoStack(config.MAX_UNDO_STEPS)
        self._on_change_callbacks: list[Callable[[], None]] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def image(self) -> Image.Image | None:
        return self._image

    @image.setter
    def image(self, value: Image.Image | None) -> None:
        self._image = value
        self._notify()

    @property
    def file_path(self) -> str | None:
        return self._file_path

    @property
    def history(self) -> UndoStack:
        return self._history

    @property
    def has_image(self) -> bool:
        return self._image is not None

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def load(self, path: str, image: Image.Image) -> None:
        """Replace the current image with a freshly-loaded one and clear history."""
        self._file_path = path
        self._image = image
        self._history.clear()
        self._notify()

    def apply(self, command: Command) -> None:
        """Execute a command through the history stack and update the image."""
        if not self.has_image:
            raise NoImageError("No image is currently loaded.")
        self._history.push(command)
        # The command is responsible for updating self._image via callback; see
        # OperationCommand below for the canonical implementation.
        self._notify()

    def undo(self) -> str | None:
        """Undo the last command. Returns the label of the undone command or None."""
        command = self._history.undo()
        if command:
            self._notify()
            return command.label
        return None

    def redo(self) -> str | None:
        """Redo the last undone command. Returns the label or None."""
        command = self._history.redo()
        if command:
            self._notify()
            return command.label
        return None

    # ------------------------------------------------------------------
    # Observer helpers
    # ------------------------------------------------------------------

    def add_observer(self, callback: Callable[[], None]) -> None:
        """Register a no-arg callback that fires whenever the image changes."""
        self._on_change_callbacks.append(callback)

    def _notify(self) -> None:
        for cb in self._on_change_callbacks:
            cb()
