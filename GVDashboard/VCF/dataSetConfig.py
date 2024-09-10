# This script contains classes and features for data selection and filtering UI

from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk
from os import path
import tkinter as tk

from VCF.dataFetcher import DataFetcher
from VCF.dataWrapper import VcfDataWrapper
from VCF.filterInfo import DataSetInfo
from VCF.globalDatasetManger import GlobalDatasetManager

from UI.tooltip import ToolTip

# This class is used to select and return files throughout the application
class FileFetcher:
    FETCHED_FILES = []

    # Returns the string path to a user-selected vcf file
    def get_vcf_filename()->str:
        filename = ctk.filedialog.askopenfilename(title="Select data file",filetypes=[("Variant call format","*.vcf *.vcf.gz")])
        if filename == "": return ""
        if filename not in FileFetcher.FETCHED_FILES:
            FileFetcher.FETCHED_FILES.append(filename)
        return filename

    def get_selected_data()->VcfDataWrapper:
        filename = FileFetcher.get_vcf_filename()
        if filename is not None and filename != "":
            return DataFetcher.load_data(filename)

FIELD_LABEL_PADDING = 20
def make_field_label(master,text:str)->ctk.CTkLabel:
    "Create a text label for the dataset creator fields"
    label =ctk.CTkLabel(master,text=text)
    label._font.configure(weight="bold")

    return label

class FilePicker(ctk.CTkFrame):
    """
    Class used to select and validate files for selection
    """

    MAX_PATH_CHARS = 20
    NO_PATH_TXT = "No path selected..."
    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        # Initialise constans
        self.path_var = ctk.StringVar(value=FilePicker.NO_PATH_TXT)
        self._path_value = ""   # Used to hold the validated path 

        # Create and pack elements 
        self.label = make_field_label(self,text="Source File:")
        self.label.pack(side=ctk.LEFT, padx=FIELD_LABEL_PADDING)

        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx = 0)
        self.path_txt = ctk.CTkLabel(self.path_frame,text="No file selected...",anchor="w", justify=ctk.LEFT)
        self.path_txt.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx = 10)

        self.file_button = ctk.CTkButton(self, text="select", command=self.user_update_path, width=40)
        self.file_button.pack(side=ctk.LEFT)
        self.path_tooltip = ToolTip(self.path_txt, text=None)

    def _on_file_change(self):
        path = self.path_var.get()
        if path == "": return
        self._path_value = path
        self._update_path_text(path)
    

    # Updates path text display to only show file name 
    def _update_path_text(self,path_text:str):
        self.path_tooltip.text = path_text
        # Get only the filename
        file_name = path.basename(path.realpath(path_text))

        self.path_txt.configure(text=file_name)


    def user_update_path(self):
        path = FileFetcher.get_vcf_filename()
        self.path_var.set(value=path)
        self._on_file_change()

    def update_dataset(self, dataset:DataSetInfo):
        if self._path_value == "": return
        dataset.configure(source_path=self._path_value)

    def set_path(self,path:str|None):
        if path is None:
            self.path_var.set(value=FilePicker.NO_PATH_TXT)
            self._path_value = ""
        else:
            self.path_var.set(path)
            self._path_value = path
            self._update_path_text(path)

class DatasetNameEdit(ctk.CTkFrame):
    "Class used to edit the name of a dataset"

    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.name_var = ctk.StringVar(value="Name...")
        # Create and pack elements 
        self.label = make_field_label(self, text="Name: ")
        self.label.pack(side=ctk.LEFT, padx=FIELD_LABEL_PADDING)

        self.name_entry = ctk.CTkEntry(self)
        # NOTE The text variable MUST be set here and not in the constructor.
        # Otherwise a memory leak occures due to issues with custom tkinter.
        self.name_entry.configure(textvariable=self.name_var) 
        self.name_entry.pack()

    def set_name(self,dataset_name:str):
        self.name_var.set(dataset_name)
        
    def update_dataset(self, dataset:DataSetInfo):
        dataset.configure(name=self.name_var.get())

    
        
    
