"""Thin wrappers around Tkinter dialog functions."""

import tkinter.filedialog as fd
import tkinter.messagebox as mb

import config


def ask_open_image() -> str | None:
    return fd.askopenfilename(
        title="Select an Image",
        filetypes=config.OPEN_FILETYPES,
    )


def ask_save_image() -> str | None:
    return fd.asksaveasfilename(
        defaultextension=config.DEFAULT_SAVE_EXT,
        filetypes=config.SAVE_FILETYPES,
    )


def show_info(title: str, message: str) -> None:
    mb.showinfo(title, message)


def show_error(title: str, message: str) -> None:
    mb.showerror(title, message)


def show_warning(title: str, message: str) -> None:
    mb.showwarning(title, message)


def ask_yes_no(title: str, message: str) -> bool:
    return mb.askyesno(title, message)
