import customtkinter as ctk
from Plot.OptionCards import PlotOptionCard, OptionCard
from Plot.ViewInfos import VarPosView
from typing import Tuple

class PosOptionCard(PlotOptionCard):
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 100, corner_radius: int | str | None = 10, border_width: int | str | None = 1, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = "#F6D9FC", border_color: str | Tuple[str] | None = '#D43480', background_corner_colors: Tuple[str | Tuple[str]] | None = ('#1F00A2', '#E8C80A', '#D36F27', '#8500A4'), overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.t = ctk.CTkLabel(self.content ,text= "This gradient indicates the position of the sequence section being displayed relative to the selected range.", wraplength= 280)
        self.t.pack()