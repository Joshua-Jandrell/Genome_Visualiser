from typing import Any, Tuple, Callable
import customtkinter as ctk 

from UI.numberEntry import NumberEntry  
from UI.filePicker import FilePicker    
from VCF.filterInfo import DataSetInfo


class DatasetFilterFrame(ctk.CTkFrame):
    """
    UI element used to set and end the regional positions 
    """

    def __init__(self, master: Any, dataset:DataSetInfo|None = None, auto_update=True, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        """
        Command will be called with arguments chromosome, min_pos and max_pos.
        If auto update is set to true the dataset will be automatically updated when values change.
        """
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Tkinter variables
        self.chromo = ctk.IntVar()
        self.pos_min = ctk.IntVar()
        self.pos_max = ctk.IntVar()
        self.qual_min = ctk.DoubleVar()
        self.qual_max = ctk.DoubleVar()
        self.case_ctrl_path = ctk.StringVar(value="")

        # NOTE dataset should only be set after variable have been constructed
        self.set_dataset(dataset)

        # Track variable changes if required
        self.__chrom_call__ = self.chromo.trace_add('write', self.__on_chromo_change)
        self.__min_pos_call__ = self.pos_min.trace_add('write', self.__on_min_pos_change)
        self.__max_pos_call__ = self.pos_max.trace_add('write', self.__on_max_pos_change)
        self.__qual_min_call__ = self.qual_min.trace_add('write', self.__on_qual_change)
        self.__qual_max_call__ = self.qual_max.trace_add('write', self.__on_qual_change)
        self.__case_ctrl_call__ = self.case_ctrl_path.trace_add('write', self.__on_case_ctrl_change)
        
        # ==== Regional UI elements ====
        chromo_label = ctk.CTkLabel(self, text="Chromosome:")
        chromo_label._font.configure(weight="bold")
        self.chromo_value = NumberEntry(self, width=30, number_variable=self.chromo)

        range_label = ctk.CTkLabel(self, text="Position:")
        range_label._font.configure(weight="bold")
        #range_min_label = ctk.CTkLabel(self, text="From")
        range_min = NumberEntry(self, width=90, number_variable=self.pos_min)
        range_max_label = ctk.CTkLabel(self, text="to")
        range_max = NumberEntry(self, width=90, number_variable=self.pos_max)
        range_max.set_as_above(range_min)

        # Pack UI elements
        _padx = 5
        _pady = 5
        chromo_label.grid(row=0, column=0, padx=_padx, columnspan=1)
        self.chromo_value.grid(row=0, column=1,padx=_padx)

        range_label.grid(row=1, column=0,padx=_padx)
        #range_min_label.grid(row=1, column=2,padx=_padx)
        range_min.grid(row=1, column=1,padx=_padx)
        range_max_label.grid(row=1, column=2)
        range_max.grid(row=1, column=3, padx=_padx)

        # ==== Quality UI elements ====
        qual_label = ctk.CTkLabel(self, text="Quality:")
        qual_label._font.configure(weight="bold")
        self.qual_min_entry = NumberEntry(self, width=60, value=0, value_range=(0,100), number_variable=self.qual_min)
        qual_max_label = ctk.CTkLabel(self, text="to")
        self.qual_max_entry = NumberEntry(self, width=60, value=100, value_range=(0,100), number_variable=self.qual_max)
        self.qual_max_entry.set_as_above(self.qual_min_entry)

        _qual_row = 2
        qual_label.grid(row=_qual_row, column=0)
        self.qual_min_entry.grid(row=_qual_row, column=1, padx=_padx)
        qual_max_label.grid(row=_qual_row, column=2, padx=0)
        self.qual_max_entry.grid(row=_qual_row, column=3, padx=_padx)

        # ==== case control elements ====
        _case_ctrl_row = 3
        case_ctrl_label = ctk.CTkLabel(self, text="Case/Ctrl:")
        case_ctrl_label._font.configure(weight="bold")
        case_ctrl_label.grid(row=_case_ctrl_row, column=0, columnspan=1, padx=_padx, pady=_pady)
        self.case_ctrl_picker = FilePicker(master=self, width=100,
                                           filetypes=[("Case/Ctrl text file", "*.txt")],
                                           path_variable=self.case_ctrl_path,
                                           button_text="select",
                                           clear_button=True
                                           )
        self.case_ctrl_picker.grid(row=_case_ctrl_row, column=1, columnspan=3, padx=_padx, sticky='ew')

    

    def destroy(self):
        self.dataset = None           
        self.chromo.trace_remove('write', self.__chrom_call__)
        self.pos_min.trace_remove('write', self.__min_pos_call__)
        self.pos_max.trace_remove('write', self.__max_pos_call__)
        self.qual_min.trace_remove('write', self.__qual_min_call__)
        self.qual_max.trace_remove('write', self.__qual_max_call__)
        self.case_ctrl_path.trace_remove('write', self.__case_ctrl_call__)
        return super().destroy()
    
    def set_dataset(self, dataset:DataSetInfo|None):
        self.dataset = dataset
        if dataset is None: return

        # Update variables to match dataset
        self.chromo.set(dataset.get_chromosome())
        _min, _max = dataset.get_range()
        self.pos_min.set(_min)
        self.pos_max.set(_max)
        _min, _max = dataset.get_quality()
        self.qual_min.set(_min)
        self.qual_max.set(_max)

    def update_all(self):
        """
        Update all datawrapper values.
        """
        self.__on_chromo_change()
        self.__on_max_pos_change()
        self.__on_min_pos_change()
        self.__on_qual_change()

    def __on_chromo_change(self, *args):
        if self.dataset is not None:
            self.dataset.set_range(chromosome=self.chromo.get())
    def __on_min_pos_change(self, *args):
        if self.dataset is not None:
            self.dataset.set_range(min=self.pos_min.get())
    def __on_max_pos_change(self, *args):
        if self.dataset is not None:
            self.dataset.set_range(max=self.pos_max.get())
    def __on_qual_change(self, *args):
        if self.dataset is not None:
            self.dataset.set_quality(min=self.qual_min.get(), max=self.qual_max.get())
    def __on_case_ctrl_change(self, *args):
        if self.dataset is not None:
            self.dataset.set_case_ctrl(self.case_ctrl_path.get())


