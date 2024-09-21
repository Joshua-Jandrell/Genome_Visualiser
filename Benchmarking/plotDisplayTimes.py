"""
This script runs a simple app to see what method is the quickest for matplotlib plot display in tkinter.\n
Tests will be run with multiple plots using wither the mpl canvas or static images.
"""

# NOTE: A nice discussion of conversion speed can be found here: https://stackoverflow.com/questions/57316491/how-to-convert-matplotlib-figure-to-pil-image-object-without-saving-image#:~:text=fig.canvas.tostring_rgb()%20is%20deprecated.%20Use

# Note about images is ctk: (https://customtkinter.tomschimansky.com/documentation/utility-classes/image/#:~:text=The%20CTkImage%20is%20not%20a%20widget%20itself,%20but%20a%20container)
# The CTkImage is not a widget itself, but a container for up to two PIL Image objects for light and dark mode.
# There's also a size tuple which describes the width and height of the image independent of scaling.
# Therefore it's important that the PIL Image's are in a higher resolution than the given size tuple,
# so that the image is not blurry if rendered on a 4K monitor with 2x scaling.
# So that the image is displayed in sharp resolution on a 2x scaled monitor,
# the given OIL Image's must have at least double the resolution than the requested size.

from typing import Tuple
import os
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar
from matplotlib.figure import Figure

from PIL import Image

from Plots.plotMethods import *
from Plots import get_plot_figure, get_random_zygoisty
from config import *
from trackTimeMem import monitor_time

from CTkXYFrame import CTkXYFrame


APP_X = 500
APP_Y = 500

KEY_W = 598
KEY_H = 598

class App(ctk.CTk):
    def __init__(self, dpi:int, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry(f"{APP_X}x{APP_Y}")

        # Canvas and figure object used to display interactive mpl plots
        self.fig, _ = get_plot_figure(APP_X, APP_Y, dpi=dpi)
        self.fig.clear()
        self.fig_frame = CTkXYFrame(self)
        self.fig_frame.pack(expand=True, fill=ctk.BOTH)
        self.agg = FigCanvas(self.fig, master=self.fig_frame)
        self.fig_widget = self.agg.get_tk_widget()
        self.fig_widget.place(x=0,y=0)
        self.fig_widget.pack()

        # Wait for app window to open before testing plots
        self.after(100, lambda:self.test_plot_times())

       # self.plot_on_canvas(data, ZYGO_PLOT_METHODS[1])

        # Open a pillow image 
        # pil_img = Image.open(os.path.realpath("./Results/Plots/ZygsityPlottingVerification/pcolormesh.png"))
        # img = ctk.CTkImage(pil_img, size=(pil_img.size[0], pil_img.size[1]))

        # img_frame = ctk.CTkLabel(master=self, image=img, text="", width=400)
        # img_frame.pack(fill=ctk.X, expand=True)

        # Messing around with how to bind final configure scale event
        #self.fig_frame.xy_canvas.bind_all("<Configure>",self.ooo)
        self.config_watch = False
        self.iter = 4
        """Will watch for next config event if set to true."""

        self.fig_widget.bind_all("<Configure>",self.ooo)

    def ooo(self,event):
        if self.config_watch:
            #if event.width <= KEY_W and event.height <= KEY_H and event.widget == self.fig_frame.xy_canvas:
            if self.fig_frame.xy_canvas:
                print(event)
                print(event.widget)
                print(event.x)
                self.config_watch = False
                self.next_event()

    def next_event(self):
        self.iter -= 1
        if self.iter > 0:
            print(f"========= {self.iter} ==============")
            self.test_plot_times()
        else:
            print("done")
        #self.config_watch = True


    def test_plot_times(self):
        # loop through variant counts and sample counts
        for _v in VAR_COUNTS[:1]:
            for _s in SAMPLE_COUNTS[:1]:
                # get data
                data = get_random_zygoisty(n_variants=2000, n_samples=100)
                
                # Loop though all plot types
                for i, method in enumerate(ZYGO_PLOT_METHODS[1:2]):
                    # Make plot
                    print("Hmm")
                    _times = monitor_time(fxn=lambda:self.plot_on_canvas(data, method),n_runs=2)
                    print(_times)
                    

    def plot_on_canvas(self, data, plot_method):
        _v, _n = data.shape
        #self.fig.set_size_inches(10,20)
        # Set image size
        self.fig_widget.pack_forget()
        self.fig_frame.xy_canvas.configure(width=_n*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        self.fig_widget.configure(width=_n*BLOCK_SIZE, height=_v*BLOCK_SIZE)
        plot_method(data, self.fig)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
        self.agg.draw()
        self.fig_widget.pack()
        self.config_watch = True





def run_render_tests():

    # loop though all possible dpi's
    for _dpi in DPI_VALS:
        # make an app with the specified figure dpi. (This will ensure that the app canvas is made correctly).
        # Making a new canvas in an old app is not a fair test because tkinter will hold references to old canvas increasing geometry use.
        app = App(dpi=_dpi)
        app.mainloop()
        break
    # for _ in range(30):
    #     app.after(50000, lambda: app.plot_on_canvas(plot_method=ZYGO_PLOT_METHODS[1]))
    #     app.mainloop()

if __name__ == "__main__":
    run_render_tests()