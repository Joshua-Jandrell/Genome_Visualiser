# This script contains the code for the main visualiser view panel

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from matplotlib.figure import Figure 

from Plot.plotInfo import ViewPlotter, ViewInfo_base
from VCF.dataSetConfig import DataSetConfig


class ViewPanel(ctk.CTkFrame):
    instance = None

    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")

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

        self.toolbar.pack(side="top")
        self.plot.pack(side="top", fill="both", expand=True)
        self.hidden = False

    def set_plot(self, views:list[ViewInfo_base])->FigCanvas:

        if len(views) > 0 and self.hidden:
            self.__show_plots()
        elif len(views) == 0 and not self.hidden:
            self.__hide_plots()
            return


        # Destroy old plot and toolbar if any
        # if self.plot is not None:
        #     self.plot.destroy()
        # if self.toolbar is not None:
        #     self.toolbar.destroy()

        # Scale figure based on window size
        self.view_plotter.plot_figure(views)
        self.canvas.draw()
        self.toolbar.update()
    

        #self.canvas.mpl_connect('motion_notify_event',self.on_mouse_move)
        return self.canvas

    # def on_mouse_move(self, event):
    #     print(event)
