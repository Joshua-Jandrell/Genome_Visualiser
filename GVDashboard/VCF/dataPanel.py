# This script contains the classes and panel used for data selection
from typing import Any, Tuple
import customtkinter as ctk

from UI.optionPanel import OptionCard
from UI.optionPanel import OptionCtrl, OptionList

from VCF.datasetDropDown import DatasetMenu

from VCF.filterInfo import DataSetInfo
from VCF.dataSetConfig import DataSetConfig
from VCF.globalDatasetManger import GlobalDatasetManager

from VCF.dataWrapper import VcfDataWrapper, SortMode
from Plot.plotInfo import ViewInfo_base


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
        DataSetConfig.open(self,register_on_create = True)

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

#DataOptionCard:
_entry_padx = 5
_padx_lastcol = 3
_padx_entrybox = 2
_padx_head = 8
_pady = 4
_height = 4
_width = 60
_width_fromto = 25
class DataOptionCard(OptionCard):
    """
    Special instance of dataset option card used to make plots. Contains useful methods for constructing common plot option widgets.\n
    The `self.value` field of a plot option card should alway inherit from `ViewInfo_base` so that it can be used to plot views.
    """
    def __init__(self, master, option_ctrl, option_key: str, option_value:DataSetInfo, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        
        #__init__(self, *args, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        #super().__init__(*args, **kwargs)
        # Set default width of menu buttons
        self.MENU_W = 125
     #####################################################################################################
     #### Position range
        
        dw = self.get_datawrap()
        min_pos, max_pos = dw.get_file_pos_range()
        # print(f"the min is: {min_pos}")
        # print(f"the max is: {max_pos}")
        
        #Position heading Textbox:
        self.position_headingLabel = ctk.CTkLabel(self.content, text=" Genome Position Range", justify="center", height=_height)
        self.position_headingLabel.grid(row=0, column=0, columnspan=3, padx=_padx_head, pady=_pady, sticky="ew")
        #Textbox:
        self.position_startLabel = ctk.CTkLabel(self.content, text="From:", width=_width_fromto, height=_height)
        self.position_startLabel.grid(row=1, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w") #
        #input field:
        self.input_pos_min = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.position_start = ctk.CTkEntry(self.content, textvariable=self.input_pos_min, width= _width, height=_height) #begin_posrange=self.input_pos_start)
        self.position_start.grid(row=1, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") #padx=0, pady=0, 
        #Textbox:
        self.position_minstartLabel = ctk.CTkLabel(self.content, text=(min_pos,"(min)"), width=_width_fromto, height=_height)
        self.position_minstartLabel.grid(row=1, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        #Next row:
        #Textbox:
        self.position_endLabel = ctk.CTkLabel(self.content, text="To:", width=_width_fromto, height=_height) #, compound="top", justify="left", anchor="w")
        self.position_endLabel.grid(row=2, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w")
        #input field:
        self.input_pos_max = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.position_end = ctk.CTkEntry(self.content,textvariable=self.input_pos_max, width= _width, height=_height) # end_posrange=self.input_pos_end)
        self.position_end.grid(row=2, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") 
        #Textbox:
        self.position_maxendLabel = ctk.CTkLabel(self.content, text=(max_pos,"(max)"), width=_width_fromto, height=_height)
        self.position_maxendLabel.grid(row=2, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        # Add traces to read in position input values:
        self.input_pos_min.trace_add(mode="write", callback=self.read_in_pos)
        self.input_pos_max.trace_add(mode="write", callback=self.read_in_pos)
        
        
      ####### quality range:   ##############
        dw = self.get_datawrap()
        min_pos, max_pos = dw.get_file_pos_range()   ##############   REDO
        
        #Quality heading Textbox:
        self.quality_headingLabel = ctk.CTkLabel(self.content, text="Variant Quality Range", justify="center", height=_height)
        self.quality_headingLabel.grid(row=3, column=0, columnspan=3, padx=_padx_head, pady=_pady, sticky="ew")
        #Textbox:
        self.quality_startLabel = ctk.CTkLabel(self.content, text="From:", width=_width_fromto, height=_height)
        self.quality_startLabel.grid(row=4, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w") #
        #input field:
        self.input_qual_min = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.quality_start = ctk.CTkEntry(self.content, textvariable=self.input_qual_min, width=_width, height=_height) #begin_posrange=self.input_pos_start)
        self.quality_start.grid(row=4, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") #padx=0, pady=0, 
        #Textbox:
        self.quality_minstartLabel = ctk.CTkLabel(self.content, text=("0 (min)"), width=_width_fromto, height=_height)
        self.quality_minstartLabel.grid(row=4, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        #Next row:
        #Textbox:
        self.quality_endLabel = ctk.CTkLabel(self.content, text="To:", width=_width_fromto, height=_height) #, compound="top", justify="left", anchor="w")
        self.quality_endLabel.grid(row=5, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w")
        #input field:
        self.input_qual_max = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.quality_end = ctk.CTkEntry(self.content,textvariable=self.input_qual_max, width= _width, height=_height) # end_posrange=self.input_pos_end)
        self.quality_end.grid(row=5, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") 
        #Textbox:
        self.quality_maxendLabel = ctk.CTkLabel(self.content, text=("100 (max)"), width=_width_fromto, height=_height)
        self.quality_maxendLabel.grid(row=5, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        # Add traces to read in sample quality input values:
        self.input_qual_min.trace_add(mode="write", callback=self.read_in_qual)
        self.input_qual_max.trace_add(mode="write", callback=self.read_in_qual)

     ###### Sort options:    ##############
     #Sort heading Textbox:
        self.quality_headingLabel = ctk.CTkLabel(self.content, text="Sort Samples by :", justify="center", height=_height)
        self.quality_headingLabel.grid(row=6, column=0, columnspan=3, padx=_padx_head, pady=_pady, sticky="ew")
    
     # Quality and Population Radio Buttons:
        self.set_sort_mode = ctk.IntVar(value=int(SortMode.BY_POSITION))

        self.positionRadioButton = ctk.CTkRadioButton(self.content, text="Position\n(low to high)", variable=self.set_sort_mode, value=SortMode.BY_POSITION, command=self.set_dw_sortmode, width=50, height=_height)
        self.positionRadioButton.grid(row=7, column=0, padx=_padx_entrybox, pady=_pady, sticky="w")
        
        self.qualityRadioButton = ctk.CTkRadioButton(self.content, text="Quality\n(100 to 0)", variable=self.set_sort_mode, value=SortMode.BY_QUALITY, command=self.set_dw_sortmode, width=50, height=_height)
        self.qualityRadioButton.grid(row=7, column=1, padx=_padx_entrybox, pady=15, sticky="w")

        # self.populationRadioButton = ctk.CTkRadioButton(self, text="Population\n(alphabetically)", variable=self.set_sort_mode, value=SortMode.BY_POPULATION, command=self.set_dw_sortmode)
        # self.populationRadioButton.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        
        #Sort heading Textbox:
        self.instruct_headingLabel = ctk.CTkLabel(self.content, text="Click the Plot button to apply filter options.", justify="center", fg_color='light green')
        self.instruct_headingLabel.grid(row=9, column=0, columnspan=3, padx=_padx_lastcol, pady=_pady, sticky="ew")
        
    # dropdown 
        #~self.sort_option = ctk.CTkOptionMenu(self)
        
    def get_datawrap(self) -> VcfDataWrapper:
        assert(isinstance(self.value, DataSetInfo))
        dw = self.value.get_data_wrapper()

        return dw
    
    def set_dw_sortmode(self):
        dw = self.get_datawrap()
        dw.set_sort_mode(self.set_sort_mode.get())

    def read_in_pos(self, *args):
        _start_pos_input = self.input_pos_min.get()
        number_input = "".join([c for c in _start_pos_input if c.isdigit()])
        if _start_pos_input  != number_input:
            self.input_pos_min.set(number_input)
        
        _end_pos_input = self.input_pos_max.get()
        number_input = "".join([c for c in _end_pos_input if c.isdigit()])
        if _end_pos_input  != number_input:
            self.input_pos_max.set(number_input)
        
        dw = self.get_datawrap()
        dw.set_pos_range(int("0"+self.input_pos_min.get()),int("0"+self.input_pos_max.get()))
            
    def read_in_qual(self, *args):
        _start_qual_input = self.input_qual_min.get()
        number_input = "".join([c for c in _start_qual_input if c.isdigit()])
        if _start_qual_input  != number_input:
            self.input_qual_min.set(number_input)
        
        _end_qual_input = self.input_qual_max.get()
        number_input = "".join([c for c in _end_qual_input if c.isdigit()])
        if _end_qual_input  != number_input:
            self.input_qual_max.set(number_input)  

        dw = self.get_datawrap()
        dw.set_qual_range(int("0"+self.input_qual_min.get()),int("0"+self.input_qual_max.get()))

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
        # NOTE: This method is called whenever a dataset is registered. DO NOT register dataset here.

        assert(isinstance(self.dataset_info,DataSetInfo)) # Option should never be selected when info is not set
        op = DataOptionCard(self.option_list, self, self.key, option_value=self.dataset_info)
        # op = DatasetOptionCard(self.option_list, self, "eee")  <<< For error checking I'm guessing
        op.reconfigure_option(option_key=self.dataset_info.get_dataset_name())

        # Clear reference to dataset_info to ensure that configuration always occurs
        self.dataset_info = None

        return op
    
    def deselect(self, opt: OptionCard):
        # Deregister option card form global manager
        GlobalDatasetManager.deregister(opt.value)
        super().deselect(opt)

