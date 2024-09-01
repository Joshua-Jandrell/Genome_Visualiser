# This script contains the core code used for the Cutom Tkinker app

import customtkinter as ctk # For general application features
import tkinter as tk
import tkinter.ttk as ttk

from menu import TopMenuBar


# Constants
DEFAULT_WIDTH = 800
DEFAULT_HIGHT = 300
MIN_WIDTH = 400
MIN_HIGHT = 150
PANEL_WIDTH = 200
HIDE_BAR_WIDTH = 10
MIN_VIEW_WIDTH = 400

# Class used to create and run the visualizer app
# Inherits from ctk.CTK class to get functionalities of native application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gnome Visualizer")

        # set geometry of app
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HIGHT}")
        self.minsize(MIN_WIDTH,MIN_HIGHT)

        # Add topbar meanu
        self.menubar = TopMenuBar(master=self)
        self.config(menu=self.menubar)

        # add main app window
        self.main_frame = MainFrame(self)
        self.main_frame.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

# Class used to hold the main frame of the application
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        # Make views
        self.left = SidePane(self,ctk.RIGHT)
        self.right = RightFrame(self)
        self.main = ViewFrame(self)

        # Pack the views into window
        self.left.pack(side = ctk.LEFT, fill=ctk.Y)
        self.right.pack(side = ctk.RIGHT, fill=ctk.Y)
        self.main.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)





# class MainFrame(ttk.PanedWindow):
#     def __init__(self, master):
#         super().__init__(master=master, orient="horizontal")

#         # Pack the views in
#         self.left = LeftFrame(self)
#         self.add(self.left, weight=0)

#         self.view = ViewFrame(self)
#         self.add(self.view, weight=1)

#         self.right = RightFrame(self)
#         self.add(self.right, weight=0)

#         #hb = HideButton(self.view, )

class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=PANEL_WIDTH)

        #self.content = ctk.CTkFrame(self, fg_color="blue", width=PANEL_WIDTH)
        #self.hideButton = HideButton(self,self.content,)

class RightFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="red", width=PANEL_WIDTH)

class ViewFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="green")


# Contains a special hideable panel
class SidePane(ctk.CTkFrame):
    def __init__(self, master, pack_side):
        super().__init__(master=master, width=PANEL_WIDTH)
        self.content = ctk.CTkFrame(self, width=PANEL_WIDTH-HIDE_BAR_WIDTH)
        self.hide_button = HideButton(self,self.content,pack_side, pack_fill=ctk.Y)

        # Pack elements
        self.hide_button.pack(side=pack_side, fill=ctk.Y)
        self.content.pack(side=pack_side, fill=ctk.Y)
# Creates a button that can hide/remove a panel when pressed
class HideButton(ctk.CTkButton):
    def __init__(self, master, target:ctk.CTkFrame, pack_side, pack_fill, visible=True):
        super().__init__(master, text=">", command=self.toggle_target, width=HIDE_BAR_WIDTH)
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


# Make app if run as main
if __name__ == "__main__":
    app = App()
    app.mainloop()