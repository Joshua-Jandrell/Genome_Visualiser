""""This script contains the implementation for the frequency option card and frequency option ctrl for the """
from typing import Tuple

import customtkinter as ctk

from Plot.OptionCards.plotCard import PlotOptionCard, PlotOptionCtrl, OptionCard
from Plot.plotInfo import FrequencyView

class FreqOptionCard(PlotOptionCard):
    """
    A plot option card specifically used to plot frequency option dat
    """
    # Useful constants 
    COUNTS_VALUE = 'counts'
    DENSITY_VALUE = 'density'
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        # Stupidly long list of constructor arguments (may be shortened in future)
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Get the dataset menu frame so that it can be put onto the card
        data_select_menu = self.get_dataset_menu_frame()
        # Put dataset menu onto the card using grid manager
        data_select_menu.grid(row = 0, column=0,padx=5,pady=5)

        # Add a segmented to help pick between plotting counts or density 
        counts_toggle = ctk.CTkSegmentedButton(master=self.content, #NB add all new elements to the content of the panel (not the panel itself)
                                               values=[self.COUNTS_VALUE,self.DENSITY_VALUE], # Values that can be selected on segmented button
                                               command=self.__on_count_toggle_change # The command to be called when the value is changed: will return the value of the toggle as an argument.
                                               )
        
        # Put toggle in the content grind
        counts_toggle.grid(row=1, column=0, padx=5, pady=5)
        # Select default toggle value to counts:
        counts_toggle.set(self.COUNTS_VALUE)

    def __on_count_toggle_change(self,value):
        """Private method called when the value of the counts toggle is updated."""
        assert(isinstance(self.value, FrequencyView)) # Ensure that view info is of type frequency view
        if value == self.COUNTS_VALUE:
           self.value.plot_density == False 
           print("Plot counts")
            ### TODO: Add code to update view info here
        elif value == self.DENSITY_VALUE:
            ### TODO: Figure out why density isn't called
            self.value.plot_density == True
            print("Plot densities")
        
        

class FreqOptionCtrl(PlotOptionCtrl):
    def make_option_card(self) -> OptionCard:
        #op = super().make_option_card()
        # Looks like the best way to make things manageable long-term is to make cutsom option cards for each plot type
        op = FreqOptionCard(master=self.option_list, # The UI container the option card goes into (should be an option list)
                             option_ctrl=self, # The option control that created this option card (should be this option control)
                             option_key="Mutation Frequency" # The `option_key` is essentially just the text displayed on the option card label
                             )
        #op.label.configure(text="Mutation Frequency")
        frequency_view_info = FrequencyView() # Make new view info for frequency plots.
        op.set_value(frequency_view_info) # Set value of option card to be frequency view info

        return op