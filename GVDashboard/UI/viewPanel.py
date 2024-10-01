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
from Plot.scrollWidget import ScrollManager
from Plot.plotUpdate import PlotUpdate

from Util.event import Event

X_VIEW_PAD = 40
Y_VIEW_PAD = 100

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
        self.plot_mount = ctk.CTkFrame(self.canvas_frame, fg_color='transparent')
        self.canvas =  FigCanvas(self.fig, master=self.plot_mount)
        
        # Create a view plotter for the canvas
        self.view_plotter = ViewPlotter(self.fig)
        self.toolbar = NavToolbar(window=self,canvas=self.canvas)
        self.plot = self.canvas.get_tk_widget()

        self.plot_mount.pack(side=ctk.TOP, expand=True)

        # Set canvas to be used by scroll widgets 
        ScrollManager.set_scroll_canvas(self.plot)

        # Set plot update to update the plot
        PlotUpdate.set_canvas(self.canvas)


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
        self.plot.pack(side="top", expand=True, fill='both')
        self.hidden = False

    def make_plot(self, views:list[ViewInfo_base])->None:

        ScrollManager.clear_scrolls()
        # Filter for only valid views
        views = [view for view in views if isinstance(view,ViewInfo_base) and view.can_plot()]
        if len(views) == 0: 
            self.__hide_plots()
            KeyCanvas.hide_canvas()
            return
        


        # Scale figure based on window size
        _w = self.winfo_width()-X_VIEW_PAD
        _h = self.winfo_height()-Y_VIEW_PAD
        plot_width, plot_height = self.view_plotter.plot_figure(views,
                                                   size=(_w,_h),
                                                   can_expand = [False, True])
        if plot_height != 0:

            if self.hidden: self.__show_plots()
            self.fig.set_size_inches(h=plot_height/100, w=plot_width/100)
            self.plot.configure(height=plot_height, width=plot_width)
            self.plot_mount.configure(height=plot_height, width=plot_width)
            self.canvas.draw()

            
            # Plot keys if possible
            make_keys(views=views)
                
        elif plot_height == 0 and not self.hidden:
            self.__hide_plots()

            return    

        #self.canvas.mpl_connect('motion_notify_event',self.on_mouse_move)
        return self.canvas

def make_keys(views:list[ViewInfo_base]):
    key_fig = KeyCanvas.get_figure()
    key_fig.clear()
    if not isinstance(key_fig, Figure): return
    
    # Find the number keys that need to be plotted
    key_views = [view for view in views if view.has_key()]
    key_count = len(key_views)
    if key_count == 0:
        KeyCanvas.hide_canvas()
        return

    # Make a gridspec for all keys
    gs = GridSpec(nrows=key_count, ncols=1)
    for i, view in enumerate(key_views):
        ax = key_fig.add_subplot(gs[i])
        view.make_key(ax,(0,0))

    KeyCanvas.show_canvas()
