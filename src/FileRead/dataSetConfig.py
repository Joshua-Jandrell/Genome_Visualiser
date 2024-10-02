# This script contains classes and features for data selection and filtering UI

from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk
from os import path
import tkinter as tk

from VCF.dataWrapper import VcfDataWrapper
from VCF.filterInfo import DataSetInfo
from VCF.globalDatasetManger import GlobalDatasetManager

from VCF.datasetEditFrames import DatasetFilterFrame, DatasetFileFrame, FileFetcher


# This class is used to select and return files throughout the application

        
    
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
    WINDOW_HIGHT = 300

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

        self.file_frame = DatasetFileFrame(self)
        self.file_frame.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5)
        # Track file path change event
        
        self.filter_frame = DatasetFilterFrame(self, dataset=dataset)
        self.filter_frame.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5)

        
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
        self.filter_frame.update_all()
        self.file_frame.update_all()


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

        self.filter_frame.set_dataset(dataset)
        self.file_frame.set_dataset(dataset)
        self.confirm_button.configure(text=self.__get_action_text())

    def __close_config(self):
        # Remove reference to dataset so that its memory is freed
        self.dataset = None

        # Clear dataset from panels
        self.filter_frame.set_dataset(None)
        self.file_frame.set_dataset(None)

        # Redirect events
        self.grab_release()
        # Hide the window
        self.withdraw()