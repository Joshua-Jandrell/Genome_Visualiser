import customtkinter as ctk
from Plot.OptionCards import PlotOptionCard, OptionCard
from Plot.ViewInfos import MutFreqView
from typing import Tuple

class MutFreqOptionCard(PlotOptionCard):
    """
    A plot option card specifically used to optionally plot the frequency of a nucleotide mutating in each position.
    """
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 70, corner_radius: int | str | None = 10, border_width: int | str | None = 1, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = "#E0FFFF", border_color: str | Tuple[str] | None = "#81C4E7", background_corner_colors: Tuple[str | Tuple[str]] | None = ("#81C4E7", "#F94902", "#81C4E7", "#F94902"), overwrite_preferred_drawing_method: str | None = None, **kwargs):
        # Stupidly long list of constructor arguments (may be shortened in future)
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.t = ctk.CTkLabel(self.content ,text= "This view indicates the probability that a mutation has occured at that position, across the selected set.", wraplength= 250)
        self.t.pack()