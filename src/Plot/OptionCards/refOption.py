import customtkinter as ctk
from Plot.OptionCards import PlotOptionCard, OptionCard
from Plot.ViewInfos import RefView
from typing import Tuple

class RefOptionCard(PlotOptionCard):
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 70, corner_radius: int | str | None = 10, border_width: int | str | None = 1, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = "#EBEBEB", border_color: str | Tuple[str] | None = "#666666", background_corner_colors: Tuple[str | Tuple[str]] | None = ("#29E838", "#E829D8", "#E89829", "#2979E8"), overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.t = ctk.CTkLabel(self.content ,text= "This view shows the Reference & Alternate nucleotide sequences at each position.", wraplength= 290)
        self.t.pack()