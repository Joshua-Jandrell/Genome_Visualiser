from Plot.OptionCards import PlotOptionCard, OptionCard
from Plot.ViewInfos import MutFreqView
from typing import Tuple

class MutFreqOptionCard(PlotOptionCard):
    """
    A plot option card specifically used to optionally plot the frequency of a nucleotide mutating in each position.
    """
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        # Stupidly long list of constructor arguments (may be shortened in future)
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Get the dataset menu frame so that it can be put onto the card
        data_select_menu = self.get_dataset_menu_frame()
        
        # Put dataset menu onto the card using grid manager
        data_select_menu.grid(row = 0, column=0,padx=5,pady=5)       