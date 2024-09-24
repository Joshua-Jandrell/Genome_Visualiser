from tkinter.constants import NORMAL
from typing import Any, Tuple
import customtkinter as ctk

class NumberEntry(ctk.CTkEntry):
    """Special ctk variable that can only hold a numerical value."""
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, text_color: str | Tuple[str, str] | None = None, placeholder_text_color: str | Tuple[str, str] | None = None, number_variable: ctk.DoubleVar | ctk.IntVar | None = None, value: float | None = None, value_range: tuple[float|None, float|None] = (0,None), is_int:bool = False, instant_validate:bool = False, placeholder_text: str | None = None, font: tuple | ctk.CTkFont | None = None, state: str = NORMAL, **kwargs):
        
        self.is_int = is_int
        if isinstance(number_variable, ctk.DoubleVar) or isinstance(number_variable, ctk.IntVar):
            self._number_variable = number_variable
            self.is_int = isinstance(number_variable, ctk.IntVar)
        elif self.is_int:
            self._number_variable = ctk.IntVar(value=0)
        else:
            self._number_variable = ctk.DoubleVar(value=0)
        
        # Create text variable to manage the input box 
        textvariable = ctk.StringVar(value='0')
        
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, text_color, placeholder_text_color, textvariable, placeholder_text, font, state, **kwargs)

        self._instant_validate = instant_validate
        if value is not None:
            if not self.is_int: value = float(value)
            else: value = int(value)
            textvariable.set(f"{value}")

        self.min, self.max = value_range
        self.entry_above:'NumberEntry'|None = None
        self.entry_below:'NumberEntry'|None = None

        self.__setting_flag = False
        """
        set to `True` when this element is busy settings is own value.
        """

        self.__read_input()
        
        # Add trace to command to see when text is changed
        textvariable.trace_add(mode="write", callback=self.__read_input)

        # Bind focus event to validate input when user is finished editing
        self.bind("<FocusOut>", self.__on_focus_out)

        def destroy():
            textvariable.trace_remove(mode="write", callback=self.__read_input)
            self.unbind("<FocusOut>", self.__on_focus_out)
            super().destroy()

    def __read_input(self, *args):
        # Do nothing is currently busy setting this input
        if self.__setting_flag: return
        self.__setting_flag = True

        _value = self._textvariable.get()

        # construct string of only numerical input characters 
        _numerical_str =  "".join([c for c in _value if c.isdigit() or (c == '.' and not self.is_int) or c == '-'])

        #  Store string valarie to set as display text
        _new_value =  _numerical_str
            
        # Ensure that number value is always a valid number, even when number sting is empty.
        if _numerical_str in ["", "-", "."]: _numerical_str = '0'  
        # Get the numerical value of number string
        _number_value = float(_numerical_str) 

        # Check that value is in range
        _new_number_value = self.__in_range(_number_value)
        if _new_number_value != self._number_variable.get():
            self._number_variable.set(_new_number_value) 

        if self._instant_validate:
            # update text value if previous sting was invalid
            if _new_number_value != _number_value:
                _new_value = str(_new_number_value)

        # Update text variable if required
        if _value != _new_value:
            self._textvariable.set(_new_value)

        self.__setting_flag = False

    def __on_focus_out(self, *args):
        valid_value = self._number_variable.get() # note: the number value should always be valid
        if self.is_int: valid_value = int(valid_value)
        if str(valid_value) != self._textvariable.get():
            self._textvariable.set(str(valid_value))


    def __in_range(self,value:float)->float|int:
        if self.entry_below is not None:
            value = max(self.entry_below.get(), value)
        if self.min is not None:
            value = max(self.min, value)
        if self.entry_above is not None:
            value = min(self.entry_above.get(), value)
        if self.max is not None:
            value = min(self.max, value)
        return value
    
    def get(self)->float|int:
        """Returns the numerical value of the number entry."""
        return self._number_variable.get()
    
    def set_as_above(self, other:'NumberEntry'):
        """
        Set the value of this number entry to always be above the value in the `other` numerical entry.
        This will also set the other number entry to be below this one
        """
        if other._number_variable is self._number_variable:
            print("WARNING! Attempt to set variable as above itself!")
            return
        self.entry_below = other
        other.entry_above = self

    

if __name__ == "__main__":
    app = ctk.CTk()
    test_widget = NumberEntry(app)
    test_widget.pack()
    app.mainloop()
        
