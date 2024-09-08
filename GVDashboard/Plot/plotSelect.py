# This script contains option controllers for selectable plot views

from typing import Tuple
import customtkinter as ctk
from UI.optionPanel import OptionCtrl, OptionCard, OptionPanel
from Plot.plotInfo import ZygoteView, RefView, DataSetInfo, ViewInfo_base

from VCF.datasetDropDown import DatasetMenu

class PlotOptionList(OptionPanel):
    def __init__(self, master, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, True, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Add plot options
        self.content.register_option(ZygoteOption(self.content,"Zygosity"))
        self.content.register_option(RefOption(self.content,"Ref. Genome"))

class PlotOptionCard(OptionCard):
    """
    Special instance of option card used  
    """
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Add common elements to the plot option panel
        data_label = ctk.CTkLabel(self.content, text="dataset:")
        data_label.grid(row=0,column=0,padx=10,pady=10,sticky='w')
        self.data_menu = DatasetMenu(self.content,50, self.BUTTON_H, command=self.update_data)
        self.data_menu.grid(row=0,column=1,padx=10,pady=10,sticky='w')

    def update_data(self,event):
        assert(isinstance(self.value,ViewInfo_base))
        # set dataset name for view info
        self.value.set_data(self.data_menu.get_selected_dataset())

    def set_value(self, value):
        super().set_value(value)
        # update data to register on new plot info
        assert(isinstance(value,ViewInfo_base))
        self.update_data(value)

class PlotOptionCtrl(OptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = PlotOptionCard(self.option_list, self, self.key)
        return op

    
# Option control specifcally for zygosity inof
class ZygoteOption(PlotOptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = super().make_option_card()
        op.label.configure(text="Zygosity Plot")
        op.set_value(ZygoteView())
        return op
    
class RefOption(PlotOptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = super().make_option_card()
        op.label.configure(text="Reference Sequence")
        op.set_value(RefView())
        return op