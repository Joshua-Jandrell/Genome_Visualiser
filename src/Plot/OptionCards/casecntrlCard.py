import customtkinter as ctk
from Plot.OptionCards import PlotOptionCard, OptionCard
from typing import Tuple

class CasecntrlOptionCard(PlotOptionCard):
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 190, height: int = 70, corner_radius: int | str | None = 10, border_width: int | str | None = 1, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = "#FFDBDB", border_color: str | Tuple[str] | None = "#A80003", background_corner_colors: Tuple[str | Tuple[str]] | None = ("#A80003", "#DF4D55", "#DF4D55", "#A80003"), overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.t = ctk.CTkLabel(self.content ,text= "This view indicates which \"case\" samples are being compared to known \"control\" samples.", wraplength= 290)
        self.t.pack()