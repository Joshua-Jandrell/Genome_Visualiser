# This script contains the search query options to loop from the vcf database

import customtkinter as ctk
import tkinter as tk

from UI.deafultSettings import Dimenations as Dims

from UI.optionPanel import OptionCard, OptionCtrl
from Plot.plotSelect import PlotOptionPanel
from VCF.dataPanel import DataPanel

class SearchPanel(ctk.CTkFrame): 
    def __init__(self, master):
        super().__init__(master=master, width=Dims.PANEL_WIDTH)

        self.search_options = SearchOptions(self)
        self.search_options.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Keep search options as it is used by other classes 
        # TODO This should be refactored to remove this depndancy
        self.button_panel = ctk.CTkFrame(self,bg_color='transparent', height=Dims.BUTTON_PANEL_HIGHT)
        self.button_panel.pack(side=ctk.TOP,fill=ctk.X)


class SearchOptions(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master=master, width=Dims.PANEL_WIDTH, fg_color="transparent")

        ## Adds tabs at the top of the Search Panel
        self.data = self.add("Datasets")
        self.plots = self.add("Plot")
        self.set("Datasets") #Selects which tab is active by default when Search Panel initially opens.

        # Create dataset panel 
        self.data_panel = DataPanel(self.data,fg_color="transparent")
        self.data_panel.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Create features for the options pannel 
        self.plots_options = PlotOptionPanel(self.plots,fg_color="transparent")
        self.plots_options.pack(fill=ctk.BOTH, expand=True)
