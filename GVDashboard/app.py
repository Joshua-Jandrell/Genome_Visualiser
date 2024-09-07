# This script contains the core code used for the Cutom Tkinker app

import customtkinter as ctk # For general application features
import tkinter as tk
import tkinter.ttk as ttk

from UI.menu import TopMenuBar
from UI.viewPanel import ViewPanel
from UI.sidePanel import SidePanel

#from Plot.dummyPlotter import make_plot
from VCF.dataWrapper import VcfDataWrapper
from VCF.vcfTest import getData

from UI.searchPanel import SearchPanel

from Plot.plotInfo import ViewPlotter, ZygoteView
# Constants
DEFAULT_WIDTH = 800
DEFAULT_HIGHT = 300
MIN_WIDTH = 400
MIN_HIGHT = 150
PANEL_WIDTH = 200
HIDE_BAR_WIDTH = 10
MIN_VIEW_WIDTH = 400

# 
class App(ctk.CTk):
    """
    Class used to create and run the visualizer app.\n
    Inherits from `ctk.CTK` class to get functionalities of native application
    """
    
    def __init__(self):
        super().__init__()

        self.title("Genome Visualizer")

        # set size app window
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HIGHT}")
        self.minsize(MIN_WIDTH,MIN_HIGHT)

        # Add topbar meanu
        self.menubar = TopMenuBar(master=self)
        self.config(menu=self.menubar)

        # add main app window
        self.main_frame = MainFrame(self)
        self.main_frame.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

    def __del__(self):
        print("killed the app")

# Class used to hold the main frame of the application
class MainFrame(ctk.CTkFrame):
    """Class used to hold the view-panels in the mainframe of the app.
    """
    def __init__(self, master):
        self.data = getData()
        super().__init__(master=master)

        # Make view-panels and put them in the app window
        self.left = SidePanel(self,ctk.RIGHT)
        self.left.pack(side = ctk.LEFT, fill=ctk.Y)

        self.right = SidePanel(self,ctk.LEFT)
        self.right.pack(side = ctk.RIGHT, fill=ctk.Y)

        self.view = ViewPanel(self)
        self.view.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Makes the left panel
        self.search_panel = SearchPanel(self.left.content)
        self.search_panel.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Makes plot button -- might get depricated
        self.left.plot_button = ctk.CTkButton(self.search_panel.button_panel,text="Plot",command=self.makePlot)
        self.left.plot_button.pack(fill=ctk.BOTH)

        # Configure canvas and plot info 
        self.view_plotter = ViewPlotter()


## might get depricated --- into Data plotter
    def makePlot(self):
        assert(self.data is not None)
        wrapped_data = VcfDataWrapper(self.data)
        view_opts = self.search_panel.search_options.plots_options.get_opt_values()
        self.view_plotter.configure(wrapped_data=wrapped_data,views=view_opts)
        self.view.set_plot(self.view_plotter.plot_figure())
        # show_alt = self.search_panel.search_options.displayData.show_alt.get()
        # show_ref = self.search_panel.search_options.displayData.show_ref.get()
        # show_labels = self.search_panel.search_options.displayData.show_labels.get()
        # self.plot_info.configure(show_ref, show_alt, show_labels)
        # self.view.set_plot(self.plot_info.plot_data(wrapped_data))

# Makes app if run as main
if __name__ == "__main__":
    app = App()
    app.mainloop()