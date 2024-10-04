""""This script contains the implementation for the frequency option card and frequency option ctrl for the """
from typing import Tuple

import customtkinter as ctk

from Plot.OptionCards.plotCard import PlotOptionCard, OptionCard
from Plot.ViewInfos import FrequencyView

class FreqOptionCard(PlotOptionCard):
    """
    A plot option card specifically used to plot frequency option dat
    """
    # Useful constants 
    COUNTS_VALUE = 'counts'
    DENSITY_VALUE = 'density'
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 70, corner_radius: int | str | None = 9, border_width: int | str | None = 1, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = "#FFF8DC", border_color: str | Tuple[str] | None = "#CC6677", background_corner_colors: Tuple[str | Tuple[str]] | None = ("#CC6677", "#CC6677", "#CC6677", "#CC6677"), overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.t = ctk.CTkLabel(self.content ,text= "This displays the density distribution of mutations across the selected set.", wraplength= 150)
        self.t.grid(row=1, column=1, padx=7, pady=5)
        
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
           self.value.set_should_plot_density(False)           
        elif value == self.DENSITY_VALUE:
            self.value.set_should_plot_density(True)

        # Invoke update event 
        self.update_event.invoke(self)
