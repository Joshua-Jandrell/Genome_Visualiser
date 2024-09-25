
from typing import Tuple
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from UI.deafultSettings import Dimenations

from matplotlib.figure import Figure 

from Plot.plotInfo import ViewPlotter, ViewInfo_base
from VCF.dataSetConfig import DataSetConfig

class KeyCanvas(ctk.CTkFrame):
    """Class used to plot keys to figures on a separate collapsable view."""

    instance = None
    def get_figure()->Figure|None:
        if isinstance(KeyCanvas.instance, KeyCanvas): return KeyCanvas.instance.fig
        else: return None

    def update_canvas():
        if isinstance(KeyCanvas.instance, KeyCanvas): KeyCanvas.instance.update()

    def show_canvas():
        if isinstance(KeyCanvas.instance, KeyCanvas): KeyCanvas.instance.show()

    def hide_canvas():
        if isinstance(KeyCanvas.instance, KeyCanvas): KeyCanvas.instance.hide()

    def __init__(self, master, width: int = Dimenations.PANEL_WIDTH, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # There can be only one
        assert KeyCanvas.instance is None
        KeyCanvas.instance = self

        self.fig = Figure(dpi=100)
        self.canvas = FigCanvas(self.fig, master=self)
        self.widget = self.canvas.get_tk_widget()
        self.widget.configure(width=Dimenations.PANEL_WIDTH)



    def update(self):
        self.fig.draw()

    def show(self):
        self.widget.pack(side="top", expand=True, fill="both")
        self.canvas.draw()

    def hide(self):
        self.widget.pack_forget()
    