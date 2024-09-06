# This script contains classes and features for data selection and filtering UI

from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk
from os import path

from VCF.dataFetcher import DataFetcher
from VCF.dataWrapper import VcfDataWrapper
from VCF.filterInfo import DataSetInfo

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
        print(filename)
        if filename is not None and filename != "":
            return DataFetcher.load_data(filename)

FIELD_LABEL_PADDING = 20
def make_field_label(master,text:str)->ctk.CTkLabel:
    "Create a text label for the dataset creator fields"
    label =ctk.CTkLabel(master,text=text)
    label._font.configure(weight="bold")

    return label

class FilePicker(ctk.CTkFrame):
    "Class used to select and validate files for selection"

    MAX_PATH_CHARS = 20
    def __init__(self, master: Any, dataset:DataSetInfo, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        # Initialise constans
        self.path_var = ctk.StringVar(value="No path selected...")
        self.dataset = dataset
        self._path_value = ""

        # Create and pack elements 
        self.label = make_field_label(self,text="Source File:")
        self.label.pack(side=ctk.LEFT, padx=FIELD_LABEL_PADDING)

        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx = 0)
        self.path_txt = ctk.CTkLabel(self.path_frame,text="No file selected...",anchor="w", justify=ctk.LEFT)
        self.path_txt.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx = 10)
        #self.path_txt = ctk.CTkOptionMenu(self,values=["one", "tow", "tree"])
        self.file_button = ctk.CTkButton(self, text="select", command=self.user_update_path, width=40)
        self.file_button.pack(side=ctk.LEFT)
        self.path_tooltip = ToolTip(self.path_txt, text=None)

        self.path_var.trace_add('write',self.on_file_change)
    def on_file_change(self, *args):
        path = self.path_var.get()
        if path == "": return
        
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

    def update_dataset(self):
        if self._path_value == "": return
        self.dataset.configure(source_path=self._path_value)

class DatasetNameEdit(ctk.CTkFrame):
    "Class used to edit the name of a dataset"

    def __init__(self, master: Any, dataset:DataSetInfo, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self.dataset = dataset
        self.name_var = ctk.StringVar(value=dataset.name)

        # Create and pack elements 
        self.label = make_field_label(self, text="Name: ")
        self.label.pack(side=ctk.LEFT, padx=FIELD_LABEL_PADDING)

        self.name_entry = ctk.CTkEntry(self,textvariable=self.name_var)
        self.name_entry.pack(side=ctk.LEFT)
        
    def update_dataset(self):
        self.dataset.configure(name=self.name_var.get())

    
        
    
class DataSetConfig(ctk.CTkToplevel):
    WINDOW_WIDTH = 400
    WINDOW_HIGHT = 250

    dateset_count = 0
    datasets = []
    def __init__(self, app:ctk.CTk, dataset:DataSetInfo|None = None,fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(master=app,  fg_color=fg_color, **kwargs)
        # Assume that dataset is being edited
        self.dataset = dataset
        self.new_dataset = False
        action_text = "Update"
        if self.dataset is None:
            self.new_dataset = True
            self.dataset = DataSetInfo(name=f"Dataset_{self.dateset_count+1}")
            action_text = "Create"

        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HIGHT}")
        self._configure_title()
        # Ensure that all events are directed to this panel
        self.grab_set()

        # Make and pack elements 
        self.name_text = DatasetNameEdit(self,self.dataset)
        self.name_text.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
        self.file_picker = FilePicker(self,self.dataset)
        self.file_picker.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5,)


        self.cancel_button = ctk.CTkButton(self, text="cancel", command=self._on_cancel)
        self.cancel_button.pack(side=ctk.RIGHT, padx=10, pady=5,anchor="se")
        self.confirm_button = ctk.CTkButton(self, text=action_text)
        self.confirm_button.pack(side=ctk.RIGHT, padx=10, pady=5,anchor="se")

    def _on_cancel(self):
        self.destroy()

    def _on_create(self):
        self.name_text.update_dataset()
        self.file_picker.update_dataset()
        self.destroy()

    def _configure_title(self):
        if self.new_dataset: self.title("Create Dataset")
        else: self.title("Edit Dataset")




    