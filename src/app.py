# This script contains the core code used for the Cutom Tkinker app

import customtkinter as ctk # For general application features
#import tkinter as tk
#import tkinter.ttk as ttk

from matplotlib.figure import Figure as Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from UI.numberEntry import NumberEntry

from UI.menu import TopMenuBar
from UI.sidePanel import SidePanel
from viewPanel import ViewPanel

from VCF.globalDatasetManger import GlobalDatasetManager

from UI.searchPanel import SearchPanel

from Plot.ViewInfos import ViewInfo_base
from autoPlotter import AutoPlotter
from Plot.keyCanvas import KeyCanvas

import pandas as pd # For set to stop deprecation 
pd.set_option('future.no_silent_downcasting', True)

# Used to configure the app settings and paths
import _config_, os

# Constants
DEFAULT_WIDTH = 1200
DEFAULT_HIGHT = 600
MIN_WIDTH = 400
MIN_HIGHT = 150
LEFT_PANEL_WIDTH = 500
RIGHT_PANEL_WIDTH = 250
HIDE_BAR_WIDTH = 10
MIN_VIEW_WIDTH = 400

class App(ctk.CTk):
    """
    Class used to create and run the visualizer app.\n
    Inherits from `ctk.CTK` class to get functionalities of native application
    """

    instance = None
    
    def __init__(self):
        super().__init__()

        # There should only ever be one instance of the app
        assert(App.instance is None)
        App.instance = self

        self.title("Genome Visualizer")

        # Give app an icon 
        try:
            self.iconbitmap(os.path.join(_config_.IMG_PATH, 'icon.ico'))
        except:
            pass

        # set size app window
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HIGHT}")
        self.minsize(MIN_WIDTH,MIN_HIGHT)

        # Add topbar menu
        #self.menubar = TopMenuBar(master=self)
        #self.config(menu=self.menubar)

        
        # Make collapsable side-panels and put them in the app window
        self.left = SidePanel(self,ctk.RIGHT, width=LEFT_PANEL_WIDTH)
        self.left.pack(side = ctk.LEFT, fill=ctk.Y)

        self.right = SidePanel(self,ctk.LEFT, width=RIGHT_PANEL_WIDTH)
        self.right.pack(side = ctk.RIGHT, fill=ctk.Y)

        # Plack search option in left panel
        self.search_panel = SearchPanel(self.left.content)
        self.search_panel.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Put key key canvas on the right panel 
        self.key_canvas = KeyCanvas(self.right.content, width=RIGHT_PANEL_WIDTH)
        self.key_canvas.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Makes plot button -- might get depricated
        self.left.plot_button = ctk.CTkButton(self.search_panel.button_panel,text="Plot",command=self.makePlot)
        self.left.plot_button.pack(fill=ctk.BOTH)
        
        self.view = ViewPanel(self)
        self.view.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

        # Activate auto plotter. This should only be done after all UI element are created 
        AutoPlotter.set_active(True)

        # Add event to define behavior when deleted
        self.protocol("WM_DELETE_WINDOW", self._on_app_delete)

        self.after(0,self.__set_size)

    def __set_size(self):
        # set size app window
        try:
            self.state('zoomed')
        except:
            self.attributes('-zoomed', True)
        #self.resizable(False, False)

    def destroy(self):
        GlobalDatasetManager.deregister_all()
        return super().destroy()

    def _on_app_delete(self):
            # Clean up plots to ensure that app is deleted
            #ViewPanel.clear_plot()
            # self.main_frame.pack_forget()
            # self.main_frame.destroy()
            # self.main_frame = None
            ViewPanel.set_active(False)
            AutoPlotter.set_active(False)
            self.destroy()

    def makePlot(self):
        self.view.make_plot(views=self.search_panel.search_options.plots_options.get_opt_values())

    def plot_views(views:list[ViewInfo_base]):
        """Static method used to plot the given list of views on the main canvas."""
        assert(isinstance(App.instance,App))
        App.instance.view.make_plot(views=views)

# Makes app if run as main
if __name__ == "__main__":
    ctk.set_default_color_theme("green")
    ctk.set_appearance_mode("light")
    app = App()
    app.mainloop()

