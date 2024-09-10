# This script contains the definition for the data select dropdown class

from typing import Any, Callable
from customtkinter import CTkFont, Variable
import customtkinter as ctk

from VCF.gloabalDatasetManger import GlobalDatasetManager
from VCF.filterInfo import DataSetInfo
from VCF.dataSetConfig import DataSetConfig

class DatasetMenu(ctk.CTkOptionMenu):
    """
    Special instance of `CTkOptionMenu` class that contains a list of all active datasets.\n
    This list is automatically updated from the `GlobalDatasetManager`.
    """
    NO_VALUE_TXT = "None"
    UNSELECTED_VALUE = "Select"
    NEW_TXT = "New..."
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, button_color: str | tuple[str, str] | None = None, button_hover_color: str | tuple[str, str] | None = None, text_color: str | tuple[str, str] | None = None, text_color_disabled: str | tuple[str, str] | None = None, dropdown_fg_color: str | tuple[str, str] | None = None, dropdown_hover_color: str | tuple[str, str] | None = None, dropdown_text_color: str | tuple[str, str] | None = None, font: tuple | CTkFont | None = None, dropdown_font: tuple | CTkFont | None = None, values: list | None = None, variable: Variable | None = None, state: str = ..., hover: bool = True, command: Callable[[str], Any] | None = None, dynamic_resizing: bool = True, anchor: str = "w", **kwargs):
        super().__init__(master, width, height, corner_radius, bg_color, fg_color, button_color, button_hover_color, text_color, text_color_disabled, dropdown_fg_color, dropdown_hover_color, dropdown_text_color, font, dropdown_font, values, variable, state, hover, command, dynamic_resizing, anchor, **kwargs)

        # Configure dataset options
        self.active_options = True
        dataset_names = GlobalDatasetManager.get_dataset_names()
        self.__update_options(dataset_names)

        # Intercept own command 
        self.__true_command = self._command
        self.configure(command = self.__on_command)

        # Register new dropdown with global dataset manager 
        GlobalDatasetManager.add_listener(self.__update_options)
    def __on_command(self,event):
        # Check if command is "new"
        if self.get() is DatasetMenu.NEW_TXT:
            DataSetConfig.open(command = self.__on_data_config)
        else:
            self.__true_command(event)

    def __on_data_config(self, dataset_info:DataSetInfo):
        GlobalDatasetManager.register(dataset_info)
        self.set(dataset_info.get_dataset_name())
        self._command(dataset_info.get_dataset_name())

    def get_selected_dataset(self)->str|None:
        """
        Returns the dataset selected by the option menu.\n
        WARNING: Do not keep a reference to the dataset returned by this method as it will prevent the dataset from being deleted.
        """
        dataset_name =  self.get() 
        if dataset_name is not DatasetMenu.NO_VALUE_TXT and dataset_name is not DatasetMenu.UNSELECTED_VALUE:
            return GlobalDatasetManager.get_dataset_by_name(dataset_name)
        else: return None

    def __update_options(self, dataset_names):
        """Updates the dropdown options to include all datasets."""
        # Configure dropdown options
        self.configure(values = dataset_names + [DatasetMenu.NEW_TXT])


        # Add divider between new options button and other datasets
        if len(dataset_names) != 0:
            # select last dataset added
            self.set(dataset_names[-1])
            self._dropdown_menu.insert_separator(len(dataset_names))

        if not self.get() in dataset_names:
            self.set(DatasetMenu.UNSELECTED_VALUE)
             # invoke command to reconfigure dataset for all listeners 
            self._command(self.get())


    def __deregister_listener(self):
        """Remove event listener for this dropdown."""
        GlobalDatasetManager.remove_listener(self.__update_options)

    # Overridden destroy command to deregister dataset
    def destroy(self):
        self.__deregister_listener()
        return super().destroy()