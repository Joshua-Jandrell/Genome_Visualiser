# A simple dropdown menu widget
from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk

class DropDown(ctk.CTkOptionMenu):
    def __init__(self, master: Any, text:str="menu", width: int = 140, height: int = 28, corner_radius: int | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, button_color: str | Tuple[str, str] | None = None, button_hover_color: str | Tuple[str, str] | None = None, text_color: str | Tuple[str, str] | None = None, text_color_disabled: str | Tuple[str, str] | None = None, dropdown_fg_color: str | Tuple[str, str] | None = None, dropdown_hover_color: str | Tuple[str, str] | None = None, dropdown_text_color: str | Tuple[str, str] | None = None, font: tuple | ctk.CTkFont | None = None, dropdown_font: tuple | ctk.CTkFont | None = None, values: list | None = None, variable: ctk.Variable | None = None, state: str = NORMAL, hover: bool = True, command: Callable[[str], Any] | None = None, dynamic_resizing: bool = True, anchor: str = "w", **kwargs):
        # Set true command to be called
        # NOTE This must be done before the base constructor is called
        self._true_command = command
        super().__init__(master, width, height, corner_radius, bg_color, fg_color, button_color, button_hover_color, text_color, text_color_disabled, dropdown_fg_color, dropdown_hover_color, dropdown_text_color, font, dropdown_font, values, variable, state, hover, command, dynamic_resizing, anchor, **kwargs)
        self.menu_text = text

        """The external command that will be called when the dropdown is updated"""
        # Configure the command from the dropdown so that it can be intercepted 
        self._command=self._on_value_change

        self._text_label.configure(text=self.menu_text)
        #self.configure(command=command)

    def _on_value_change(self, event):
        self._text_label.configure(text=self.menu_text)
        # Now call the true command
        self._true_command(event)

    # Overwrite configure so that command remains intercepted
    def configure(self, require_redraw=False, **kwargs):
        super().configure(require_redraw, **kwargs)
        if self._command != self._on_value_change:
            self._true_command = self._command
            self._command=self._on_value_change
