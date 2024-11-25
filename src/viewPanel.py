# This script contains the code for the main visualiser view panel

from typing import Tuple, Any
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavToolbar

from matplotlib.figure import Figure 
from matplotlib.gridspec import GridSpec as GridSpec

from Plot.ViewInfos.viewInfo import get_view_sets, ViewSetManager, ViewInfo_base
from VCF.dataSetConfig import DataSetConfig, GlobalDatasetManager

from Plot.keyCanvas import KeyCanvas
from Plot.inspector import InspectorPanel
from Plot.scrollWidget import ScrollWidget

from Util.box import Box

from _config_ import ERROR_RED

X_VIEW_PAD = 40
Y_VIEW_PAD = 100
DEFAULT_DPI = 100
IS_DYNAMIC = False

def px_to_inches(px:int, dpi:float=DEFAULT_DPI):
    """
    Converts pixes to inches
#     """
class FigureMount(ctk.CTkFrame):
    DPI = DEFAULT_DPI
    """
    Class used to store and pack a figure.
    """
    def __init__(self, master: Any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.fig = Figure(dpi = self.DPI)
        self.plot_mount = ctk.CTkFrame(self, fg_color='transparent')
        self.canvas =  FigCanvas(self.fig, master=self.plot_mount)

        self.toolbar = NavToolbar(window=self,canvas=self.canvas)
        self.plot = self.canvas.get_tk_widget()

        self.toolbar.pack(side="top", fill="x", expand=True)
        self.plot_mount.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        self.plot.pack(side=ctk.TOP, expand=True)


        # Create scroll bars
        self.vsb = ScrollWidget(self.plot, orientation='vertical')
        self.hsb = ScrollWidget(self.plot, orientation='horizontal')
        self.hsb2 = ScrollWidget(self.plot, orientation='horizontal') # Needed is special cases where there are two main axes

        # Subscribe to scroll events
        self.vsb.scroll_event.add_listener(self.__on_scroll)
        self.hsb.scroll_event.add_listener(self.__on_scroll)

        self._viewset:ViewSetManager|None = None

        # subscribe to canvas mouse/over event 
        self.fig.canvas.mpl_connect('motion_notify_event', self.__on_mouse_move)

    def __on_mouse_move(self, event):
        
        # Get viewinfo display data
        info = self._viewset.get_view_info(event=event)
        InspectorPanel.display_info(info)
        
        #self.canvas.draw_idle()


    @classmethod
    def _place_scroll(cls, scroll:ScrollWidget, scroll_box:Box):
        scroll.place(relx=scroll_box.get_left(),
                        rely=1-scroll_box.get_top(),
                        relwidth = scroll_box.get_width(),
                        relheight = scroll_box.get_height(),
                        anchor='nw')


    def __on_scroll(self):
        if not IS_DYNAMIC:
            self.canvas.draw_idle()
        
    def clear(self):
        self.fig.clear()
        self.hsb.place_forget()
        self.vsb.place_forget()

    def plot_set(self,view_set:ViewSetManager, size:tuple[float,float]):
        ax = self.fig.add_subplot(111)
        fig_width, fig_hight, x_scroll_box, y_scroll_box = view_set.plot(fig=self.fig, ax=ax, size=size)
        self.plot.configure(width=fig_width, height=fig_hight)

        self.canvas.draw_idle()
        self.toolbar.update()

        # Make scroll bars if required
        if x_scroll_box is not None:
            self.hsb.set_view(view=view_set.main_view) # NB this must be done first
            self._place_scroll(self.hsb, x_scroll_box)

        if y_scroll_box is not None:
            self.vsb.set_view(view=view_set.main_view) # NB this must be done first
            self._place_scroll(self.vsb, y_scroll_box)
            
        if self._viewset is not None:
            self._viewset.main_view.update_event.remove_listener(self._on_main_update)
        # Subscribe to main view update event 
        view_set.main_view.update_event.add_listener(self._on_main_update)
        self._viewset = view_set


    def _on_main_update(self,viewinfo:ViewInfo_base|None, type):
        
        if IS_DYNAMIC and viewinfo is not None:
            self.canvas.draw_idle()

class PlotLoadPanel(ctk.CTkFrame):
    def __init__(self, master: Any, fg_color: str | Tuple[str] | None = None, delay_ms = 1):
        super().__init__(master, fg_color=fg_color, corner_radius=0)

        label = ctk.CTkLabel(self,text="Plotting...")
        label.pack(expand=True, fill=ctk.BOTH)

        self.delay = delay_ms
        self.__plotting_flag = False
    def show(self):
        self.__plotting_flag = True
        #self.after(self.delay,self.__show_self)
        self.__show_self()
    def hide(self):
        self.__plotting_flag = False
        self.place_forget()
        
    def __show_self(self):
        if self.__plotting_flag or True:
            self.place(x=0,y=0,relw=1,relh=1)
        



class ViewPanel(ctk.CTkFrame):
    __instance = None
    __active = True

    def set_active(active:bool):
        ViewPanel.__active = active

    def set_plots(views:list[ViewInfo_base], block_popups=False):
        if ViewPanel.__active and isinstance(ViewPanel.__instance, ViewPanel):
            ViewPanel.__instance.make_plot(views=views, block_popups=block_popups)

    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent")
        
        # There can only be one instance 
        assert(not isinstance(ViewPanel.__instance, ViewPanel))

        self.scroll_frame = ctk.CTkScrollableFrame(self)

        self.__mounts:list[FigureMount] = []
        self.__mounts_in_use:list[FigureMount] = [] 

        # Create button to let users quickly select datasets
        self.data_select_button = ctk.CTkButton(self, text="Select Dataset File",
                                                command=lambda: DataSetConfig.open()
        )

        self._error_frame = ctk.CTkLabel(self, text="Error: cannot plot.",
                                            text_color="red")


        self.__plot_load_panel = PlotLoadPanel(self)

        self.__hide_plots()
        self.__show_select_button()
        ViewPanel.__instance = self

    def __get_mount(self)->FigureMount:
        """Returns a new plot mount."""
        if len(self.__mounts) > 0:
            new_mount = self.__mounts.pop()
        else:
            new_mount = FigureMount(self.scroll_frame, fg_color="white")

        self.__mounts_in_use.append(new_mount)
        new_mount.pack(side=ctk.TOP, fill=ctk.X, expand=True)
        
        return new_mount

    def __hide_plots(self):
        """Hides the plot canvas. Should be called when no figures are plotted."""
        # hide canvas and toolbar
        for mount in self.__mounts_in_use:
            mount.clear()
            mount.pack_forget()
            self.__mounts.append(mount)
        self.__mounts_in_use.clear()  

        self.scroll_frame.pack_forget()

        self.hidden = True
         

    def __show_plots(self):
        self.data_select_button.place_forget()
        self._error_frame.place_forget()
        self.scroll_frame.pack(side="top", fill="both", expand=True)
        self.hidden = False

    def make_plot(self, views:list[ViewInfo_base], block_popups:bool=False)->None:

        views = [view for view in views if isinstance(view,ViewInfo_base) and view.has_data()]
        # Filter for view with data
        no_views = len(views) == 0
        no_data = len(GlobalDatasetManager.get_datasets())==0
        # Filter for only valid views
        views = [view for view in views if isinstance(view,ViewInfo_base) and view.can_plot()]
        if len(views) == 0: 
            if no_data:
                if not block_popups:
                    DataSetConfig.open(register_on_create = True)
                self.__show_select_button()
            elif no_views:
                self.__show_no_plots_frame()
            else:
                self.__show_no_values_frame()

            self.__hide_plots()
            KeyCanvas.hide_canvas()
            return
        
        
        self.__plot_load_panel.show()
        self.__plot_load_panel.update()
        self.__hide_plots()
               
        # Pack plot frame
        self.__show_plots()
        
        # group views into a collection of view sets
        view_sets = get_view_sets(views)
        
        # Scale figure based on window size
        _w = self.winfo_width()-X_VIEW_PAD
        _h = self.winfo_height()-Y_VIEW_PAD

        for view_set in view_sets:
            mount = self.__get_mount()
            mount.plot_set(view_set,size=(_w,_h))

        # Plot keys if possible
        #make_keys(views=views)

        #self.__plot_load_panel.hide()
        self.__plot_load_panel.hide()

    def __show_select_button(self):
        """Shows the dataset select button."""
        # show dataset selection button 
        self._error_frame.place_forget()
        self.data_select_button.place(relx=.5, rely=.5, anchor="center")

    def __show_no_plots_frame(self):
        """Shows frame indicating that there are not plots."""
        self.data_select_button.place_forget()
        self._error_frame.configure(text="Error: Cannot plot:\n No plots selected.\n Please select view from plot tap on left of screen.")
        self._error_frame.place(relx=.5, rely=.5, anchor="center")
    def __show_no_values_frame(self):
        """Shows frame indicating that there is not data matching the given filter."""
        self.data_select_button.place_forget()
        self._error_frame.configure(text="Dataset is empty\n All data has been excluded from dataset due it the current filter parameters.\n Please reconfigure filters to include data to plot.")
        self._error_frame.place(relx=.5, rely=.5, anchor="center")
           


#def make_keys(views:list[ViewInfo_base]):
    # key_fig = KeyCanvas.get_figure()
    # key_fig.clear()
    # if not isinstance(key_fig, Figure): return
    
    # # Find the number keys that need to be plotted
    # key_views = [view for view in views if view.has_key()]
    # key_count = len(key_views)
    # if key_count == 0:
    #     KeyCanvas.hide_canvas()
    #     return

    # h = KeyCanvas.get_height()/key_count
    # # Make a gridspec for all keys
    # gs = GridSpec(nrows=key_count, ncols=1)
    # for i, view in enumerate(key_views):
    #     ax = key_fig.add_subplot(gs[i])
    #     view.make_key(ax,(0,h))

    # KeyCanvas.show_canvas()


