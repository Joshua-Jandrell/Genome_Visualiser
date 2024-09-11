from Plot.OptionCards import PlotOptionCard, PlotOptionCtrl, OptionCard
from Plot.plotInfo import RefView
from typing import Tuple

class RefOptionCard(PlotOptionCard):
    """
    A plot option card specifically used to optionally plot reference sequence data
    """
    # Useful constants 
    COUNTS_VALUE = 'counts'
    DENSITY_VALUE = 'density'
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
    #def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        # Stupidly long list of constructor arguments (may be shortened in future)
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Get the dataset menu frame so that it can be put onto the card
        data_select_menu = self.get_dataset_menu_frame()
        # Put dataset menu onto the card using grid manager
        data_select_menu.grid(row = 0, column=0,padx=5,pady=5)

        # # Add a segmented to help pick between plotting counts or density 
        # counts_toggle = ctk.CTkSegmentedButton(master=self.content, #NB add all new elements to the content of the panel (not the panel itself)
        #                                        values=[self.COUNTS_VALUE,self.DENSITY_VALUE], # Values that can be selected on segmented button
        #                                        command=self.__on_count_toggle_change # The command to be called when the value is changed: will return the value of the toggle as an argument.
        #                                        )
        
        # # Put toggle in the content grind
        # counts_toggle.grid(row=1, column=0, padx=5, pady=5)
        # # Select default toggle value to counts:
        # counts_toggle.set(self.COUNTS_VALUE)

    # def __on_count_toggle_change(self,value):
    #     """Private method called when the value of the counts toggle is updated."""
    #     assert(isinstance(self.value, RefView)) # Ensure that view info is of type frequency view
    #     if value == self.COUNTS_VALUE:
    #         print("Plot counts")
    #         ### TODO: Add code to update view info here
    #     elif value == self.DENSITY_VALUE:
    #         ### TODO: Add code to update view info here
    #         print("Plot densities")


class RefOptionCtrl(PlotOptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = super().make_option_card()
        op.label.configure(text="Reference Sequence")
        op.set_value(RefView())
        return op