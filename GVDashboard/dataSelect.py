# This script contains classes and features for data selection and filtering UI

from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk

from VCF.dataFetcher import DataFetcher
from VCF.dataWrapper import VcfDataWrapper

# This class is used to select and return files throughout the application
class FileFetcher:
    FETCHED_FILES = []


    # Returns the string path to a user-selected vcf file
    def get_vcf_file()->str:
        filename = ctk.filedialog.askopenfilename(title="Select data file",filetypes=[("Variant call format","*.vcf")])
        if filename not in FileFetcher.FETCHED_FILES:
            FileFetcher.FETCHED_FILES.append(filename)
        return filename

    def get_selected_data()->VcfDataWrapper:
        filename = FileFetcher.get_vcf_file()
        print(filename)
        if filename is not None and filename is not "":
            return DataFetcher.load_data(filename)
        
    
class PathSelect(ctk.CTkOptionMenu):
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, button_color: str | Tuple[str, str] | None = None, button_hover_color: str | Tuple[str, str] | None = None, text_color: str | Tuple[str, str] | None = None, text_color_disabled: str | Tuple[str, str] | None = None, dropdown_fg_color: str | Tuple[str, str] | None = None, dropdown_hover_color: str | Tuple[str, str] | None = None, dropdown_text_color: str | Tuple[str, str] | None = None, font: tuple | ctk.CTkFont | None = None, dropdown_font: tuple | ctk.CTkFont | None = None, values: list | None = None, variable: ctk.Variable | None = None, state: str =NORMAL, hover: bool = True, command: Callable[[str], Any] | None = None, dynamic_resizing: bool = True, anchor: str = "w", **kwargs):
        super().__init__(master, width, height, corner_radius, bg_color, fg_color, button_color, button_hover_color, text_color, text_color_disabled, dropdown_fg_color, dropdown_hover_color, dropdown_text_color, font, dropdown_font, values, variable, state, hover, command, dynamic_resizing, anchor, **kwargs)
        
        # Initialise constants
    def UpdateOptions(self):
        self.configure(values=FileFetcher.FETCHED_FILES)
    