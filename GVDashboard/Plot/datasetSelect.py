# This script contains dataset filters for viewing parts of datasets

from typing import Tuple
import customtkinter as ctk
from UI.optionPanel import OptionCtrl, OptionCard, OptionPanel
from Plot.plotInfo import ZygoteView, RefView, DataSetInfo, ViewInfo_base, FrequencyView

from VCF.datasetDropDown import DatasetMenu

from Plot.OptionCards import FreqOptionCtrl, ZygoteOptionCtrl, RefOptionCtrl

from GVDashboard.Plot.dataPanel_v2 import DataOptionCard


POSITION_RANGE_OPT = "Genome-variant Positions:"
QUALITY_RANGE_OPT = "Search by quality of \{???\}:"
QUALITY_SORT_OPT = "Sort by Quality:"
POPULATION_SORT_OPT = "Sort by Population of samples:"

class DatasetFilterPanel(OptionPanel):
    __instance = None

    def get_view_list()->list[ViewInfo_base]:
        """
        Returns a list of all selected view options.\n
        Returns an empty list is no instance of `DatasetFilterPanel` exists.
        """
        if isinstance(DatasetFilterPanel.__instance, DatasetFilterPanel):
            return DatasetFilterPanel.__instance.get_opt_values()
        else: return[]

    def select_instance_option(opt_key:str)->OptionCard:
        """
        Selects a view option and returns the newly created `OptionCard` for filtering.
        """
        assert(isinstance(DatasetFilterPanel.__instance,DatasetFilterPanel))
        return DatasetFilterPanel.__instance.select_option(opt_key)
    
    def listen(command):
        """Add a listener to changes in the plot option panel."""
        if isinstance(DatasetFilterPanel.__instance, DatasetFilterPanel):
            DatasetFilterPanel.__instance.content.add_listener(command=command)

    def listen_stop(command):
        """Remove a listener from plot option panel update events"""
        if isinstance(DatasetFilterPanel.__instance, DatasetFilterPanel):
            DatasetFilterPanel.__instance.content.add_listener(command=command)


    def __init__(self, master, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, True, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # There should only be one instance
        assert(not isinstance(DatasetFilterPanel.__instance, DatasetFilterPanel))
        DatasetFilterPanel.__instance = self

        # Add dataset options
        self.content.register_option(ZygoteOptionCtrl(self.content,POSITION_RANGE_OPT))
        self.content.register_option(RefOptionCtrl(self.content,QUALITY_RANGE_OPT))
        
        self.content.register_option(FreqOptionCtrl(self.content,QUALITY_SORT_OPT))
        self.content.register_option(FreqOptionCtrl(self.content,POPULATION_SORT_OPT))
        

