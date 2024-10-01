from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk
from customtkinter import ThemeManager
from os import path

from .tooltip import ToolTip

class FilePicker(ctk.CTkFrame):
    """
    Class used to let the user select files.
    """
    def __init__(self, master: Any, width: int = 200, height: int = 28, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, command:Callable[[],str]=None, filetypes:list[tuple[str,str]]=[("All files", "*")], button_text:str|None="select", clear_text:str|None="clear", default_text:str|None = "[No file.]", path_variable:ctk.StringVar|None =None, clear_button:bool = False, **kwargs):
        # Intercept styling
        # if border_color is None:
        #     border_color = ThemeManager.theme['CTkEntry']['border_color']
        # if border_width is None:
        #     border_width = ThemeManager.theme['CTkEntry']['border_width']
        # if corner_radius is None:
        #     corner_radius = ThemeManager.theme['CTkEntry']['corner_radius']
        
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self._path_variable = path_variable
        self._label = ctk.CTkLabel(self, height=height-2*self._border_width, text=default_text)
        self._label.grid(row=0, column=0, pady=self._border_width)
        
        self._button = ctk.CTkButton(self, width = 40, height=height, 
                                     corner_radius=corner_radius,
                                     border_color=self._border_color,
                                     border_width=self._border_width,
                                     command=self.__open_path_select,
                                     text=button_text)
        self._button.grid(row=0, column=1)

        if clear_button:
            self._clear_button = ctk.CTkButton(self, width = 40, height=height, 
                                        corner_radius=corner_radius,
                                        border_color=self._border_color,
                                        border_width=self._border_width,
                                        command=self.clear_path, 
                                        text=clear_text)
            self._clear_button.grid(row=0, column=2)
        else: self._clear_button = None

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure([1,2],weight=0)
        
        self._command = command
        command = self.__open_path_select
        
        self._filetypes = filetypes
        self._file_text = default_text
        self.path_tooltip = ToolTip(self, text=None)

        self.__path_var_callback__ = None
        if self._path_variable is not None:
            self.__path_var_callback__ = self._path_variable.trace_add('write', self.__on_path_change_var)

    def destroy(self):
        if self.__path_var_callback__ is not None:
            self._path_variable.trace_remove('write', self.__path_var_callback__)
        return super().destroy()

    def __open_path_select(self):
        _filepath = ctk.filedialog.askopenfilename(title=self._file_text, filetypes=self._filetypes)
        if _filepath == "": return
        self.set_path(_filepath)

    def __on_path_change_var(self,*args):
        self.set_path(self._path_variable.get())

        

    def set_path(self, file_path:str, __ignore_path_var__ = False):
        
        if file_path == "": 
            self.clear_path()
            return
        
        # Update name variable
        if not __ignore_path_var__ and self._path_variable is not None:
            self._path_variable.set(file_path)

        # Update label text 
        _filename = path.basename(path.realpath(file_path))
        self._label.configure(text=_filename)

        # Update tooltip
        self.path_tooltip.set_text(file_path)

        if self._command is not None:
            self._command(file_path)

    def clear_path(self):
        self._path_variable.set("")
        self.path_tooltip.set_text("")
        self._label.configure(text=self._file_text)
    
    def configure(self, require_redraw=False, command:Callable[[], str]|None = None, **kwargs):
        if command is not None: self._command = command
        return super().configure(require_redraw, **kwargs)
