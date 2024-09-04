# This script contains base the classes and functions for a plot type selection tkinter menu

from typing import Tuple
import customtkinter as ctk
import tkinter as tk

from UI.dropDown import DrowDown

# An option panel that can be added to an option list  
# This object must be a chid on a OptionList 
class OptionPanel(ctk.CTkFrame):
    BUTTON_W = 20
    BUTTON_H = 20
    def __init__(self, master, option_ctrl, option_key:str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        assert(isinstance(option_ctrl,OptionCtrl))

        # Set local variables
        self.key = option_key
        self.value = option_value
        self.ctrl = option_ctrl
        self.index = -1 # Holds the grid row/colum of the list managing the option

        # Create panels and buttons
        self.remove_button = ctk.CTkButton(self,text="x", command=self.deselect, width=self.BUTTON_W, height=self.BUTTON_H)
        # Create panel content
        self.content = ctk.CTkFrame(self,fg_color="transparent",width=0, height=self._desired_height-2*self.BUTTON_H) # set width and hight to avoid massive expansion
        # Create label
        self.label = ctk.CTkLabel(self, text=self.key)

        # configure grid
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)

        # Pack items in grid
        self.content.grid(row=1,column=0, rowspan=1,columnspan=2, sticky='nsew')
        self.label.grid(row=0, column=0, sticky="w",ipadx=20)
        self.remove_button.grid(row=0,column=1)


    def deselect(self):
        self.ctrl.deselect(self)


        


# Class used to spawn in new option panels
class OptionCtrl():
    def __init__(self,option_list,key):
        # Constants 
        self.H = 90
        assert(isinstance(option_list,OptionList))

        self.option_list = option_list
        self.key = key
        self.count = 0 # Number of times this option has been selected

        # Register option control
        option_list.register_option(self)

    # Select an option and add it to the option list
    def select(self):
        opt = self.make_option_panel()
        self.option_list._add_option_panel(opt)
        self.count += 1

    def deselect(self,opt:OptionPanel):
        self.option_list._remove_option_panel(opt)
        self.count -= 1

        # delete option permanently
        opt.destroy()

    # Returns true if option is eligible to be selected 
    def is_selectable(self)->bool:
        return True

    # Designed to be overridden by descendants to customize option available
    # Acts as a factory method for the option panel UI element 
    def make_option_panel(self)->OptionPanel:
        return OptionPanel(self.option_list.content,self,self.key,self.key, height=self.H)
    
    def move_panel_up(self,opt:OptionPanel):
        if opt.index != 0:
            self.option_list.swap_opts(opt.index, opt.index-1)

        



class OptionList(ctk.CTkFrame):
    def __init__(self, master, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Class-level constants 
        self.ADD_TXT = "Add plot"
        self.PLOT_TXT = "Options"
        self.PAD = 5

        # Coningure local valriables
        self.opts = {}
        self.active_opts = []
        self.swap_buttons = []
        self.option_index = 0 # the row for the next option to be added 

        # Create top label
        self.make_title()
        self.make_add_button()
        # Create content 
        self.content = ctk.CTkFrame(self)

        # Position objects in grid
        self.title_txt.grid(row=0,column=0,sticky="ew",padx=20)
        self.opt_button.grid(row=0,column=1,sticky="")
        self.content.grid(row=1,column=0,columnspan=2, sticky="nsew")

        # configure grid layout 
        self.grid_columnconfigure(0,weight=7)
        self.grid_columnconfigure(1,weight=3)
        self.grid_rowconfigure(1,weight=1)

        # configure content grid layout
        self.content.grid_columnconfigure(0,weight=1)

    # Returns list of all selected option values from the option list
    def get_opt_values(self)->list[any]:
        vals = []
        for opt in self.active_opts:
            assert(isinstance(opt,OptionPanel))
            vals.append(opt.value)
        return vals


    def make_title(self):
        self.title_txt = ctk.CTkLabel(master=self,
                                      text=self.PLOT_TXT)
        
    # Creates the basic dropdown button to add new plot types
    def make_add_button(self):
        self.selected_opt = ctk.StringVar()
        self.opt_button = DrowDown(self,values=[],variable=self.selected_opt,text=self.ADD_TXT,command=self.on_add_option_click)

    # Updates the options available on the dropdown
    def update_dropdown_opts(self):
        opt_txt = []
        for key,opt in self.opts.items():
            assert(isinstance(opt, OptionCtrl))
            opt_txt.append(key)
        
        # Update dropdown
        self.opt_button.configure(values=opt_txt)


    def on_add_option_click(self, event):
        self.opts[self.selected_opt.get()].select()
        self.update_dropdown_opts()

    def register_option(self, option_ctrl:OptionCtrl):
        self.opts[option_ctrl.key] = option_ctrl
        self.update_dropdown_opts()

    # Function wich adds options to display. Should only be called from an OptionPanel object
    def _add_option_panel(self,option:OptionPanel):
        # add a swap button
        if self.option_index != 0:
            self._add_swap_button()

        option.grid(row=2*self.option_index, column=0, sticky="ew",pady=self.PAD, padx=self.PAD)
        option.index = self.option_index
        self.active_opts.append(option)



        self.option_index += 1

    def _remove_option_panel(self,option:OptionPanel):
        target_index = option.index
        # Remove option from active options list
        self.active_opts.remove(option)
        # Remove option from grid
        option.grid_forget()

        # Remove swap button
        self._remove_swap_button()

        self.option_index -= 1

        # shift all other options up one
        for i in range(target_index+1,len(self.active_opts)):
            opt = self.active_opts[i]
            assert(isinstance(opt,OptionPanel))
            opt.index -= 1
            opt.grid_configure(row=opt.index)

    # Shifts an option panel up one grid column 
    def swap_opts(self,index_1:int, index_2:int):
        opt1 = self.active_opts[index_1]
        opt2 = self.active_opts[index_2]
        self.active_opts[index_1], self.active_opts[index_2] = self.active_opts[index_2], self.active_opts[index_1]
        assert(isinstance(opt1,OptionPanel) and isinstance(opt2,OptionPanel))

        opt1.index = index_2
        opt1.grid_configure(row=2*index_2)

        opt2.index = index_1
        opt2.grid_configure(row=2*index_1)


    def _add_swap_button(self):
        swap_button = self._make_swap_button()
        ind_1 = self.option_index
        ind_2 = self.option_index - 1
        swap_button.configure(command=lambda: self.swap_opts(ind_1, ind_2))
        swap_button.grid(row=2*self.option_index-1,column=0,sticky='ew')
        self.swap_buttons.append(swap_button)
    
    def _remove_swap_button(self):
        if len(self.swap_buttons) > 0:
            swap_button = self.swap_buttons.pop()
            assert(isinstance(swap_button, ctk.CTkButton))
            swap_button.grid_forget()
            swap_button.destroy()

    # Function intended to be overriddedn for customisation
    def _make_swap_button(self):
        return ctk.CTkButton(self.content, text="swap", height=20)