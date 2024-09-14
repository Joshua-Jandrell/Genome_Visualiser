# This script contains the classes and panel used for data selection
from typing import Any, Tuple
import customtkinter as ctk

from UI.optionPanel import OptionCard
from UI.optionPanel import OptionCtrl, OptionList

from VCF.filterInfo import DataSetInfo
from VCF.dataSetConfig import DataSetConfig
from VCF.globalDatasetManger import GlobalDatasetManager

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

#DataOptionCard:                #### Currently:: Initialises and says hi :)
class DataOptionCard(OptionCard):
    """
    Special instance of option card used to make plots. Contains useful methods for constructing common plot option widgets.\n
    The `self.value` field of a plot option card should alway inherit from `ViewInfo_base` so that it can be used to plot views.
    """
    def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Set default width of menu buttons
        self.MENU_W = 125
 
        ###
        #Add range selection functions from DataWrapper here
        ###
            
            #From, file: plotCard.py --> class: PlotOptionCard 
            # def set_value(self, value):
            #     """Override of set value method. Value must inherit for `ViewInfo_base`."""
            #     super().set_value(value)
            #     # update data to register on new plot info
            #     assert(isinstance(value,ViewInfo_base))
            #     self.__on_dataset_update(value)

        # So you can add any number of tkinter or custom tkinter elements to the card.  <<< That's pretty cool!!
        # Used `self.content` as the master (root) for all elements you add (this way you won't need to worry about the card label)  <<< A... content creator?!??!!? 
    
    ############### JOSH'S  CODE :: (look out below):: 
        # For example here is a simple button:
        random_button = ctk.CTkButton(master=self.content, # Note that master is content.
                                      text="Cool button",  # This text will display on the button
                                      command=self.say_hi) # The command is a function that is called when the button is pressed
                                                           # NOTE this function will not work until say hi is implemented 
       
        # NB once an element is made it must be packed/placed in the content panel:
        random_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10) # The button will be in the 2nd row and span two columns

        self.text_var = ctk.StringVar(value="words") # A custom tkinter variable that can be linked to a UI input element 
        self.text_input = ctk.CTkEntry(self.content,textvariable=self.text_var)
        self.text_input.grid(row=0, column=1, columnspan=1, padx=10, pady=10) 
    
                
    def say_hi(self):
        text_val = self.text_var.get() # Can get value form text variable 
        text_val2 = self.text_input.get() # Can also get value directly from tet input 
        print(f"Hi {text_val} and {text_val2}")

        self.text_var.set("Noice") # can also set value of variable to change the text which is displayed 

        # In this case the `self.value` variable will be a data info (which hold a reference to a datawrapper)
        assert(isinstance(self.value, DataSetInfo))
        dw = self.value.get_data_wrapper() # NB please PULL from git to get this to work without loading a new datawrapper each time
        # now, for example, you could use that number extracting code to get numeric values form textbox input...
                   


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
        op = DataOptionCard(self.option_list, self, self.key)
        # op = DatasetOptionCard(self.option_list, self, "eee")  <<< For error checking I'm guessing
        op.reconfigure_option(option_key=self.dataset_info.get_dataset_name(), option_value=self.dataset_info)

        # Clear reference to dataset_info to ensure that configuration always occurs
        self.dataset_info = None

        return op
    
    def deselect(self, opt: OptionCard):
        # Deregister option card form global manager
        GlobalDatasetManager.deregister(opt.value)
        super().deselect(opt)

      ###################~~ JOSH'S CODE FOR: DataOptionCard ~~############################################
 
# class DatasetOptionCard(OptionCard):   ### MUST TAKE out later
#     "Example class - will not commit to avoid comflicts"
    # def __init__(self, master, option_ctrl, option_key: str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
    #     super().__init__(master, option_ctrl, option_key, option_value, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

    #     # So you can add any number od tkinter or custom tkinter elements to the card.
    #     # Used `self.content` as the master (root) for all elements you add (this way you won't need to worry about the card label)

    #     # For example here is a simple button:
    #     random_button = ctk.CTkButton(master=self.content, # Note that master is content.
    #                                   text="Cool button",  # This text will display on the button
    #                                   command=self.say_hi) # The command is a function that is called when the button is pressed
    #                                                        # NOTE this function will not work until say hi is implemented 
    #     # NB once an element is made it must be packed/placed in the content panel:
    #     random_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10) # The button will be in the 2nd row and span two columns

    #     self.text_var = ctk.StringVar(value="words") # A custom tkinter variable that can be linked to a UI input element 
    #     self.text_input = ctk.CTkEntry(self.content,textvariable=self.text_var)
    #     self.text_input.grid(row=0, column=1, columnspan=1, padx=10, pady=10) 
    
    # def say_hi(self):
    #     text_val = self.text_var.get() # Can get value form text variable 
    #     text_val2 = self.text_input.get() # Can also get value directly from tet input 
    #     print(f"Hi {text_val} and {text_val2}")

    #     self.text_var.set("Noice") # can also set value of variable to change the text which is displayed 

    #     # In this case the `self.value` variable will be a data info (which hold a reference to a datawrapper)
    #     assert(isinstance(self.value, DataSetInfo))
    #     dw = self.value.get_data_wrapper() # NB please PULL from git to get this to work without loading a new datawrapper each time
    #     # now, for example, you could use that number extracting code to get numeric values form textbox input...
