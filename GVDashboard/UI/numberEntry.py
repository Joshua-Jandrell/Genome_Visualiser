from tkinter.constants import NORMAL
from typing import Any, Tuple
import customtkinter as ctk

class NumberEntry(ctk.CTkEntry):
    """Special entry type that can only hold a numerical value."""
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, text_color: str | Tuple[str, str] | None = None, placeholder_text_color: str | Tuple[str, str] | None = None, textvariable: ctk.Variable | None = None, placeholder_text: str | None = None, font: tuple | ctk.CTkFont | None = None, state: str = ctk.ctk_tk.NORMAL, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, text_color, placeholder_text_color, textvariable, placeholder_text, font, state, **kwargs)

        # Add trace to command to see when 

    # def get()->int:
        
