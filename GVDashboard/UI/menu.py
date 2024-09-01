# This script contains classes used to implement the application menu bar

import tkinter as tk    # Use standard tkinker because custom tkinker does not implement manubar
import customtkinter as ctk
import tkinter.ttk as ttk

# This class is used to make the top menu bar for the visualizer app
# TODO: There is no custom tkinker widget for this so we will need to format it properly some time.
# NOTE: There is not way to style the menubar on windows: may need to make out own later
class TopMenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master=master)

        # Add file menu option
        self.file_menu = FileMenu(self)
        self.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )

        # Format 
        self.config(bg = "GREEN")

    # # Update the format of the menubar based on ctk theme
    # def updateFormat(self):
    #     self.

# this class manages the `File` sub-menu
class FileMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master=master, tearoff=0)

        # add menu items to the File menu
        self.add_command(label='New')
        self.add_command(label='Open...')
        self.add_command(label='Close')
        self.add_separator()