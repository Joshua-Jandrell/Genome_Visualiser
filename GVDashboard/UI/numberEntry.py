from tkinter.constants import NORMAL
from typing import Any, Tuple
import customtkinter as ctk

class NumberEntry(ctk.CTkEntry):
    """Special ctk variable that can only hold a numerical value."""
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, text_color: str | Tuple[str, str] | None = None, placeholder_text_color: str | Tuple[str, str] | None = None, intvariable: ctk.IntVar | None = None, placeholder_text: str | None = None, font: tuple | ctk.CTkFont | None = None, state: str = NORMAL, **kwargs):
        
        if isinstance(intvariable, ctk.IntVar):
            self.intVar = intvariable
        else:
            self.intVar = ctk.IntVar(value=0)
        
        # Create text variable to manage the input box 
        textvariable = ctk.StringVar()
        
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, text_color, placeholder_text_color, textvariable, placeholder_text, font, state, **kwargs)

        self.__edit_lock = False
        """Set to true then this widget is editing its own input."""
        # Add trace to command to see when 
        textvariable.trace_add(mode="write", callback=self.__read_input)

    # def get()->int:
    def __read_input(self, *args):
        _value = self._textvariable.get()
        # construct string of only numerical input characters 
        _numerical_str =  "".join([c for c in _value if c.isdigit()])
        if _value != _numerical_str:
            self._textvariable.set(value=_numerical_str)

if __name__ == "__main__":
    app = ctk.CTk()
    test_widget = NumberEntry(app)
    test_widget.pack()
    app.mainloop()
        
