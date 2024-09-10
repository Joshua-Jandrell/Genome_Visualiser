# This script contains the classes and panel used for data selection
from typing import Any, Tuple
import customtkinter as ctk

from UI.optionPanel import OptionCard
from UI.optionPanel import OptionCtrl, OptionList

from VCF.filterInfo import DataSetInfo
from VCF.dataSetConfig import DataSetConfig
from VCF.gloabalDatasetManger import GlobalDatasetManager

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

        # Data option control used to create new dataset cards
        self.data_opt_ctl = DataOptionCtrl(option_list=self.content,key="Add")

        # Subscribe to option list change event 
        GlobalDatasetManager.add_listener(self.__on_global_data_update)

    def make_title(self):
        self.title_txt = ctk.CTkLabel(master=self,
                                      text=self.PLOT_TXT)
        
    # Creates the basic dropdown button to add new plot types
    def make_add_button(self):
        self.selected_opt = ctk.StringVar()
        self.add_button = ctk.CTkButton(self,text=self.ADD_TXT,command=self.on_add_button_click, width=20, height=20)

    def on_add_button_click(self):
        # Open data picker dialog box
        DataSetConfig.open(self,command=self.on_data_select)

    def on_data_select(self, dataset_info:DataSetInfo):
        # self.data_opt_ctl.configure(dataset_info)
        # self.data_opt_ctl.select()

        # Register dataset with global manager.
        # NOTE When this is done a card will be automatically created
        GlobalDatasetManager.register(dataset_info)

    def __on_global_data_update(self, dataset_names):
        """Called when the list of global datasets is updated to add any new datasets here."""
        current_datasets = self.content.get_opt_values()
        all_datasets = GlobalDatasetManager.get_datasets() 

        # Add all new datasets to dataset options list
        [self.data_opt_ctl.register_dataset(dataset) for dataset in all_datasets if dataset not in current_datasets]
            

    def destroy(self):
        # Unsubscribe from global dataset event
        GlobalDatasetManager.remove_listener(self.__on_global_data_update)

        # Remove all datasets 
        self.content.deselect_all()
        GlobalDatasetManager.reconfigure(datasets = [])
        return super().destroy()

# Class used to create dataset option panels
class DataOptionCtrl(OptionCtrl):
    """
    An option controller to manges option cards for datasets
    """
    def register_dataset(self,dataset_info:DataSetInfo, add_set:bool = True):
        """
        Set the dataset info that the next selected dataset will hold a reference to.\n
        If `add_set` is `True` then the set will automatically be selected and added to the list.
        """
        self.dataset_info = dataset_info
        if add_set:
            self.select()

    def make_option_card(self) -> OptionCard:
        # NOTE: This method is called whenever a dataset is register. DO NOT register dataset here.

        assert(isinstance(self.dataset_info,DataSetInfo)) # Option should never be selected when info is not set
        op = super().make_option_card()
        op.reconfigure_option(option_key=self.dataset_info.get_dataset_name(), option_value=self.dataset_info)

        # Clear reference to dataset info to ensure that config always occurs
        self.dataset_info = None

        return op
    
    def deselect(self, opt: OptionCard):
        # Deregister option card form global manager
        GlobalDatasetManager.deregister(opt.value)
        super().deselect(opt)
