from typing import Any, Tuple, Callable
import customtkinter as ctk 

from UI.numberEntry import NumberEntry      


class FilterFrame(ctk.CTkFrame):
    """
    UI element used to set and end the regional positions 
    """

    def __init__(self, master: Any, command:Callable[[int,int,int], None]|None = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        """
        Command will be called with arguments chromosome, min_pos and max_pos
        """
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Tkinter variables
        self.chromo = ctk.IntVar()
        self.pos_min = ctk.IntVar()
        self.pos_max = ctk.IntVar()
        self.qual_min = ctk.DoubleVar()
        self.qual_max = ctk.DoubleVar()

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

    




    def __on_chromo_change(self, value):
        print(f"Set chromo to {value}")


