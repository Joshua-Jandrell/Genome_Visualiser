"""
Contains applications with various UI and plotting structures to help determine which approach is the most efficient.
These systems use manual'next plot' testing so that the responsiveness of each plot type can be qualitatively evaluated as well.
"""

from typing import Tuple

import os, time, csv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas

import customtkinter as ctk
from CTkXYFrame import CTkXYFrame

from .plotSetup import get_plot_figure
from .plotMethods import *

from config import BLOCK_SIZE, RESULT_DIR
from .makeRandomData import get_random_zygoisty

APP_X = 500
APP_Y = 500

DEFAULT_FIG = 200

DATA_DIMS = [(5,20),(500,2000)]#,(50,200),(500,200),(500,2000)]
"""Data sizes used for plotting tests."""
DPIS = [50]#, 100, 150]

SAVE_FOLDER = os.path.join(RESULT_DIR,"Plots","RenderTimes")

class InfoBar(ctk.CTkFrame):
    """
    Used to display details regarding the plot method and size used.
    """

    def __init__(self,master,command=None):
        super().__init__(master=master)

        self.label = ctk.CTkLabel(self, text="<Plot method>\t<plot size>")
        self.label.pack(side=ctk.LEFT, padx = 10)

        self.next_button = ctk.CTkButton(self, command=command, text="Next Plot", height=20)
        self.next_button.pack(side=ctk.RIGHT,padx=10, pady=4)
        
    def set_text(self,method:str, x:int, y:int, dpi:int):
        self.label.configure(text=f"{method}\t{x}x{y} dpi:{dpi}")

    def set_action(self,action_txt:str):
        self.next_button.configure(text=action_txt)

def get_csv_headings():
    return [
        "canvas_type", # How is the plot displayed: interactive canvas or image?
        "scroll_type",  # How is the figure scrolled: matplotlib, tkinter scroll view or tkinter canvas scroll?
        "plot_type",   # What plotting method was used to generate the plot 
        "n_variants",
        "n_samples",
        "n_values",
        "dpi",
        "resized",  # Set to true is the canvas needed to resized to fit the plot.
        "plot_time",
        "render_time"
    ]
class ResultsCSV():
    """Static class used to write results to an output file."""
    f = None
    writer = None

    @classmethod
    def add_row(cls, row):
        """
        Add a rows as follows [canvas_type, scroll_type, plot_type, variants, samples, values, dpi, resized, plot_time, render_time]
        """
        if cls.writer is None:
            # Make file if required 
            os.makedirs(SAVE_FOLDER, exist_ok=True)
            cls.f = open(os.path.join(SAVE_FOLDER, "render_test_results.csv"), mode="w", newline="")
            cls.writer = csv.writer(cls.f)
            cls.writer.writerow(get_csv_headings())
            
        cls.writer.writerow(row)

        
    @classmethod
    def close(cls):
        if cls.f is not None:
            cls.writer = None
            cls.f.close()
            cls.f = None


