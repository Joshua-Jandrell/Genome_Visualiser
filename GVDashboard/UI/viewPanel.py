# This script contains the code for the main visualiser view panel

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from matplotlib.figure import Figure 
from matplotlib.gridspec import GridSpec as GridSpec

from Plot.plotInfo import ViewPlotter, ViewInfo_base
from VCF.dataSetConfig import DataSetConfig
from Plot.keyCanvas import KeyCanvas

class ViewPanel(ctk.CTkFrame):
    __instance = None
    __active = True

    def set_active(active:bool):
        ViewPanel.__active = active

    def set_plots(views:list[ViewInfo_base]):
        if ViewPanel.__active and isinstance(ViewPanel.__instance, ViewPanel):
            ViewPanel.__instance.make_plot(views=views)

    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")
        
        # There can only be one instance 
        assert(not isinstance(ViewPanel.__instance, ViewPanel))

        self.plot = None
        self.toolbar = None

        self.fig = Figure(figsize = (5, 5), dpi = 100)
        self.canvas_frame = ctk.CTkScrollableFrame(self)
        self.canvas =  FigCanvas(self.fig, master=self.canvas_frame)
        
        # Create a view plotter for the canvas
        self.view_plotter = ViewPlotter(self.fig)
        self.toolbar = NavToolbar(window=self,canvas=self.canvas)
        self.plot = self.canvas.get_tk_widget()

        test = ctk.CTkSlider(self.plot,orientation="horizontal", height=20)
        test.place(relx=0.5, y=2,relwidth=1,anchor="n")  

        self.test_scroll = test    


        # Create button to let users quickly select datasets
        self.data_select_button = ctk.CTkButton(self, text="Select Dataset File",
                                                command=lambda: DataSetConfig.open()
        )

        self.__hide_plots()
        ViewPanel.__instance = self

    def __hide_plots(self):
        """Hides the plot canvas. Should be called when no figures are plotted."""
        # hide canvas and toolbar
        self.canvas_frame.pack_forget()
        self.toolbar.pack_forget()
        self.hidden = True

        # show dataset selection button 
        self.data_select_button.place(relx=.5, rely=.5, anchor="center")
         

    def __show_plots(self):
        self.data_select_button.place_forget()

        self.toolbar.pack(side="top",fill="x")
        self.toolbar.update()
        self.canvas_frame.pack(side="top", fill="both", expand=True)
        self.plot.pack(side="top", fill='x', expand='true')
        self.hidden = False

    def make_plot(self, views:list[ViewInfo_base])->FigCanvas:

        # Scale figure based on window size
        plot_width, plot_hight = self.view_plotter.plot_figure(views,
                                                   size=tuple([self.winfo_width(), 0]),
                                                   can_expand = [False, True])

        if plot_hight != 0:
            self.plot.configure(height=plot_hight)
            self.canvas.draw()
            A.c = self.canvas
            if self.hidden: self.__show_plots()

            # Add scroll bars if required
            make_scrolls(views=views, scroll_bar=self.test_scroll)

            # Plot keys if possible
            make_keys(views=views)
                
        elif plot_hight == 0 and not self.hidden:
            self.__hide_plots()
            return    

        #self.canvas.mpl_connect('motion_notify_event',self.on_mouse_move)
        return self.canvas

def make_keys(views:list[ViewInfo_base]):
    key_fig = KeyCanvas.get_figure()
    if not isinstance(key_fig, Figure): return
    key_fig.clear()
    
    # Find the number keys that need to be plotted
    key_count = sum([view.has_key() for view in views])
    if key_count == 0:
        KeyCanvas.hide_canvas()
        return
    
    # Make a gridspec for all keys
    gs = GridSpec(nrows=key_count, ncols=1)
    for i, view in enumerate(views):
        ax = key_fig.add_subplot(gs[i])
        view.make_key(ax,(0,0))

    KeyCanvas.show_canvas()

def make_scrolls(views:list[ViewInfo_base], scroll_bar:ctk.CTkSlider):
    # Find the list of views that require scroll bars
    x_scroll_views = [view for view in views if view.should_add_x_scroll()]

    print(x_scroll_views)
    A.a = x_scroll_views[0]
    min, max, window = x_scroll_views[0].get_x_scroll_params()
    #scroll_bar.configure(command=A.test_scroll)
    scroll_bar._button_length = 20
    scroll_bar.configure(command = A.test_scroll, from_ = min, to = max-window)

class A:
    a:ViewInfo_base
    c:FigCanvas
    def test_scroll(val):
        A.a.scroll_x(val)
        A.c.draw()
