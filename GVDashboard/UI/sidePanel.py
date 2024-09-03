# This script contains tge code for a collapsable side panel
import customtkinter as ctk # For general application features
import tkinter as tk
import tkinter.ttk as ttk
from UI.deafultSettings import Dimenations as Dims

class SidePane(ctk.CTkFrame):
    def __init__(self, master, pack_side):
        super().__init__(master=master, width=Dims.PANEL_WIDTH)
        self.content = ctk.CTkFrame(self, width=Dims.PANEL_WIDTH-Dims.HIDE_BAR_WIDTH)
        self.hide_button = HideButton(self,self.content,pack_side, pack_fill=ctk.Y)

        # Pack elements
        self.hide_button.pack(side=pack_side, fill=ctk.Y)
        self.content.pack(side=pack_side, fill=ctk.Y)
# Creates a button that can hide/remove a panel when pressed
class HideButton(ctk.CTkButton):
    def __init__(self, master, target:ctk.CTkFrame, pack_side, pack_fill, visible=True):
        super().__init__(master, text="", command=self.toggle_target, width=Dims.HIDE_BAR_WIDTH)
        self.target = target
        self.visible = visible
        self.pack_side = pack_side
        self.pack_fill = pack_fill

    # Hides / removes target based on visibility
    def toggle_target(self):
        if self.visible:
            self.hide_target()
        else:
            self.show_target()
        

    def hide_target(self):
        self.target.pack_forget()
        self.visible = False
    
    def show_target(self):
        self.target.pack(side=self.pack_side, fill=self.pack_fill)
        self.visible = True