class CTkScrollAgg(ctk.CTk):
    """
    Interactive matplotlib canvas with scrolling and scaling managed by tkinter scroll view.
    """
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Interactive plot with tkinter scroll")
        self.geometry(f"{APP_X}x{APP_Y}")

        # Display bar
        self.info = InfoBar(self, command=self.next_plot)
        self.info.pack(side=ctk.TOP, fill=ctk.X)

        # Scroll frame used to hold the panel
        self.scroll_frame = CTkXYFrame(self)
        self.scroll_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        self.fig, _ = get_plot_figure()
        
        self.agg_canvas = FigCanvas(self.fig, master=self.scroll_frame)
        self.fig_widget = self.agg_canvas.get_tk_widget()
        self.fig_widget.pack()

        self.size_i = 0
        self.method_i = 0
        self.dpi_i = 0
        self.set_defaults()

        self.watch_config = False
        self.plot_t = 0
        self.start_t = 0
        self.render_t = 0
        self.resized = False
        self.method_name = ""
        self.v = 0
        self.s = 0
        self.dpi = 0

        # Bind configure event to find when final plot configuration is completed
        self.fig_widget.bind_all("<Configure>",self.on_configure_end)

    def on_configure_end(self,event):
        # In most cases the resizing of the canvas signals the end os scaling
        if self.watch_config and event.widget == self.scroll_frame:

            self.render_t = time.time() - self.start_t

            # Stop checking for canvas config to avoid recoding new times when the frame is scrolled
            self.watch_config = False

        # in some cases the scrollable frame must then adjust to accommodate the canvas resulting in longer scaling times
        if event.widget == self.scroll_frame.xy_canvas:
            self.render_t = time.time() - self.start_t
            self.resized = True

    def set_defaults(self):
        self.fig.clear()
        self.fig_widget.configure(width=300, height=300)
        self.agg_canvas.draw()
        self.resized = False
        self.clear = True
        self.info.set_action("plot next")

    def set_plotted(self):
        self.clear = False
        self.info.set_action("clear plot")

    def record_data(self):
        ResultsCSV.add_row([
            "Agg",
            "tkinter_widget",
            self.method_name,
            self.s,
            self.v,
            self.s * self.v,
            self.dpi,
            self.resized,
            self.plot_t,
            self.render_t
        ])

    def next_plot(self):
        """
        Call this function to run plotting and scrolling tests.
        """
        if not self.clear:
            self.record_data()
            self.set_defaults()
            return
        # Get next set of dimensions and plot types
        if self.size_i < len(DATA_DIMS):
            dim = DATA_DIMS[self.size_i]
            self.s = _s = dim[0]
            self.v = _v = dim[1]


            # Make data
            data = get_random_zygoisty(n_samples=_s, n_variants=_v)

            # Get next plot method, or increment dimensions
            if self.method_i < len(ZYGO_PLOT_METHODS):
                method = ZYGO_PLOT_METHODS[self.method_i]
                self.method_name = ZYGO_PLOT_METHOD_NAMES[self.method_i]
                if self.dpi_i < len(DPIS):
                    self.dpi = dpi = DPIS[self.dpi_i]
                    self.fig.set_dpi(dpi)
                    self.dpi_i += 1

                    # Update top bar 
                    self.info.set_text(self.method_name, _s, _v, dpi)

                    # Indicate the canvas is not clear
                    self.set_plotted()

                    self.plot_on_canvas(data, method)
                else:
                    self.dpi_i = 0
                    self.method_i+=1
                    self.next_plot()

            else:
                self.size_i += 1
                self.method_i = 0
                self.next_plot()

        else:
            self.destroy()
            
    def plot_on_canvas(self, data, plot_method):
        _v, _s = data.shape
        _ts = time.time()
        plot_method(data, self.fig)
        self.plot_t = time.time()-_ts

        self.start_t = time.time()
        
        self.fig_widget.configure(width=_s*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        self.agg_canvas.draw()


        # Set start time and start tracking for configure event
        self.watch_config = True


class MPLScrollAgg(ctk.CTk):
    """
    Interactive matplotlib canvas with scrolling and scaling managed by setting matplotlib limits.
    """
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Interactive plot with tkinter scroll")
        self.geometry(f"{APP_X}x{APP_Y}")

        # Display bar
        self.info = InfoBar(self, command=self.next_plot)
        self.info.pack(side=ctk.TOP, fill=ctk.X)

        # Scroll frame used to hold the panel
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        self.fig, _ = get_plot_figure()
        
        self.agg_canvas = FigCanvas(self.fig, master=self.canvas_frame)
        self.fig_widget = self.agg_canvas.get_tk_widget()
        self.fig_widget.pack()

        self.size_i = 0
        self.method_i = 0
        self.dpi_i = 0
        self.set_defaults()

        self.watch_config = False
        self.plot_t = 0
        self.start_t = 0
        self.render_t = 0
        self.resized = False
        self.method_name = ""
        self.v = 0
        self.s = 0
        self.dpi = 0

        # Bind configure event to find when final plot configuration is completed
        self.fig_widget.bind_all("<Configure>",self.on_configure_end)

    def on_configure_end(self,event):
        # In most cases the resizing of the canvas signals the end os scaling
        if self.watch_config and event.widget == self.canvas_frame:

            self.render_t = time.time() - self.start_t

            # Stop checking for canvas config to avoid recoding new times when the frame is scrolled
            self.watch_config = False

        # in some cases the scrollable frame must then adjust to accommodate the canvas resulting in longer scaling times
        if event.widget == self.fig_widget:
            self.render_t = time.time() - self.start_t
            self.resized = True

    def set_defaults(self):
        self.fig.clear()
        self.fig_widget.configure(width=300, height=300)
        self.agg_canvas.draw()
        self.resized = False
        self.clear = True
        self.info.set_action("plot next")

    def set_plotted(self):
        self.clear = False
        self.info.set_action("clear plot")

    def record_data(self):
        ResultsCSV.add_row([
            "Agg",
            "tkinter_widget",
            self.method_name,
            self.s,
            self.v,
            self.s * self.v,
            self.dpi,
            self.resized,
            self.plot_t,
            self.render_t
        ])

    def next_plot(self):
        """
        Call this function to run plotting and scrolling tests.
        """
        if not self.clear:
            self.record_data()
            self.set_defaults()
            return
        # Get next set of dimensions and plot types
        if self.size_i < len(DATA_DIMS):
            dim = DATA_DIMS[self.size_i]
            self.s = _s = dim[0]
            self.v = _v = dim[1]


            # Make data
            data = get_random_zygoisty(n_samples=_s, n_variants=_v)

            # Get next plot method, or increment dimensions
            if self.method_i < len(ZYGO_PLOT_METHODS):
                method = ZYGO_PLOT_METHODS[self.method_i]
                self.method_name = ZYGO_PLOT_METHOD_NAMES[self.method_i]
                if self.dpi_i < len(DPIS):
                    self.dpi = dpi = DPIS[self.dpi_i]
                    self.fig.set_dpi(dpi)
                    self.dpi_i += 1

                    # Update top bar 
                    self.info.set_text(self.method_name, _s, _v, dpi)

                    # Indicate the canvas is not clear
                    self.set_plotted()

                    self.plot_on_canvas(data, method)
                else:
                    self.dpi_i = 0
                    self.method_i+=1
                    self.next_plot()

            else:
                self.size_i += 1
                self.method_i = 0
                self.next_plot()

        else:
            self.destroy()
            
    def plot_on_canvas(self, data, plot_method):
        _ts = time.time()
        _v, _s = data.shape
        #self.scroll_frame.xy_canvas.configure(width=_n*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        self.fig_widget.configure(width=_s*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        plot_method(data, self.fig)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        self.agg_canvas.draw()
        self.plot_t = time.time()-_ts

        # Set start time and start tracking for configure event
        self.watch_config = True
        self.start_t = time.time()

class CanvasScrollAgg(ctk.CTk):
    """
    Interactive matplotlib canvas with scrolling and scaling managed directly on plot canvas widget.
    """
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Interactive plot with canvas scroll")
        self.geometry(f"{APP_X}x{APP_Y}")

        # Display bar
        self.info = InfoBar(self, command=self.next_plot)
        self.info.pack(side=ctk.TOP, fill=ctk.X)

        # Scroll frame used to hold the panel
        self.scroll_frame = CTkXYFrame(self)
        self.scroll_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        self.fig, _ = get_plot_figure()
        
        self.agg_canvas = FigCanvas(self.fig, master=self.scroll_frame)
        self.fig_widget = self.agg_canvas.get_tk_widget()
        self.fig_widget.pack()

        self.size_i = 0
        self.method_i = 0
        self.dpi_i = 0
        self.set_defaults()

        self.watch_config = False
        self.plot_t = 0
        self.start_t = 0
        self.render_t = 0
        self.resized = False
        self.method_name = ""
        self.v = 0
        self.s = 0
        self.dpi = 0

        # Bind configure event to find when final plot configuration is completed
        self.fig_widget.bind_all("<Configure>",self.on_configure_end)

    def on_configure_end(self,event):
        # In most cases the resizing of the canvas signals the end os scaling
        if self.watch_config and event.widget == self.scroll_frame:

            self.render_t = time.time() - self.start_t

            # Stop checking for canvas config to avoid recoding new times when the frame is scrolled
            self.watch_config = False

        # in some cases the scrollable frame must then adjust to accommodate the canvas resulting in longer scaling times
        if event.widget == self.scroll_frame.xy_canvas:
            self.render_t = time.time() - self.start_t
            self.resized = True

    def set_defaults(self):
        self.fig.clear()
        self.fig_widget.configure(width=300, height=300)
        self.agg_canvas.draw()
        self.resized = False
        self.clear = True
        self.info.set_action("plot next")

    def set_plotted(self):
        self.clear = False
        self.info.set_action("clear plot")

    def record_data(self):
        ResultsCSV.add_row([
            "Agg",
            "tkinter_canvas",
            self.method_name,
            self.s,
            self.v,
            self.s * self.v,
            self.dpi,
            self.resized,
            self.plot_t,
            self.render_t
        ])

    def next_plot(self):
        """
        Call this function to run plotting and scrolling tests.
        """
        if not self.clear:
            self.record_data()
            self.set_defaults()
            return
        # Get next set of dimensions and plot types
        if self.size_i < len(DATA_DIMS):
            dim = DATA_DIMS[self.size_i]
            self.s = _s = dim[0]
            self.v = _v = dim[1]


            # Make data
            data = get_random_zygoisty(n_samples=_s, n_variants=_v)

            # Get next plot method, or increment dimensions
            if self.method_i < len(ZYGO_PLOT_METHODS):
                method = ZYGO_PLOT_METHODS[self.method_i]
                self.method_name = ZYGO_PLOT_METHOD_NAMES[self.method_i]
                if self.dpi_i < len(DPIS):
                    self.dpi = dpi = DPIS[self.dpi_i]
                    self.fig.set_dpi(dpi)
                    self.dpi_i += 1

                    # Update top bar 
                    self.info.set_text(self.method_name, _s, _v, dpi)

                    # Indicate the canvas is not clear
                    self.set_plotted()

                    self.plot_on_canvas(data, method)
                else:
                    self.dpi_i = 0
                    self.method_i+=1
                    self.next_plot()

            else:
                self.size_i += 1
                self.method_i = 0
                self.next_plot()

        else:
            self.destroy()
            
    def plot_on_canvas(self, data, plot_method):
        _ts = time.time()
        _v, _s = data.shape
        #self.scroll_frame.xy_canvas.configure(width=_n*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        self.fig_widget.configure(width=_s*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        plot_method(data, self.fig)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        self.agg_canvas.draw()
        self.plot_t = time.time()-_ts

        # Set start time and start tracking for configure event
        self.watch_config = True
        self.start_t = time.time()

def run_all_plot_app_tests():
    ctk_agg = CTkScrollAgg()
    ctk_agg.mainloop()

    ResultsCSV.close()
