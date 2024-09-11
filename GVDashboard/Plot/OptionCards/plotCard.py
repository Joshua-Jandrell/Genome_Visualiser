"""This script contains the base class for plot option control and plot option cards"""
from typing import Tuple
import customtkinter as ctk

from UI.optionPanel import OptionCard, OptionCtrl
from VCF.datasetDropDown import DatasetMenu

from Plot.plotInfo import ViewInfo_base


class PlotOptionCard(OptionCard):
    """
    Special instance of option card used to make plots. Contains useful methods for constructing common plot option widgets.\n
    The `self.value` field of a plot option card should alway inherit from `ViewInfo_base` so that it can be used to plot views.
    """
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Set default width of menu buttons
        self.MENU_W = 125
        
        # Create dataset menu
        self.dataset_menu_frame =self.make_dataset_menu()
 
    def make_dataset_menu(self)->ctk.CTkFrame:
        """
        Returns The frame of a dataset menu linked to this plot option card.\n
        The menu can be access as `self.data_menu`.\n
        NOTE: The menu frame will not be placed or packed into the content by this function.
        """
        self.dataset_frame = frame = ctk.CTkFrame(self.content, height=self.BUTTON_H)
        data_label = ctk.CTkLabel(frame, text="Dataset:")
        self.data_menu = DatasetMenu(frame, width=self.MENU_W, height=self.BUTTON_H, command=self.__on_dataset_update, dynamic_resizing=False)
        data_label.pack(side=ctk.LEFT, padx = 5, pady = 0)
        self.data_menu.pack(side=ctk.LEFT)
        return self.dataset_frame

    def get_dataset_menu_frame(self)->ctk.CTkFrame:
        """Method used to get the frame holding the dataset menu.\n"""
        """Use this method to access and place the dataset menu on the card."""
        return self.dataset_menu_frame
        

    def __on_dataset_update(self,event):
        """Private method to be called when dataset is updated (generally by dataset menu)."""
        if isinstance(self.value,ViewInfo_base): # Check that there is an instance of value (view_info) to update.
            prev_val = self.value.get_data()
            new_val = self.data_menu.get_selected_dataset()

            if prev_val != new_val:
                # set dataset name for view info
                self.value.set_data(new_val)
                self.update_event.invoke(self)

    def set_value(self, value):
        """Override of set value method. Value must inherit for `ViewInfo_base`."""
        super().set_value(value)
        # update data to register on new plot info
        assert(isinstance(value,ViewInfo_base))
        self.__on_dataset_update(value)

class PlotOptionCtrl(OptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = PlotOptionCard(self.option_list, self, self.key)
        return op
