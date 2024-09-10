# This script contains the code for the main visualiser view panel

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from matplotlib.figure import Figure 

from Plot.plotInfo import ViewPlotter, ViewInfo_base
from VCF.dataSetConfig import DataSetConfig


class ViewPanel(ctk.CTkFrame):
    __instance = None

    def set_plots(views:list[ViewInfo_base]):
        if isinstance(ViewPanel.__instance, ViewPanel):
            ViewPanel.__instance.make_plot(views=views)

    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")
        
        # There can only be one instance 
        assert(not isinstance(ViewPanel.__instance, ViewPanel))

        self.plot = None
        self.toolbar = None

        self.fig = Figure(figsize = (5, 5), dpi = 100)
        self.canvas =  FigCanvas(self.fig, master=self)
        
        # Create a view plotter for the canvas
        self.view_plotter = ViewPlotter(self.fig)
        self.toolbar = NavToolbar(window=self,canvas=self.canvas)
        self.plot = self.canvas.get_tk_widget()


        # Create button to let users quickly select datasets
        self.data_select_button = ctk.CTkButton(self, text="Select Dataset File",
                                                command=lambda: DataSetConfig.open()
        )

        self.__hide_plots()
        ViewPanel.__instance = self

    def __hide_plots(self):
        """Hides the plot canvas. Should be called when no figures are plotted."""
        # hide canvas and toolbar
        self.plot.pack_forget()
        self.toolbar.pack_forget()
        self.hidden = True

        # show dataset selection button 
        self.data_select_button.place(relx=.5, rely=.5, anchor="center")
         

    def __show_plots(self):
        self.data_select_button.place_forget()

        self.toolbar.pack(side="top",fill="x")
        self.toolbar.update()
        self.plot.pack(side="top", fill="both", expand=True)
        self.hidden = False

    def make_plot(self, views:list[ViewInfo_base])->FigCanvas:

        # Scale figure based on window size
        plot_good = self.view_plotter.plot_figure(views)

        if plot_good and self.hidden:
            self.__show_plots()
            self.canvas.draw()
            self.toolbar.update()
        elif not plot_good and not self.hidden:
            self.__hide_plots()
            return
    

        #self.canvas.mpl_connect('motion_notify_event',self.on_mouse_move)
        return self.canvas

