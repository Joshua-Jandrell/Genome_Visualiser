from typing import Any, Tuple
from os import path

import customtkinter as ctk

from VCF.dataWrapper import VcfDataWrapper
from VCF.filterInfo import DataSetInfo
from UI.tooltip import ToolTip

class FileFetcher:
    FETCHED_FILES = []

    # Returns the string path to a user-selected vcf file
    def get_vcf_filename()->str:
        filename = ctk.filedialog.askopenfilename(title="Select data file",filetypes=[("Variant call format","*.vcf *.vcf.gz")])
        if filename == "": return ""
        if filename not in FileFetcher.FETCHED_FILES:
            FileFetcher.FETCHED_FILES.append(filename)
        return filename

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

class DatasetFileFrame(ctk.CTkFrame):
    """
    Frame used to let users select dataset files and case control files
    """
    def __init__(self, master: Any, dataset:DataSetInfo|None = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
                # Make and pack elements 
        self.name_text = DatasetNameEdit(self)
        self.name_text.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
        self.file_picker = FilePicker(self)
        self.file_picker.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5)

        self.set_dataset(dataset)

    def set_dataset(self, dataset:DataSetInfo|None):
        self.dataset = dataset
        if dataset is None: return
        
        self.file_picker.set_path(self.dataset.get_source_path())
        self.name_text.set_name(self.dataset.get_dataset_name())


    def update_all(self):
        self.name_text.update_dataset(self.dataset)
        self.file_picker.update_dataset(self.dataset)