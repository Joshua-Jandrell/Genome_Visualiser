# This script contains option controllers for selectable plot views

from typing import Tuple
import customtkinter as ctk

from UI.optionPanel import OptionCtrl, OptionCard, OptionPanel
from Plot.ViewInfos import DataSetInfo, ViewInfo_base, ZygoteView, RefView, VarPosView, FrequencyView, MutFreqView, CaseCtrlView, MutationBarView

from VCF.datasetDropDown import DatasetMenu

from Plot.OptionCards import PlotOptionCard, RefOptionCard, MutFreqOptionCard, FreqOptionCard, ZygoOptionCard, CasecntrlOptionCard

REF_OPT = "Ref. & Alt. Genome"
ZYGOSITY_OPT = "Sample Zygosity Map"
MUTATION_FREQUENCY_OPT = "Mutation Probabilities Map"
FREQ_BAR_OPT = "Zygosity Frequency Bar Graph"
CASE_CTRL_OPT = "Case/Control View"

POS_OPT = "Position Heatmap"
FREQUENCY_OPT = "Population Mutation Density Histograms"

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
        _swaps = False
        super().__init__(master, _swaps, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, text="Plot", add_text="New plot", **kwargs)


        # Reposition some elements to fit dataset dropdown
        self._opt_add_button.grid_forget()
        self.content.grid(row=1, column=0, columnspan=3)

        # Configure gird columns
        self.grid_columnconfigure(1, weight=1)

        # Make dataset dropdown label
        _dropdown_label = ctk.CTkLabel(self, text="Dataset:", justify='right')

        # Make dataset dropdown 
        self._dataset_menu = DatasetMenu(self, width=self.BUTTON_W*2, height=self.BUTTON_H,
                                         command=self.__on_dataset_select)
        

        # Place dataset dropdown menu and label
        _dropdown_label.grid(row=0, column=1, sticky="w", padx=0)
        self._dataset_menu.grid(row=0, column=2)

        # There should only be one instance
        assert(not isinstance(PlotOptionPanel.__instance, PlotOptionPanel))
        PlotOptionPanel.__instance = self

        # Set option list to toggle all view options as they are register (to create plot cards)
        self.content.set_toggle_on_register(True)

        # Add plot options
        self.content.register_option(OptionCtrl(self.content,REF_OPT, option_class=RefOptionCard,option_value=RefView))
        self.content.register_option(OptionCtrl(self.content,ZYGOSITY_OPT, option_class=ZygoOptionCard, option_value=ZygoteView))
        self.content.register_option(OptionCtrl(self.content,MUTATION_FREQUENCY_OPT, option_class= MutFreqOptionCard, option_value=MutFreqView))
        self.content.register_option(OptionCtrl(self.content,FREQ_BAR_OPT, option_value=MutationBarView))
        self.content.register_option(OptionCtrl(self.content,CASE_CTRL_OPT,option_class=CasecntrlOptionCard, option_value=CaseCtrlView))
        
        self.content.register_option(OptionCtrl(self.content,POS_OPT, option_value=VarPosView))
        self.content.register_option(OptionCtrl(self.content,FREQUENCY_OPT, option_class= FreqOptionCard, option_value=FrequencyView))
        
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

    