# A simple dropdown menu widget
from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk

class DrowDown(ctk.CTkOptionMenu):
    def __init__(self, master: Any, text:str="menu", width: int = 140, height: int = 28, corner_radius: int | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, button_color: str | Tuple[str, str] | None = None, button_hover_color: str | Tuple[str, str] | None = None, text_color: str | Tuple[str, str] | None = None, text_color_disabled: str | Tuple[str, str] | None = None, dropdown_fg_color: str | Tuple[str, str] | None = None, dropdown_hover_color: str | Tuple[str, str] | None = None, dropdown_text_color: str | Tuple[str, str] | None = None, font: tuple | ctk.CTkFont | None = None, dropdown_font: tuple | ctk.CTkFont | None = None, values: list | None = None, variable: ctk.Variable | None = None, state: str = NORMAL, hover: bool = True, command: Callable[[str], Any] | None = None, dynamic_resizing: bool = True, anchor: str = "w", **kwargs):
        super().__init__(master, width, height, corner_radius, bg_color, fg_color, button_color, button_hover_color, text_color, text_color_disabled, dropdown_fg_color, dropdown_hover_color, dropdown_text_color, font, dropdown_font, values, variable, state, hover, command, dynamic_resizing, anchor, **kwargs)
        self.value = variable # set value to be true control variable
        self.menu_text = text
        variable.trace_add('write', self._on_value_change)
        self._text_label.configure(text=self.menu_text)

    def _on_value_change(self, *args):
        self._text_label.configure(text=self.menu_text)
