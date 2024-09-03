# This script contains the core code used for the Cutom Tkinker app

import customtkinter as ctk # For general application features
import tkinter as tk
import tkinter.ttk as ttk

from UI.menu import TopMenuBar
from UI.viewPanel import ViewPanel
from UI.sidePanel import SidePane

#from Plot.dummyPlotter import make_plot
from UI.plotInfo import *
from VCF.vcfTest import getData

for UI.Se

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
        self.view = ViewPanel(self)

        # Pack the views into window
        self.left.pack(side = ctk.LEFT, fill=ctk.Y)
        self.right.pack(side = ctk.RIGHT, fill=ctk.Y)
        self.view.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # make plot button
        self.left.plot_button = ctk.CTkButton(self.left.content,text="Plot",command=self.makePlot)
        self.left.plot_button.pack()

    def makePlot(self):
        print("bbom")
        data = getData()
        wrapped_data = VcfDataWrapper(data)
        self.plot_info = PlotInfo()
        self.view.set_plot(self.plot_info.plot_data(wrapped_data))





class MainFrame1(ttk.PanedWindow):
    def __init__(self, master):
        super().__init__(master=master, orient="horizontal")

        # Pack the views in
        self.left = LeftFrame(self)
        self.add(self.left, weight=0)

        self.view = ViewPanel(self)
        self.add(self.view, weight=1)

        self.right = RightFrame(self)
        self.add(self.right, weight=0)

        
        # make plot button
        self.left.plot_button = ctk.CTkButton(self.left,text="Plot",command=self.makePlot)
        self.left.plot_button.pack()

    def makePlot(self):
        #fig = make_plot()
        data = getData()
        wrapped_data = VcfDataWrapper(data)
        self.plotInfo = PlotInfo()
        self.view.set_plot(PlotInfo.plot_data(wrapped_data))
        
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

# Make app if run as main
if __name__ == "__main__":
    app = App()
    app.mainloop()