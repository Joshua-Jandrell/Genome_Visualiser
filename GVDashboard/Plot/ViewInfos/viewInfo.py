"""
The viewInfo call is used to define how each view should be plotted on the canvas.
"""
import numpy as np
from numpy.typing import NDArray
from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
from matplotlib.widgets import Slider, Button, RadioButtons

from mpl_toolkits.axes_grid1 import make_axes_locatable

from VCF.filterInfo import DataSetInfo
from Util.box import Box
from Util.event import Event

def inch_to_cm(inches:float)->float:
    """Converts inches to centimeters"""
    return inches * 2.54

BASE_TYPE_KEY = "BASE"

class ViewInfo_base:
    """
    Base class used to define and plot different views
    """
    def __init__(self) -> None:
        self.plots = []
        self.dataset_info = None
        self.link_to_prev = True # Link the 'long' axis of this plot to the plot that came before it.
        self.link_to_next = True # Link the 'long' axis of this plot to the next plot
        self._has_key = False
        self._view_type = BASE_TYPE_KEY
        """Defines what type of views this view can be combined with."""

        
        self.update_event = Event()
        """
        Event to be called when a major update is made to a view info.\n
        All listeners should accept view info base as their only argument.
        """

        self.key_row_size = 12
        """The type key is used to link like views."""

        self.pos_in_set = -1 
        """The position of te plot in the set."""

        self.last_in_set = False
        # Set a default dataset for the view
        
    def set_data(self, dataset_info:DataSetInfo):
        self.dataset_info = dataset_info

    def get_data(self)->DataSetInfo|None:
        """
        Returns the current dataset info.\n
        Warning: do not keep a reference to this dataset, this is so that it can be deleted correctly 
        """
        return self.dataset_info
    
    def get_plot_count(self)->int:
        """Returns the number of plots expected"""
        return 1
    def get_height_weights(self)->list[int]:
        return [1]
    
    def get_key_size(self)->int:
        return 4 * self.key_row_size
    
    def get_desired_size(self)->list[int]:
        """
        Returns the the hight, in pixes, that the given plot will ideally occupy.
        """
        return [500]
    
    def make_plots(self,axs:list[Axes],size:tuple[int,int], plot_box:Box)->str:
        """
        Method used to plot the data on a figure\n
        Returns the axis used for plotting and a log-string containing any errors or notes\n
        NOTE: This function must be overridden, only then can the `ViewInfo_base` class is implemented.
        """
        pass
    def make_key(self, axs, size):
        pass
    def fit_to_size(self,size:tuple[int,int]):
        """
        Scale the view to comfortably fit into the given size.
        """
        pass
    def can_plot(self)->bool:
        """Returns true if the view can be plotted."""
        return self.dataset_info is not None and self.dataset_info.get_data_wrapper() is not None
    def can_link(self, other):
        """Returns `True` if two view infos are compatible to be linked."""
        return self._view_type == other._view_type
    def has_key(self)->bool:
        return self._has_key
    
    # === Group/set type information ===

    def is_fist_in_set(self):
        return self.pos_in_set == 0
    
    def get_view_type(self):
        return self._view_type
    
    def get_set_views(self)->list:
        """
        Returns any addtional view that may supplement this widgets group.
        """
        return []
    
    # Scrolling information 
    def should_add_x_scroll(self)->bool:
        """Returns true if the graph requires a scroll bar in the x direction."""
        return False
    
    def get_x_scroll_params(self)->tuple[float, float, float]:
        """Returns a tuple of min value, max value and widow size."""
        return 0,0,0
    
    def scroll_x(self, x_pos:float):
        """
        Scrolls the views left most point to the given x position.\n
        MUST be overridden for functionality 
        """
        print("Warning scroll not possible")
        pass
    
############################################################################################################

