# This script contains the code for the main visualiser view panel

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from matplotlib.figure import Figure 

from Plot.plotInfo import ViewPlotter, ViewInfo_base


class ViewPanel(ctk.CTkFrame):
    instance = None

    def __init__(self, master):
        super().__init__(master=master, fg_color="pink")

        self.plot = None
        self.toolbar = None

        self.fig = Figure(figsize = (5, 5), dpi = 100)
        self.canvas =  FigCanvas(self.fig, master=self)
        
        # Create a view plotter for the canvas
        self.view_plotter = ViewPlotter(self.fig)

        self.toolbar = NavToolbar(window=self,canvas=self.canvas)
        self.toolbar.update()
        self.toolbar.pack(side="top")
        
        self.plot = self.canvas.get_tk_widget()
        self.plot.pack(side="top", fill="both", expand=True)

        

    def set_plot(self, views:list[ViewInfo_base])->FigCanvas:

        # Destroy old plot and toolbar if any
        # if self.plot is not None:
        #     self.plot.destroy()
        # if self.toolbar is not None:
        #     self.toolbar.destroy()

        # Scale figure based on window size
        self.view_plotter.plot_figure(views)
        self.canvas.draw()
    

        #self.canvas.mpl_connect('motion_notify_event',self.on_mouse_move)
        return self.canvas

    # def on_mouse_move(self, event):
    #     print(event)
