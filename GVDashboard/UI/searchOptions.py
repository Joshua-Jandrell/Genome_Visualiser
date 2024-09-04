# This script contains the search query options to loop from the vcf database

import customtkinter as ctk
import tkinter as tk

from UI.deafultSettings import Dimenations as Dims

from Plot.plotSelect import OptionList, OptionCtrl


class SearchPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, width=Dims.PANEL_WIDTH)

        # Configure the grid system
        self.rowconfigure(0,weight=80)
        self.rowconfigure(1,weight=20)

        self.button_panel = ctk.CTkFrame(self,bg_color='transparent', height=Dims.BUTTON_PANEL_HIGHT)
        self.search_options = SearchOptions(self)

        self.button_panel.pack(side=ctk.BOTTOM,fill=ctk.X)
        self.search_options.pack(side=ctk.BOTTOM, expand=True, fill=ctk.BOTH)

# Class contains details for how plot should be displayed
class DisplayData(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master,)
        self.show_ref = ctk.BooleanVar(value=True)
        self.show_alt = ctk.BooleanVar(value=True)
        self.show_labels = ctk.BooleanVar(value=True)
        self.min_block_size = 20

        # Add UI elements
        # ==> Show reference checkbox
        ref_label = ctk.CTkLabel(
            master = self,
            text="Display Sequence Information"
        )
        ref = ctk.CTkCheckBox(
            master = self,
            text = "Ref. Sequence",
            variable=self.show_ref
        )
        # ==> Show alternatives checkbox 
        alt = ctk.CTkCheckBox(
            master = self,
            text = "Alt. Sequence",
            variable=self.show_alt
        )
        # ==> annotate refs
        labels = ctk.CTkCheckBox(
            master=self,
            text="Show Labels",
            variable=self.show_labels
        )

        # Pack UI elements 
        ref_label.grid(row=0, column=0, columnspan=2)
        ref.grid(row=1, column=0)
        alt.grid(row=1, column=1)
        labels.grid(row=2, column=0)


class SearchOptions(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master=master)

        self.filters = self.add("Filers")
        self.display = self.add("Display")
        self.testing = self.add("Testing")
        self.plots = self.add("Plot")
        self.set("Plot")

        # Add fetures to display
        self.displayData = DisplayData(self.display)
        self.displayData.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Add features to the testing panel
        no_vars = ctk.CTkTextbox(self.testing)
        no_vars.pack(expand=True, fill="both")
        
        pl = OptionList(self.plots)
        pl.pack(fill=ctk.BOTH, expand=True)

        oc = OptionCtrl(pl,"nice")
        oc = OptionCtrl(pl,"cool")
        

