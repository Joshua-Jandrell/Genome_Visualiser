# This script contains base the classes and functions for a plot type selection tkinter menu
from typing import Tuple, Any, Callable
import customtkinter as ctk

from Util.event import Event

from UI.dropDown import DropDown

import UI._ui_config_ as _ui_config_

# An option card that can be displayed in an option list.
# This object must be a child on an OptionList 
class OptionCard(ctk.CTkFrame):
    BUTTON_W = 20
    BUTTON_H = 20
    def __init__(self, master, option_ctrl, option_key:str, option_value=None, width: int = 200, height: int = 90, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None, 
                 toggleable = False, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        assert(isinstance(option_ctrl,OptionCtrl))

        # Set local variables
        self.key = option_key
        self.value = option_value
        self.ctrl = option_ctrl
        self.index = -1 # Holds the grid row/colum of the list managing the option
        self._toggleable = toggleable

        # Even that can be be called whenever the option card or its value are updated
        self.update_event = Event()
        """
        Event that can be be called whenever the option card or its value are updated and should be re-plotted.\n
        Call event using:
        ```python
        self.update_event.invoke(self)
        ```
        """
        self._selected_var = ctk.BooleanVar(value=True)
        # Create panels and buttons
        if not toggleable:
            self.deselected_button = ctk.CTkButton(self,text="x", command=self.deselect, width=self.BUTTON_W, height=self.BUTTON_H)
        else:
            #self.deselected_button = ctk.CTkSwitch(self, text="Active",command=self._toggle)
            self.deselected_button = ctk.CTkCheckBox(self, text="", width=self.BUTTON_W, height=self.BUTTON_H, checkbox_width=self.BUTTON_W, checkbox_height=self.BUTTON_H,
                                                     variable=self._selected_var,
                                                     command=self.__on_button_toggle)
        # Create panel content
        self.content = ctk.CTkFrame(self,fg_color="transparent",width=0, height=self._desired_height-2*self.BUTTON_H) # set width and hight to avoid massive expansion
        # Create label
        self.label = ctk.CTkLabel(self, text=self.key)

        # configure grid
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)

        # Pack items in grid
        self.content.grid(row=1,column=0, rowspan=1,columnspan=2, sticky='nsew', pady = 3, padx=3)
        self.label.grid(row=0, column=0, sticky="w",padx=20, pady=3)
        self.deselected_button.grid(row=0,column=1, padx=5, pady=3)

    def reconfigure_option(self, option_key:str|None = None, option_value=None):
        if option_key is not None:
            self.key = option_key
            self.label.configure(text=option_key)
        if option_value is not None:
            self.value = option_value

        self.update_event.invoke(self)

    def __on_button_toggle(self):
        
        if self._selected_var.get():
            self.toggle_on()
        else:
            self.toggle_off()

    def toggle_on(self):
        if not self._toggleable:
            raise Exception("Attempt to toggle non-toggalabale option card.")
        
        self._selected_var.set(True)
        self.update_event.invoke(self)

    def toggle_off(self):
        if not self._toggleable:
            raise Exception("Attempt to toggle non-toggalabale option card.")
        
        self._selected_var.set(False)
        self.update_event.invoke(self)

    def is_toggleable(self)->bool:
        return self._toggleable

    def is_selected(self)->bool:
        return self._selected_var.get()
    
    def deselect(self):
        self.ctrl.deselect(self)

        if not self._toggleable:
            # Remove all listeners form update event
            self.update_event.remove_all()

            # Set value to be none to avoid hanging references (MUST be done AFTER deselection from control)
            self.value = None 
    def set_value(self,value):
        self.value = value

    def add_listener(self,command):
        """Set a command to be called every time the option card is significantly updated"""
        self.update_event.add_listener(command=command)

    def remove_listener(self,command):
        self.update_event.remove_listener(command=command)

    def destroy(self):
        self.update_event.remove_all()
        return super().destroy()
        