class DataSetConfig(ctk.CTkToplevel):
    """
    A top-level window that lets the user create and edit datasets and their filters.
     NOTE Use the static `open` and `close` methods to control the panel, not the constructor
    """
    instance = None

    def open(app:ctk.CTk|None = None, dataset:DataSetInfo|None = None, command:Callable[[DataSetInfo],Any]|None = None, register_on_create:bool = True, get_file_first:bool = True, fg_color: str | Tuple[str] | None = None, **kwargs):
        
        new_file = False
        if get_file_first and dataset is None:
            file_name = FileFetcher.get_vcf_filename()
            if file_name == "": return
            dataset = DataSetInfo(source_path=file_name)
            new_file = True

        
        if not isinstance(DataSetConfig.instance,DataSetConfig):
            DataSetConfig.instance = DataSetConfig(app, dataset, command, register_on_create, new_file, fg_color, **kwargs)
        else:
            DataSetConfig.instance.__open_config(dataset=dataset, command=command, register_on_create=register_on_create, treat_as_new=new_file)

    WINDOW_WIDTH = 400
    WINDOW_HIGHT = 250
    test = None

    def __init__(self, app:ctk.CTk|None = None, dataset:DataSetInfo|None = None, command:Callable[[DataSetInfo],Any]|None = None, register_on_create:bool = True, treat_as_new:bool = False, fg_color: str | Tuple[str] | None = None, **kwargs):
        """
        Creates a new `DataSetConfig` window.\n
        NOTE: The `command` function must be a function that accepts a single positional argument of type `DataSetInfo`\n
        WARNING: This function should only be called by the dataset config `open` method
        """
        super().__init__(master=app,  fg_color=fg_color, **kwargs)
        self.dataset = dataset
        self.command = command
        self.register_on_create = register_on_create
        self.new_dataset = (treat_as_new or dataset is None)

        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HIGHT}")

        # Make and pack elements 
        self.name_text = DatasetNameEdit(self)
        self.name_text.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
        self.file_picker = FilePicker(self)
        self.file_picker.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5,)

        
        self.cancel_button = ctk.CTkButton(self, text="cancel", command=self._on_cancel)
        self.cancel_button.pack(side=ctk.RIGHT, padx=10, pady=5,anchor="se")

        
        self.confirm_button = ctk.CTkButton(self, command=self._on_create)
        self.confirm_button.pack(side=ctk.RIGHT, padx=10, pady=5,anchor="se")

        # Add event handler to catch when user clicks the exit button
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        # Open window (This must be done after all input element have been created)
        self.__open_config(dataset=dataset, command=command, register_on_create=register_on_create, treat_as_new=treat_as_new)

    def __set_dataset(self, dataset:DataSetInfo|None = None, command:Callable[[DataSetInfo],Any]|None = None, treat_as_new:bool = False):
        # Assume that dataset is being edited
        self.dataset = dataset
        self.new_dataset = treat_as_new or dataset is None
        self.command = command
        if self.dataset is None:
            self.dataset = DataSetInfo()

    def __get_action_text(self):
        if self.new_dataset: return "create"
        else: return "update"

    def _on_cancel(self):
        self.dataset = None
        self.__close_config()

    def _on_create(self):

        # TODO Validate input
        
        # Update dataset according to settings
        self.name_text.update_dataset(self.dataset)
        self.file_picker.update_dataset(self.dataset)

        # Note, always register before executing command
        if self.register_on_create:
            GlobalDatasetManager.register(self.dataset)

        # Execute creation command
        if self.command is not None:
            self.command(self.dataset)

        self.__close_config()

    def _configure_title(self):
        if self.new_dataset: self.title("Create Dataset")
        else: self.title("Edit Dataset")

    def __open_config(self,dataset:DataSetInfo|None = None, command:Callable[[DataSetInfo],Any]|None = None, register_on_create:bool = True, treat_as_new:bool = False):
        
        # Ensure that all events are directed to this panel
        self.deiconify()
        self.grab_set()

        # Set the dataset info 
        self.new_dataset = treat_as_new or dataset is None
        self.__set_dataset(dataset,command, treat_as_new=treat_as_new)
        self.register_on_create = register_on_create

        # Set title too correspond with action
        self._configure_title()

        # Configure the input fields (NB use self.dataset not the input dataset which could be None)
        self.file_picker.set_path(self.dataset.get_source_path())
        self.name_text.set_name(self.dataset.get_dataset_name())
        self.confirm_button.configure(text=self.__get_action_text())

    def __close_config(self):
        # Remove reference to dataset so that its memory is freed
        self.dataset = None
        # Redirect events
        self.grab_release()
        # Hide the window
        self.withdraw()