# This script contains the definition for the data select dropdown class

from typing import Any, Callable
from customtkinter import CTkFont, Variable
import customtkinter as ctk

from VCF.gloabalDatasetManger import GlobalDatasetManager
from VCF.filterInfo import DataSetInfo

class DatasetMenu(ctk.CTkOptionMenu):
    """
    Special instance of `CTkOptionMenu` class that contains a list of all active datasets.\n
    This list is automatically updated from the `GlobalDatasetManager`.
    """
    NO_VALUE_TXT = "None"
    UNSELECTED_VALUE = "Select"
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, bg_color: str | tuple[str, str] = "transparent", fg_color: str | tuple[str, str] | None = None, button_color: str | tuple[str, str] | None = None, button_hover_color: str | tuple[str, str] | None = None, text_color: str | tuple[str, str] | None = None, text_color_disabled: str | tuple[str, str] | None = None, dropdown_fg_color: str | tuple[str, str] | None = None, dropdown_hover_color: str | tuple[str, str] | None = None, dropdown_text_color: str | tuple[str, str] | None = None, font: tuple | CTkFont | None = None, dropdown_font: tuple | CTkFont | None = None, values: list | None = None, variable: Variable | None = None, state: str = ..., hover: bool = True, command: Callable[[str], Any] | None = None, dynamic_resizing: bool = True, anchor: str = "w", **kwargs):
        super().__init__(master, width, height, corner_radius, bg_color, fg_color, button_color, button_hover_color, text_color, text_color_disabled, dropdown_fg_color, dropdown_hover_color, dropdown_text_color, font, dropdown_font, values, variable, state, hover, command, dynamic_resizing, anchor, **kwargs)

        # Configure dataset options
        dataset_names = GlobalDatasetManager.get_dataset_names()
        self.configure(values=dataset_names)
        self.active_options = True
        if len(dataset_names) > 0:
            # Set value to the last dataset selected
            self.set(dataset_names[-1])
        else:
            self.__on_no_datasets()

        # Register new dropdown with global dataset manager 
        GlobalDatasetManager.add_listener(self.__update_options)
        print(dataset_names)

    def get_selected_dataset(self)->str|None:
        """
        Returns the dataset selected by the option menu.\n
        WARNING: Do not keep a reference to the dataset returned by this method as it will prevent the dataset from being deleted.
        """
        dataset_name =  self.get() 
        if dataset_name is not DatasetMenu.NO_VALUE_TXT and dataset_name is not DatasetMenu.UNSELECTED_VALUE:
            return dataset_name
        else: return None

    def __update_options(self, dataset_names):
        """Updates the dropdown options to include all datasets."""
        # Configure dropdown options
        self.configure(values = dataset_names)

        if len(dataset_names) == 0:
            self.__on_no_datasets()
        elif self.active_options is False:
            self.configure(state='active')
            self.set(DatasetMenu.UNSELECTED_VALUE)
        elif not self.get() in dataset_names:
            self.set(DatasetMenu.UNSELECTED_VALUE)

    def __on_no_datasets(self):
        """Method called when there are no dataset option available."""
        self.set(DatasetMenu.NO_VALUE_TXT)
        self.configure(state="disabled")
        self.active_options = False

    def __deregister_listener(self):
        """Remove event listener for this dropdown."""
        GlobalDatasetManager.remove_listener(self.__update_options)

    # Overridden destroy command to deregister dataset
    def destroy(self):
        self.__deregister_listener()
        return super().destroy()