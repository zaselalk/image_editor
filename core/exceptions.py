"""Custom exceptions for the image editor."""


class ImageEditorError(Exception):
    """Base exception for all image editor errors."""


class ImageLoadError(ImageEditorError):
    """Raised when an image cannot be loaded."""


class ImageSaveError(ImageEditorError):
    """Raised when an image cannot be saved."""


class NoImageError(ImageEditorError):
    """Raised when an operation is attempted without a loaded image."""
