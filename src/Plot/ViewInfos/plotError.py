from typing import Tuple
import customtkinter as ctk

class plotErrorPopup(ctk.CTkToplevel):
    instance = None
    @classmethod
    def open(msg:str):
        pass
    def __init__(self, *args, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.title("Error!")
        