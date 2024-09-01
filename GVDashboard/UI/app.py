# This script contains the core code used for the Cutom Tkinker app

import customtkinter as ctk # For general application features
import tkinter.ttk as ttk

from menu import TopMenuBar


# Constants
DEFAULT_WIDTH = 800
DEFAULT_HIGHT = 300
MIN_WIDTH = 400
MIN_HIGHT = 150
PANEL_WIDTH = 200
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
class MainFrame(ttk.PanedWindow):
    def __init__(self, master):
        super().__init__(master=master, orient="horizontal")

        # Pack the views in
        self.left = LeftFrame(self)
        self.add(self.left, weight=0)

        self.view = ViewFrame(self)
        self.add(self.view, weight=1)

        self.right = RightFrame(self)
        self.add(self.right, weight=0)



        #hb = HideButton(self.view, )

class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="blue", width=PANEL_WIDTH)

class RightFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="red", width=PANEL_WIDTH)

class ViewFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class HideButton(ctk.CTkButton):
    def __init__(self, master, target:ctk.CTkFrame):
        super().__init__(master, text="Hide", command=self.hide_target)
        self.target = target

    def hide_target(self):
        self.target.pack_forget()

# Make app if run as main
if __name__ == "__main__":
    app = App()
    app.mainloop()