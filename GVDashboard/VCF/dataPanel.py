# This script contains the classes and panel used for data selection
from typing import Any, Tuple
import customtkinter as ctk

from UI.optionPanel import OptionCard
from UI.optionPanel import OptionCtrl, OptionList

from VCF.filterInfo import DataSetInfo
from VCF.dataSetPanel import DataSetConfig

# Panel used to add and remove Datasets and the filter options of each "Dataset".
class DataPanel(ctk.CTkFrame):
    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Class-level constants 
        self.ADD_TXT = "+"
        self.PLOT_TXT = "Datasets"

        # Create top label
        self.make_title()
        self.make_add_button()
        # Create content 
        self.content = OptionList(self, False)

        # Position objects in grid
        self.title_txt.grid(row=0,column=0,sticky="ew",padx=20)
        self.add_button.grid(row=0,column=1,sticky="e")
        self.content.grid(row=1,column=0,columnspan=2, sticky="nsew")

        # configure grid layout 
        self.grid_columnconfigure(0,weight=7)
        self.grid_columnconfigure(1,weight=3)
        self.grid_rowconfigure(1,weight=1)


    def make_title(self):
        self.title_txt = ctk.CTkLabel(master=self,
                                      text=self.PLOT_TXT)
        
    # Creates the basic dropdown button to add new plot types
    def make_add_button(self):
        self.selected_opt = ctk.StringVar()
        self.add_button = ctk.CTkButton(self,text=self.ADD_TXT,command=self.on_add_button_click, width=20, height=20)

    def on_add_button_click(self):
        # Create file path selection dialog box
        self.new_dataset = DataSetConfig(self)

# Class used to create dataset option panels
class DataOption(OptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = super().make_option_card()
        return op