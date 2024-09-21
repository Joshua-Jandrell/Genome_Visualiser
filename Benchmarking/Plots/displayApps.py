"""
Contains applications with various UI and plotting structures to help determine which approach is the most efficient.
"""

from typing import Tuple
import customtkinter as ctk
from CTkXYFrame import CTkXYFrame

from .plotSetup import get_plot_figure
from .plotMethods import *

from config import BLOCK_SIZE
from .makeRandomData import get_random_zygoisty

APP_X = 500
APP_Y = 500

DATA_DIMS = [(5,20),(50,20)]#,(50,200),(500,200),(500,2000)]
"""Data sizes used for plotting tests."""


class InfoBar(ctk.CTkFrame):
    """
    Used to display details regarding the plot method and size used.
    """

    def __init__(self,master):
        super().__init__(master=master)

        self.method_label = ctk.CTkLabel(self, text="<Plot method>")
        self.method_label.pack(side=ctk.LEFT, padx = 10)

        self.size_label = ctk.CTkLabel(self, text="XXXxXXX")
        self.size_label.pack(side=ctk.LEFT, padx = 10)\
        
    def set_text(self,method:str, x:int, y:int):
        self.method_label.configure(text=method)
        self.size_label.configure(text=f"{x}x{y}")

class CTkScrollAgg(ctk.CTk):
    """
    Interactive matplotlib canvas with scrolling and scaling managed by tkinter scroll view.
    """
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Interactive plot with tkinter scroll")
        self.geometry(f"{APP_X}x{APP_Y}")

        # Scroll frame used to hold the panel
        self.scroll_frame = CTkXYFrame(self)
        self.scroll_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        self.fig, _ = get_plot_figure()

        # Wait for app to finish loading then run first test

    def run_tests(self):
        """
        Call this function to run plotting and scrolling tests.
        """
        # Loop through all data dimensions
        for dim in DATA_DIMS:
            _s = dim[0]
            _v = dim[1]
            data = get_random_zygoisty(n_samples=_s, n_variants=_v)
            
            # update display bar to represent data data size and method


    
    def plot_on_canvas(self, data, plot_method):
        _v, _n = data.shape
        #self.fig.set_size_inches(10,20)
        # Set image size
        self.fig_frame.xy_canvas.configure(width=_n*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        self.fig_widget.configure(width=_n*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        plot_method(data, self.fig)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        self.agg.draw()
        self.fig_widget.pack(fill=ctk.BOTH, expand=True)
        self.fig_frame.xy_canvas.yview()

def run_all_plot_app_tests():
    ctk_agg = CTkScrollAgg()
    ctk_agg.mainloop()
