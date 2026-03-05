"""
Legacy compatibility shim.

New code should import from ``services.image_io`` directly.
"""

from services.image_io import load as load_image, save as _save, resize_for_display


def save_image(image, path, format=None):
    _save(image, path, fmt=format)
