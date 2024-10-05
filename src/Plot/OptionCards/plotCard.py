"""This script contains the base class for plot option control and plot option cards"""
from typing import Tuple
import customtkinter as ctk

from UI.optionPanel import OptionCard, OptionCtrl
from VCF.datasetDropDown import DatasetMenu

from Plot.ViewInfos import ViewInfo_base


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
        self.dataset_menu_frame = None
   