# Class used to spawn in new option panels
class OptionCtrl():
    def __init__(self,option_list,key, option_value:Callable|Any|None = None, option_class:type = OptionCard, toggle_to:bool|None = None):
        """
        Create and option control that will add options to the specified option list.\n
        The option card will be assigned the value of `option_value` or the return value of `option_value` if it is a callable.
        """
        # Constants 
        self.H = 90
        assert(isinstance(option_list,OptionList))

        self.option_list = option_list
        self.key = key
        self.count = 0 # Number of times this option has been selected

        self.__opt_class = option_class
        self.__opt_value = option_value

        # Toggle option on an off if required
        self._toggle_card:OptionCard|None = None
        if toggle_to is not None:
            self._toggle_card = self.select()
        if toggle_to == False:
            # Toggle back off again
            self.deselect(self._toggle_card)


        # Register option control
        option_list.register_option(self)

        

    # Select an option and add it to the option list
    def select(self)->OptionCard:
        if self._toggle_card is None:
            opt = self.make_option_card()
            self.option_list._add_option_card(opt)
        else:
            opt = self._toggle_card
            opt.toggle_on()

        self.count += 1

        return opt

    def deselect(self,opt:OptionCard):

        if opt.is_toggleable():
            if self._toggle_card is None: self._toggle_card = opt
            opt.toggle_off()
        else:
            self.option_list._remove_option_card(opt)
            # delete option permanently
            opt.destroy()

        self.count -= 1


    # Returns true if option is eligible to be selected 
    def is_selectable(self)->bool:
        return True

    def make_option_card(self)->OptionCard:
        """
        Designed to be overridden by descendants to customize option available.\n
        Acts as a factory method for the option panel UI element 
        """
        _value = self.__opt_value
        if _value is None: _value = self.key
        if isinstance(_value, Callable):
            _value = _value()
        return self.__opt_class(self.option_list,self,self.key,_value, height=self.H)
    
    def move_card_up(self,opt:OptionCard):
        if opt.index != 0:
            self.option_list.swap_opts(opt.index, opt.index-1)


