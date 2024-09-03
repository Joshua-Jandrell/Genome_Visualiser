# This script contains the code for the main visualiser view panel

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from matplotlib.figure import Figure 


class ViewPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="pink")

        self.plot = None
        self.toolbar = None

    def set_plot(self, fig : Figure)->FigCanvas:

        # Destroy old plot and toolbar if any
        if self.plot is not None:
            self.plot.destroy()
        if self.toolbar is not None:
            self.toolbar.destroy()

        # Scale figure based on window size
        self.canvas =  FigCanvas(fig, master=self)
        self.plot = self.canvas.get_tk_widget()
        self.canvas.draw()
        
        self.toolbar = NavToolbar(window=self,canvas=self.canvas)
        self.toolbar.update()

        self.toolbar.pack(side="top")
        self.plot.pack(side="top", fill="both", expand=True)

        #self.canvas.mpl_connect('motion_notify_event',self.on_mouse_move)
        return self.canvas

    # def on_mouse_move(self, event):
    #     print(event)
