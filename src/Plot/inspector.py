"""
Contains definition for the inspector panel used to display data information.
"""

from typing import Any, Tuple
import customtkinter as ctk

class InspectorPanel(ctk.CTkFrame):
    _instance:"InspectorPanel" = None
    @classmethod
    def get_instance(cls)->"InspectorPanel":
        """
        Get the active inspector panel instance
        """
        if cls._instance is None:
            raise RuntimeError("Inspector panel instance not set.")
        
        return cls._instance
        

    @classmethod
    def display_info(cls, info:dict):
        """
        Display all information contained in the info dict.
        """
        instance = cls.get_instance()

        # Clear old labels
        for label in instance._used_labels:
            label.pack_forget()
            #label.grid_forget()
            instance._labels.append(label)

        for key, val in info.items():
            cls.make_label(key,val)

    
    @classmethod
    def make_label(cls, key:str, value:str)->ctk.CTkLabel:
        instance = cls.get_instance()
        txt = f"{key}: \t {value}"
        if len(instance._labels) > 0:
            label = instance._labels.pop()
            label.configure(text=txt)
        else:
            label = ctk.CTkLabel(instance,text=txt)
        

        #label.grid(row=len(instance._used_labels), column=0, sticky='ew')
        label.pack(pady=10)
        instance._used_labels.append(label)

        return label
       
    ### Can make them different values & pack them with a grid similar to the option panel
    ## Add them to labels in use so we can call forget label when done    
        

    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.title_card = ctk.CTkFrame(self,width=width, height=10, fg_color='transparent')
        self.title_card.pack(side=ctk.TOP, fill=ctk.X, pady=0, padx=0)
        self._labels:list[ctk.CTkLabel] = []
        self._used_labels:list[ctk.CTkLabel] = []
        InspectorPanel._instance = self
        

    def destroy(self):
        self._labels.clear()
        return super().destroy()
    