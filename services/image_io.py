"""
Image I/O service.

Responsible solely for disk operations (load/save) and display-scaling.
All PIL details are confined here so the rest of the app stays decoupled
from the underlying image library.
"""

from __future__ import annotations

from PIL import Image

from core.exceptions import ImageLoadError, ImageSaveError


def _resampler():
    try:
        return Image.Resampling.LANCZOS
    except AttributeError:                # Pillow < 9
        return Image.LANCZOS


def load(path: str) -> Image.Image:
    """Open and return a PIL Image. Raises ``ImageLoadError`` on failure."""
    try:
        img = Image.open(path)
        img.load()   # Force decode so errors surface here, not later
        return img
    except Exception as exc:
        raise ImageLoadError(f"Cannot open '{path}': {exc}") from exc


def save(image: Image.Image, path: str, fmt: str | None = None) -> None:
    """
    Save *image* to *path*, inferring format from the extension when *fmt*
    is omitted. Raises ``ImageSaveError`` on failure.
    """
    try:
        # JPEG requires RGB — silently convert if needed
        if path.lower().endswith((".jpg", ".jpeg")) and image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        image.save(path, format=fmt)
    except Exception as exc:
        raise ImageSaveError(f"Cannot save to '{path}': {exc}") from exc


def resize_for_display(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    """Return a downscaled copy that fits within *max_width* × *max_height*."""
    if image is None:
        raise ValueError("image must not be None")

    w, h = image.size
    if w == 0 or h == 0:
        return image

    ratio = min(max_width / w, max_height / h, 1.0)   # Never upscale
    new_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
    return image.resize(new_size, _resampler())
