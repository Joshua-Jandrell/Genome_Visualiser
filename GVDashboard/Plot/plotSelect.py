# This script contains option controllers for selectable plot views

from typing import Tuple
import customtkinter as ctk
from UI.optionPanel import OptionCtrl, OptionCard, OptionPanel
from Plot.plotInfo import DataSetInfo, ViewInfo_base
from Plot.ViewInfos import ZygoteView, RefView

from VCF.datasetDropDown import DatasetMenu

from Plot.OptionCards import FreqOptionCtrl, ZygoteOptionCtrl, RefOptionCtrl, PosOptionCtrl, MutFreqOptionCtrl, PlotOptionCard

ZYGOSITY_OPT = "Zygosity"
REF_OPT = "Ref. Genome"
FREQUENCY_OPT = "Mutation Frequency Histograms"
MUTATION_FREQUENCY_OPT = "Mutation Probabilities"
POS_OPT = "Position"

class PlotOptionPanel(OptionPanel):
    __instance = None

    def get_view_list()->list[ViewInfo_base]:
        """
        Returns a list of all selected view options.\n
        Returns an empty list is no instance of `PlotOptionPanel` exists.
        """
        if isinstance(PlotOptionPanel.__instance, PlotOptionPanel):
            return PlotOptionPanel.__instance.get_opt_values()
        else: return[]

    def select_instance_option(opt_key:str)->OptionCard:
        """
        Selects a view option and returns the newly created `OptionCard`.
        """
        assert(isinstance(PlotOptionPanel.__instance,PlotOptionPanel))
        return PlotOptionPanel.__instance.select_option(opt_key)
    
    def listen(command):
        """Add a listener to changes in the plot option panel."""
        if isinstance(PlotOptionPanel.__instance, PlotOptionPanel):
            PlotOptionPanel.__instance.content.add_listener(command=command)

    def listen_stop(command):
        """Remove a listener from plot option panel update events"""
        if isinstance(PlotOptionPanel.__instance, PlotOptionPanel):
            PlotOptionPanel.__instance.content.add_listener(command=command)


    def __init__(self, master, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, True, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, text="Plots", add_text="New plot", **kwargs)

        # Make dataset dropdown 
        self._dataset_menu = DatasetMenu(self, width=self.BUTTON_W*2, height=self.BUTTON_H)

        # Reposition some elements to fit dataset dropdown
        self._opt_add_button.grid(row=0, column=2)
        self.content.grid(row=1, column=0, columnspan=3)

        # Place dataset dropdown menu
        self._dataset_menu.grid(row=0, column=1)

        # There should only be one instance
        assert(not isinstance(PlotOptionPanel.__instance, PlotOptionPanel))
        PlotOptionPanel.__instance = self

        # Add plot options
        self.content.register_option(ZygoteOptionCtrl(self.content,ZYGOSITY_OPT))
        self.content.register_option(RefOptionCtrl(self.content,REF_OPT))
        self.content.register_option(MutFreqOptionCtrl(self.content,MUTATION_FREQUENCY_OPT))
        self.content.register_option(FreqOptionCtrl(self.content,FREQUENCY_OPT))
        self.content.register_option(PosOptionCtrl(self.content,POS_OPT))
    