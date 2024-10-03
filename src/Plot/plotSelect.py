# This script contains option controllers for selectable plot views

from typing import Tuple
import customtkinter as ctk
from UI.optionPanel import OptionCtrl, OptionCard, OptionPanel
from Plot.plotInfo import DataSetInfo, ViewInfo_base
from Plot.ViewInfos import ZygoteView, RefView, VarPosView, FrequencyView, MutFreqView, CaseCtrlView, MutationBarView

from VCF.datasetDropDown import DatasetMenu

from Plot.OptionCards import PlotOptionCard, RefOptionCard

ZYGOSITY_OPT = "Zygosity"
REF_OPT = "Ref. Genome"
FREQUENCY_OPT = "Mutation Frequency Histograms"
MUTATION_FREQUENCY_OPT = "Mutation Probabilities"
POS_OPT = "Position"
CASE_CTRL_OPT = "Case/Ctrl view "
FREQ_BAR_OPT = "Mutation Frequency Bar Graph"

class PlotOptionPanel(OptionPanel):
    __instance = None

    def get_view_list()->list[ViewInfo_base]:
        """
        Returns a list of all selected view options.\n
        Returns an empty list is no instance of `PlotOptionPanel` exists.
        """
        if isinstance(PlotOptionPanel.__instance, PlotOptionPanel):
            return PlotOptionPanel.__instance.__get_views()
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


        # Reposition some elements to fit dataset dropdown
        self._opt_add_button.grid(row=0, column=2)
        self.content.grid(row=1, column=0, columnspan=3)


        # Make dataset dropdown 
        self._dataset_menu = DatasetMenu(self, width=self.BUTTON_W*2, height=self.BUTTON_H,
                                         command=self.__on_dataset_select)

        # Place dataset dropdown menu
        self._dataset_menu.grid(row=0, column=1)

        # There should only be one instance
        assert(not isinstance(PlotOptionPanel.__instance, PlotOptionPanel))
        PlotOptionPanel.__instance = self

        # Add plot options
        self.content.register_option(OptionCtrl(self.content,ZYGOSITY_OPT, ZygoteView))
        self.content.register_option(OptionCtrl(self.content,REF_OPT, option_class=RefOptionCard,option_value=RefView))
        self.content.register_option(OptionCtrl(self.content,MUTATION_FREQUENCY_OPT, option_value=MutFreqView))
        self.content.register_option(OptionCtrl(self.content,FREQUENCY_OPT, option_value=FrequencyView))
        self.content.register_option(OptionCtrl(self.content,POS_OPT, option_value=VarPosView))
        self.content.register_option(OptionCtrl(self.content,CASE_CTRL_OPT, option_value=CaseCtrlView))
        self.content.register_option(OptionCtrl(self.content,CASE_CTRL_OPT, option_value=CaseCtrlView))
        self.content.register_option(OptionCtrl(self.content,FREQ_BAR_OPT, option_value=MutationBarView))

    def __get_views(self)->list[ViewInfo_base]:
        """
        Returns a list of all views and sets there datasets if required.
        """
        # Check if dataset has been set
        views = self.get_opt_values()
        dataset = self._dataset_menu.get_selected_dataset()
        self.__set_dataset_for_all(dataset, views)
        return views
    
    def __on_dataset_select(self, dataset_name):
        self.__set_dataset_for_all(self._dataset_menu.get_selected_dataset(), self.get_opt_values())

    def __set_dataset_for_all(self,dataset:DataSetInfo|None, views:list[ViewInfo_base]):
        """
        Set all plot options to use the given dataset.\n
        """
        for view in views:
            assert(isinstance(view,ViewInfo_base))
            view.set_data(dataset)

    