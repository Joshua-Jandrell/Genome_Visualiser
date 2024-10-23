from typing import Any, Callable, Tuple
from os import path

import customtkinter as ctk

from VCF.filterInfo import DataSetInfo
from UI.filePicker import FilePicker

class FileFetcher:
    SUPPORTED_TYPES = [('All','*.vcf *.vcf.gz *.bcf *.bcf.gz'),
                       ('Variant call format','*.vcf *.vcf.gz'),
                       ('Binary call format','*.bcf *.bcf.gz')]

    # Returns the string path to a user-selected vcf file
    def get_vcf_filename()->str:
        return ctk.filedialog.askopenfilename(title="Select data file",filetypes=FileFetcher.SUPPORTED_TYPES)


FIELD_LABEL_PADDING = 20
def make_field_label(master,text:str)->ctk.CTkLabel:
    "Create a text label for the dataset creator fields"
    label =ctk.CTkLabel(master,text=text)
    label._font.configure(weight="bold")

    return label

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
        self.name_text = DatasetNameEdit(self, fg_color='transparent')
        self.name_text.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)

        # Make dataset file picker
        self.path_var = ctk.StringVar()

        # Create and pack elements 
        self.label = make_field_label(self,text="Source File:")
        self.label.pack(side=ctk.LEFT, padx=FIELD_LABEL_PADDING)

        self.picker = FilePicker(self, command=self.__on_dataset_file_change, path_variable=self.path_var,
                                 filetypes=FileFetcher.SUPPORTED_TYPES)
        self.picker.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx = 0)

        self.set_dataset(dataset)

    def __on_dataset_file_change(self,new_file):
        self.dataset.configure(source_path=new_file)

    def set_dataset(self, dataset:DataSetInfo|None):
        self.dataset = dataset
        if dataset is None: return
        
        self.path_var.set(self.dataset.get_source_path())
        self.name_text.set_name(self.dataset.get_dataset_name())


    def update_all(self):
        self.name_text.update_dataset(self.dataset)
        self.dataset.configure(source_path=self.path_var.get())