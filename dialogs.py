"""
Legacy compatibility shim.

New code should import from ``ui.dialogs`` directly.
"""

from ui.dialogs import ask_open_image, ask_save_image, show_info, show_error, show_warning, ask_yes_no

__all__ = ["ask_open_image", "ask_save_image", "show_info", "show_error", "show_warning", "ask_yes_no"]
