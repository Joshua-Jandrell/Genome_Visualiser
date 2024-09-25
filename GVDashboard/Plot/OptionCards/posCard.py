from Plot.OptionCards import PlotOptionCard, PlotOptionCtrl, OptionCard
from Plot.ViewInfos import VarPosView
from typing import Tuple

class PosOptionCard(PlotOptionCard):
    """
    A plot option card specifically used to optionally plot zygosity data
    """
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
    #def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        # Stupidly long list of constructor arguments (may be shortened in future)
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Get the dataset menu frame so that it can be put onto the card
        data_select_menu = self.get_dataset_menu_frame()
        # Put dataset menu onto the card using grid manager
        data_select_menu.grid(row = 0, column=0,padx=5,pady=5)

    #### TODO: Maybe we can toggle homo or hetero on??? We shall ask in usability tests tho

# Option control specifcally for position "heatmap" info
class PosOptionCtrl(PlotOptionCtrl):
    def make_option_card(self) -> OptionCard:
        # op = PosOptionCard(master=self.option_list, # The UI container the option card goes into (should be an option list)
        #                    option_ctrl=self, # The option control that created this option card (should be this option control)
        #                    option_key="Position" # The `option_key` is essentially just the text displayed on the option card label
        #                    )
        op = super().make_option_card()
        op.set_value(VarPosView())
        return op
        