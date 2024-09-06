# This script contains a simple tkinter tooltip widget class
# Code was adapted from squareRoot17's answer found here: https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python

#from tkinter import *
import tkinter as tk
from typing import Tuple
import customtkinter as ctk

# Class used to create tooltip frame widgets
class TooltipWindow(ctk.CTkToplevel):
    def __init__(self, *args, text:str, x, y,fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.wm_overrideredirect(1)
        self.wm_geometry("+%d+%d" % (x, y))
        label = ctk.CTkLabel(self, text=text, justify=ctk.LEFT)
        label.pack(ipadx=1)
   
class ToolTip(object):

    def __init__(self, widget:tk.Widget, text:str|None = "Tooltip"):
        self.widget = widget
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.text = text

        widget.bind('<Enter>', self.showtip)
        widget.bind('<Leave>', self.hidetip)

    def showtip(self,event):
        "Display text in tooltip window"

        if isinstance(self.tip_window, TooltipWindow) or self.text is None: return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()
        y = y + cy + self.widget.winfo_rooty()
        self.tip_window = TooltipWindow(self.widget,text=self.text,x=x,y=y)
 

    def hidetip(self,event):
        if isinstance(self.tip_window,TooltipWindow):
            self.tip_window.destroy()
            self.tip_window = None

