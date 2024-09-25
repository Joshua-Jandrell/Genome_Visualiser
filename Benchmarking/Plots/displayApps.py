"""
Contains applications with various UI and plotting structures to help determine which approach is the most efficient.
These systems use manual'next plot' testing so that the responsiveness of each plot type can be qualitatively evaluated as well.
"""

from typing import Tuple

import os, time, csv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from PIL import Image

import customtkinter as ctk
import tkinter as tk
from CTkXYFrame import CTkXYFrame

from .plotSetup import get_plot_figure
from .plotMethods import *

from config import BLOCK_SIZE, RESULT_DIR
from .makeRandomData import get_random_zygoisty
from .plotSetup import scale_figure

APP_X = 500
APP_Y = 500

DEFAULT_FIG = 200

DATA_DIMS = [(500,200)] #,(500,2000)]
"""Data sizes used for plotting tests."""
DPIS = [100]#, 100, 150]

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
        self.method_i = 1
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
        scale_figure(self.fig,_s*BLOCK_SIZE,_v*BLOCK_SIZE)
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
        self.title("Interactive plot with matplotlib scroll")
        self.geometry(f"{APP_X}x{APP_Y}")

        # Display bar
        self.info = InfoBar(self, command=self.next_plot)
        self.info.pack(side=ctk.TOP, fill=ctk.X)

        # Scroll bar for x values
        self.x_slider = ctk.CTkSlider(self, command=self.scroll_fig_x)
        #self.x_slider = ctk.CTkScrollbar(self, command=self.scroll_fig_x, orientation='horizontal')
        self.x_slider.pack(side=ctk.BOTTOM, fill=ctk.X)

        # Scroll bar for y slider
        self.y_slider = ctk.CTkSlider(self, command=self.scroll_fig_y, orientation='vertical')
        self.y_slider.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Scroll frame used to hold the panel
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        self.fig, _ = get_plot_figure()
        
        self.agg_canvas = FigCanvas(self.fig, master=self.canvas_frame)
        self.fig_widget = self.agg_canvas.get_tk_widget()
        self.fig_widget.pack()

        self.size_i = 0
        self.method_i = 1
        self.dpi_i = 0
        self.set_defaults()

        self.watch_config = False
        self.plot_t = 0
        self.start_t = 0
        self.render_t = 0
        self.resized = True
        self.method_name = ""
        self.v = 0
        self.s = 0
        self.dpi = 0

        self.x_window = 0
        self.y_window = 0

    def set_defaults(self):
        self.fig.clear()
        self.fig_widget.configure(width=300, height=300)
        self.agg_canvas.draw()
        self.resized = False
        self.clear = True
        self.info.set_action("plot next")

        # Configure e scroll bars
        self.x_slider.configure(state="disabled", button_length=self.x_slider.winfo_width())
        self.x_slider.set(0)
        self.y_slider.configure(state="disabled", button_length=self.y_slider.winfo_height())
        self.y_slider.set(0)

    def set_plotted(self):
        self.clear = False
        self.info.set_action("clear plot")

    def record_data(self):
        ResultsCSV.add_row([
            "Agg",
            "matplotlib_plot",
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

        #self.fig.axes[0].set_xticks(range(_s))

        # Check to see if scroll is required 
        if BLOCK_SIZE * _s > self.canvas_frame.winfo_width():
            self.fig_widget.configure(width=self.canvas_frame.winfo_width())
            # Find ideal x window size (NOTE use canvas frame size here, not figure widget which tends to be unreliable)
            self.x_window = self.canvas_frame.winfo_width()/BLOCK_SIZE
            # Configure y scroll bar 
            self.x_slider.configure(from_=0, to=_s-self.x_window, state="normal", button_length=(self.x_window/_s)*self.x_slider.winfo_width())
            #self.x_slider.configure(width=self.x_window)
            self.x_slider.set(0, _s-self.x_window)

            # do initial scroll
            self.scroll_fig_x(0)
        else:
            self.fig_widget.configure(width=BLOCK_SIZE*_s)

        if BLOCK_SIZE * _v > self.canvas_frame.winfo_height():
            self.fig_widget.configure(height=self.canvas_frame.winfo_height())
            # Find ideal y window size (NOTE use canvas frame size here, not figure widget which tends to be unreliable)
            self.y_window = self.canvas_frame.winfo_height()/BLOCK_SIZE
            # Configure y scroll bar 
            self.y_slider.configure(from_=0, to=_v-self.y_window, state="normal", button_length=(self.y_window/_v)*self.y_slider.winfo_height())
            # do initial scroll
            self.scroll_fig_y(_v-self.y_window)
            self.y_slider.set(_v-self.y_window)
        else:
            self.fig_widget.configure(height=BLOCK_SIZE*_v)

        # Set start time and start tracking for configure event
        self.watch_config = True
        self.start_t = time.time()


        self.fig_widget.configure(width=_s*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        self.agg_canvas.draw()

    def scroll_fig_x(self,value):
        if self.method_name in ["matshow", "imshow"]:
            value -= 0.5
        self.fig.axes[0].set_xlim([value, value+self.x_window])
        self.agg_canvas.draw_idle()

    def scroll_fig_y(self, value):
        if self.method_name in ["matshow", "imshow"]:
            value -= 0.5
        self.fig.axes[0].set_ylim([value, value+self.y_window])
        self.agg_canvas.draw_idle()

class CTkScrollImg(ctk.CTk):
    """
    Static images with scrolling and scaling managed by tkinter scroll view.
    """
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Pillow image plot with tkinter scroll")
        self.geometry(f"{APP_X}x{APP_Y}")

        # Display bar
        self.info = InfoBar(self, command=self.next_plot)
        self.info.pack(side=ctk.TOP, fill=ctk.X)

        # Scroll frame used to hold the panel
        self.scroll_frame = CTkXYFrame(self)
        self.scroll_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        self.fig, _ = get_plot_figure()
        
        self.agg_canvas = FigCanvas(self.fig, master=self.scroll_frame)
        self.img_label = ctk.CTkLabel(master=self.scroll_frame, text="")
        #self.img_label = ctk.CTkLabel(master=self, text="")

        self.size_i = 0
        self.method_i = 1
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
        #self.fig_widget.bind_all("<Configure>",self.on_configure_end)

    # def on_configure_end(self,event):
    #     # In most cases the resizing of the canvas signals the end os scaling
    #     if self.watch_config and event.widget == self.scroll_frame:

    #         self.render_t = time.time() - self.start_t

    #         # Stop checking for canvas config to avoid recoding new times when the frame is scrolled
    #         self.watch_config = False

    #     # in some cases the scrollable frame must then adjust to accommodate the canvas resulting in longer scaling times
    #     if event.widget == self.scroll_frame.xy_canvas:
    #         self.render_t = time.time() - self.start_t
    #         self.resized = True

    def set_defaults(self):
        self.fig.clear()
        self.img_label.pack_forget()
        self.agg_canvas.draw()
        self.resized = False
        self.clear = True
        self.info.set_action("plot next")

    def set_plotted(self):
        self.clear = False
        self.info.set_action("clear plot")

    def record_data(self):
        ResultsCSV.add_row([
            "Figure",
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

        scale_figure(self.fig,_s*BLOCK_SIZE,_v*BLOCK_SIZE)

        _ts = time.time()
        plot_method(data, self.fig)
        self.plot_t = time.time()-_ts

        self.img_label.pack()
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        self.agg_canvas.draw()

        self.fig.savefig(os.path.realpath("plot.png"))


        #img = Image.frombytes('RGB', self.fig.canvas.get_width_height(), self.fig.canvas.tostring_rgb())
        img = Image.open(os.path.realpath("plot.png"))
        ctk_img = ctk.CTkImage(img, size=(_s*BLOCK_SIZE,_v*BLOCK_SIZE))

        self.start_t = time.time()

        self.img_label.configure(width=_s*BLOCK_SIZE, height=_v*BLOCK_SIZE, image=ctk_img)


        # Set start time and start tracking for configure event
        self.watch_config = True

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
        self.method_i = 1
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

    mpl_scroll_agg = MPLScrollAgg()
    mpl_scroll_agg.mainloop()

    ctk_fig = CTkScrollImg()
    ctk_fig.mainloop()

    ResultsCSV.close()