class viewSetManager:
    """Class used to store information about a group of linked (or similar) views."""
    TOP_PADDING = 50
    BOTTOM_PADDING = 20
    LEFT_PADDING = 30
    RIGHT_PADDING = 20
  
    def __init__(self,stack=True, view_info:ViewInfo_base|None = None) -> None:
        """
        Construct a plot set manager to link plots to a set of plots relating to the given axis.\n
        If stack is true views will be added and linked vertically.
        """
        self.is_linked = False
        self.views:list[ViewInfo_base] = []
        self.__stack = stack

        if view_info is not None:
            self.link(view_info)

        "Link new plot vertically if stack set to true. " 
    def link(self,view_info:ViewInfo_base)->bool:
        """
        Link a new set of axes to the view set manger if type keys are compatible.\n
        Returns true if linking was successful.
        """
        # check to see if a link has occurred
        if not self.is_linked:
            #Link first view into view set.
            #self.ax =ax
            self.view_type = view_info.get_view_type
            self.base_info = view_info
            self.is_linked = True
            view_info.pos_in_set = 0
            self.views.append(view_info)
            return True

        # The base type view is not compatible, event with itself, by default.
        if self.view_type == BASE_TYPE_KEY or not view_info.can_link(self.base_info): return False

        # Updated last view 
        view_info.pos_in_set = len(self.views)
        self.views[-1].last_in_set = False
        view_info.last_in_set = True
        self.views.append(view_info)

        return True
    
    def get_desired_hight(self):
        """Returns the desired hight of the full view set"""
        return sum([sum(view.get_desired_size()) for view in self.views])
    
    def plot(self, ax:Axes, size:tuple[int,int], plot_box:Box):
        """Plot all views in the view set on the given axes"""

        # Get addtional views from the group:
        additional_views = []
        for view in self.views:
            additional_views += view.get_set_views()

        _views:list[ViewInfo_base] = additional_views + self.views
        hights=[]
        ax.set_axis_off()
        for view in _views:
            hights += view.get_desired_size()
        h, ratios = length_and_ratios(hights)
        bounds = np.concatenate((np.array([0]), np.cumsum(ratios)),axis=0)

        bound_index = 0
        # Get relative box bounds
        left_edge, top_edge = plot_box.get_top_left() # Get the top of the bounding plot box (which hold the size relative to the the full figure)
        right_edge = plot_box.get_right()
        for view in _views:
            axs =[] 
            
            # Move top edge down as more axes are packed 
            start_bound = top_edge - bounds[bound_index] * plot_box.get_height() # scale by proportional hight
            for _ in range(view.get_plot_count()):
                bottom = 1-bounds[bound_index+1]
                top = 1-bounds[bound_index]
                axs.append(ax.inset_axes([0,bottom,1,top-bottom],sharex=ax))
                bound_index += 1  
            end_bound = top_edge - bounds[bound_index] * plot_box.get_height() # scale by proportional hight
            
            view.make_plots(axs=axs, size=size, plot_box=Box.from_points(top_left=(left_edge,start_bound), bottom_right=(right_edge, end_bound)))

def get_view_sets(view_infos:ViewInfo_base)->list[viewSetManager]:
    """Iterate through a list of view infos and return a list of view set managers for those views"""
    view_sets = []
    live_set = viewSetManager()
    for info in view_infos:
        # Try to link a view to the live set
        if not live_set.link(info):
            # Link failed, append the live set an make a new one for this info
            view_sets.append(live_set)
            live_set = viewSetManager(info)
    # Link the final set 
    view_sets.append(live_set)

    return view_sets

def length_and_ratios(requested_lengths:list[int])->tuple[int,NDArray]:
    """Task a list of lengths and return the total length an ratios between lengths."""
    full_length = sum(requested_lengths)
    weights = np.array(requested_lengths)/full_length
    return full_length, weights

def plot_sets(view_sets:list[viewSetManager], fig:Figure, size:tuple[int,int]=tuple([0,0]), can_expand=tuple([False, False]))->int:
    """Plots the list of view sets on the given figure and returns its desired hight in pixels"""

    # Determine which axes can expand
    can_expand = tuple([can_expand[0] or size[0] == 0,can_expand[1] or size[1] == 0])

    fig_hights = []
    for view_set in view_sets:
        fig_hights.append(view_set.get_desired_hight())

    fig_widths = [size[0]]

    # Get length and ratios of view sets
    fig_hight, h_ratios = length_and_ratios([viewSetManager.TOP_PADDING]+fig_hights+[viewSetManager.BOTTOM_PADDING])
    fig_width, w_ratios = length_and_ratios([viewSetManager.LEFT_PADDING]+fig_widths+[viewSetManager.RIGHT_PADDING])

    # Scale figure side padding
    fig.subplots_adjust(left=w_ratios[0], right=1-w_ratios[-1], top=1-h_ratios[0], bottom=h_ratios[-1])

    # Create a gridspec to manage all figure set subplots
    nrows = len(view_sets)
    ncols = 1
    gs = GridSpec(nrows=nrows, ncols=ncols,height_ratios=fig_hights,figure=fig)

    # iterate through figures sets, assign each of them a subplot
    top_edge = 1-h_ratios[0]
    for i, view_set in enumerate(view_sets):
        x = w_ratios[0]
        y = top_edge
        w = w_ratios[1]
        h = h_ratios[i+1]
        # Shift top edge down to account for the next view
        top_edge -= h
        # Construct bounding box
        box = Box(x,y,w,h)
        # Make axis for view set 
        ax = fig.add_subplot(gs[i])
        view_set.plot(ax=ax, size=size, plot_box=box)

    return fig_width, fig_hight



#def scale_sets(view_sets:list[viewSetManager], fig:Figure, size:tuple[int,int]=tuple([0,0]), can_expand=tuple([False, False])):
    """Function used to update the scale of a list of view sets without re-plotting"""

    
