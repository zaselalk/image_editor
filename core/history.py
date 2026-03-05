"""Command pattern implementation for undo/redo history."""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque

import config


class Command(ABC):
    """Abstract base class for reversible operations."""

    @abstractmethod
    def execute(self):
        """Apply the operation and return the new image."""

    @abstractmethod
    def undo(self):
        """Revert to the state before the operation and return the previous image."""

    @property
    @abstractmethod
    def label(self) -> str:
        """Human-readable description shown in the status bar."""


class UndoStack:
    """Manages undo/redo history with a configurable maximum depth."""

    def __init__(self, max_steps: int = config.MAX_UNDO_STEPS) -> None:
        self._undo: deque[Command] = deque(maxlen=max_steps)
        self._redo: deque[Command] = deque(maxlen=max_steps)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def push(self, command: Command) -> None:
        """Execute a command and push it onto the undo stack."""
        command.execute()
        self._undo.append(command)
        self._redo.clear()  # New action invalidates redo history

    def undo(self) -> Command | None:
        """Undo the last command. Returns the command or None if stack is empty."""
        if not self._undo:
            return None
        command = self._undo.pop()
        command.undo()
        self._redo.append(command)
        return command

    def redo(self) -> Command | None:
        """Redo the last undone command. Returns the command or None."""
        if not self._redo:
            return None
        command = self._redo.pop()
        command.execute()
        self._undo.append(command)
        return command

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)

    @property
    def undo_label(self) -> str:
        return self._undo[-1].label if self._undo else ""

    @property
    def redo_label(self) -> str:
        return self._redo[-1].label if self._redo else ""
