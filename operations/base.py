"""
Abstract base for all image operations.

Each concrete operation:
  1. Subclasses ``ImageOperation`` and implements ``apply()``.
  2. Is wrapped by ``OperationCommand`` to integrate with the undo stack.
"""

from __future__ import annotations
from abc import ABC, abstractmethod

from PIL import Image

from core.history import Command


class ImageOperation(ABC):
    """
    A stateless, pure transformation on a PIL Image.

    ``apply()`` must be a pure function — it should not mutate the
    input and must return a new Image object.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Short human-readable name (shown in status bar / menus)."""

    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image:
        """Return a transformed copy of *image*."""


class OperationCommand(Command):
    """
    Bridges an ``ImageOperation`` with the ``UndoStack``.

    Keeps a snapshot of the image *before* the operation so it can
    be restored verbatim on undo.
    """

    def __init__(self, model, operation: ImageOperation) -> None:
        # Import here to avoid circular deps at module level
        from core.image_model import ImageModel  # noqa: F401
        self._model = model          # ImageModel instance
        self._operation = operation
        self._before: Image.Image | None = None
        self._after: Image.Image | None = None

    # ------------------------------------------------------------------
    # Command interface
    # ------------------------------------------------------------------

    def execute(self) -> None:
        self._before = self._model.image.copy()
        self._after = self._operation.apply(self._model.image)
        self._model._image = self._after   # Direct write; notified by ImageModel.apply()

    def undo(self) -> None:
        self._model._image = self._before

    @property
    def label(self) -> str:
        return self._operation.name