# Generic class that holds a list of options which can be added, removed and re-organized
class OptionPanel(ctk.CTkFrame):
    BUTTON_H = 20
    BUTTON_W = 30
    def __init__(self, master, has_swaps:bool|None = True, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, text="Options", add_text="+", **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Class-level constants 
        self._add_text = add_text
        self._text = text

        # Create top label
        self.make_title()
        self.title_txt.grid(row=0,column=0,sticky="ew",padx=20)
        self.__make_add_button()
        self._opt_add_button.grid(row=0,column=1,sticky="")
        # Create content 
        self.content = OptionList(self, has_swaps, opts_update_command=self._on_list_opt_register)
        #self.content.option_count.trace_add("write", self._on_list_opt_register)
        self.content.grid(row=1,column=0,columnspan=2, sticky="nsew")

        # configure grid layout 
        self.grid_columnconfigure(0,weight=7)
        self.grid_columnconfigure(1,weight=3)
        self.grid_rowconfigure(1,weight=1)

    # Returns list of all selected option values from the option list
    def get_opt_values(self)->list[any]:
        return self.content.get_opt_values()

    def _on_list_opt_register(self):
        self.update_dropdown_opts()

    def make_title(self):
        self.title_txt = ctk.CTkLabel(master=self,
                                      text=self._text,
                                      font=_ui_config_.get_h1())
        self.title_txt._font.configure()
        
    # Creates the basic dropdown button to add new plot types
    def __make_add_button(self):
        self.selected_opt = ctk.StringVar()
        self._opt_add_button = DropDown(self,width=self.BUTTON_W, height=self.BUTTON_H,values=[],variable=self.selected_opt,text=self._add_text,command=self.on_add_option_click)
    # Updates the options available on the dropdown
    def update_dropdown_opts(self):
        opt_txt = []
        for key,opt in self.content.opt_ctrls.items():
            assert(isinstance(opt, OptionCtrl))
            opt_txt.append(key)
        
        # Update dropdown
        self._opt_add_button.configure(values=opt_txt)


    def on_add_option_click(self, event):
        self.content.select_option(self.selected_opt.get())
        self.update_dropdown_opts()

    def register_option(self, option_ctrl:OptionCtrl):
        self.content.register(option_ctrl)
        self.update_dropdown_opts()

    def select_option(self,key:str)->OptionCard:
        return self.content.select_option(key=key)




class OptionList(ctk.CTkScrollableFrame):
    def __init__(self, master, has_swaps:bool = True, opts_update_command:Callable[[],Any]|None=None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, overwrite_preferred_drawing_method: str | None = None,
                 toggle_on_register:bool = False,  **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        # Configure local valriables
        self.PAD = 5
        self.opt_ctrls = {}
        self.opts_update_command = opts_update_command # Command called when a new option is registered
        self.active_opt_cards = []
        self.swap_buttons = []
        self.option_index = 0 # the row for the next option to be added 
        self._has_swaps = has_swaps
        self._toggle_on_register = toggle_on_register

        # configure content grid layout
        self.grid_columnconfigure(0,weight=1)

        
        # Create an event to be called when options are updated
        self.update_event = Event()

    def set_toggle_on_register(self,value:bool):
        self._toggle_on_register = value

    def destroy(self):
        self.update_event.remove_all()
        return super().destroy()

    # Select and option and add it to the list
    def select_option(self, key:str):
        return self.opt_ctrls[key].select()

    # Register an option a selectable
    def register_option(self, option_ctrl:OptionCtrl):
        self.opt_ctrls[option_ctrl.key] = option_ctrl

        if self._toggle_on_register:
            _dummy = option_ctrl.select()
            option_ctrl.deselect(_dummy)

        # Invoke the command for option registration
        if self.opts_update_command is not None:
            self.opts_update_command()

    # Returns list of all selected option values from the option list
    def get_opt_values(self)->list[any]:
        vals = []
        for opt in self.active_opt_cards:
            assert(isinstance(opt,OptionCard))
            if opt.is_selected():
                vals.append(opt.value)
        return vals
    
    def get_opt_count(self)->int:
        return len(self.opt_ctrls)
    
    # Function wich adds options to display. Should only be called from an OptionPanel object
    def _add_option_card(self,option:OptionCard):
        # add a swap button
        if self.option_index != 0 and self._has_swaps:
            self._add_swap_button()

        option.grid(row=self.get_opt_grid_row(self.option_index), column=0, sticky="ew",pady=self.PAD, padx=self.PAD)
        option.index = self.option_index
        self.active_opt_cards.append(option)

        self.option_index += 1

        # Add event listener to option card
        option.add_listener(self.__on_card_update)
        # Invoke option update event
        self.update_event.invoke(self,[option])

    def _remove_option_card(self,option:OptionCard):
        target_index = option.index
        # Remove option from active options list
        self.active_opt_cards.remove(option)
        # Remove option from grid
        option.grid_forget()

        # shift all other options up one
        for i in range(target_index,len(self.active_opt_cards)):
            opt = self.active_opt_cards[i]
            assert(isinstance(opt,OptionCard))
            opt.index -= 1
            opt.grid_configure(row=self.get_opt_grid_row(opt.index))

        # Remove swap button
        self._remove_swap_button()

        self.option_index -= 1

        # Remove event listener 
        option.remove_listener(self.__on_card_update)

        # Invoke the the update event
        self.update_event.invoke(self,[option])

    def deselect_all(self):
        """Called to clear the list of all selected options and deselect them."""

        # Note: always remove cards from back, one at a time to avoid unintended behavior as list is resized
        while len(self.active_opt_cards) > 0:
            self._remove_option_card(self.active_opt_cards[-1])

    # Shifts an option panel up one grid column 
    def swap_opts(self,index_1:int, index_2:int):
        opt1 = self.active_opt_cards[index_1]
        opt2 = self.active_opt_cards[index_2]
        self.active_opt_cards[index_1], self.active_opt_cards[index_2] = self.active_opt_cards[index_2], self.active_opt_cards[index_1]
        assert(isinstance(opt1,OptionCard) and isinstance(opt2,OptionCard))

        opt1.index = index_2
        opt1.grid_configure(row=self.get_opt_grid_row(index_2))

        opt2.index = index_1
        opt2.grid_configure(row=self.get_opt_grid_row(index_1))

        # Invoke update event for both options
        self.update_event.invoke(self,[opt1, opt2])

    def _add_swap_button(self):
        swap_button = self._make_swap_button()
        ind_1 = self.option_index
        ind_2 = self.option_index - 1
        swap_button.configure(command=lambda: self.swap_opts(ind_1, ind_2))
        swap_button.grid(row=2*self.option_index-1,column=0,sticky='ew')
        self.swap_buttons.append(swap_button)
    
    def _remove_swap_button(self):
        if len(self.swap_buttons) > 0 and self._has_swaps:
            swap_button = self.swap_buttons.pop()
            assert(isinstance(swap_button, ctk.CTkButton))
            swap_button.grid_forget()
            swap_button.destroy()

    # Function intended to be overriddedn for customisation
    def _make_swap_button(self):
        return ctk.CTkButton(self, text="swap", height=20)
    def get_opt_grid_row(self,index:int)->int:
        if self._has_swaps: return 2*index
        else: return index

    def add_listener(self,command:Callable):
        """
        Add a listener to the option panel update event.\n
        The listener mus accept two arguments, an the option list which changed followed by a list of options card which have changed.
        """
        self.update_event.add_listener(command=command)

    def remove_listener(self,command:Callable):
        """Stop tracking option list updates."""
        self.update_event.remove_listener(command=command)

    def __on_card_update(self,card):
        self.update_event.invoke(self,[card])