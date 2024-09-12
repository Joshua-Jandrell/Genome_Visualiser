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

from VCF.filterInfo import DataSetInfo
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
        self.type_key = BASE_TYPE_KEY
        """The type key is used to link like views."""
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
    
    def get_desired_size(self)->list[int]:
        """
        Returns the the hight, in pixes, that the given plot will ideally occupy.
        """
        return [500]
    
    def make_plots(self,axs:list[Axes],show_x:bool,show_y:bool)->str:
        """
        Method used to plot the data on a figure\n
        Returns the axis used for plotting and a log-string containing any errors or notes\n
        NOTE: This function must be overridden, only then can the `ViewInfo_base` class is implemented.
        """
        pass
    def can_plot(self)->bool:
        """Returns true if the view can be plotted."""
        return self.dataset_info is not None and self.dataset_info.get_data_wrapper() is not None
    def can_link(self, other):
        """Returns `True` if two view infos are compatible to be linked."""
        return self.type_key == other.type_key
    def has_key(self)->bool:
        return self._has_key
    
############################################################################################################

class viewSetManager:
    """Class used to store information about a group of linked (or similar) views."""

  
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
            self.type_key = view_info.type_key
            self.base_info = view_info
            self.is_linked = True
            self.views.append(view_info)
            return True

        # The base type view is not compatible, event with itself, by default.
        if self.type_key == BASE_TYPE_KEY or not view_info.can_link(self.base_info): return False

        self.views.append(view_info)

        return True
    
    def get_desired_hight(self):
        """Returns the desired hight of the full view set"""
        return sum([sum(view.get_desired_size()) for view in self.views])
    
    def plot(self, ax:Axes, size:tuple[int,int]):
        """Plot all views in the view set on the given axes"""
        hights=[]
        ax.set_axis_off()
        for view in self.views:
            hights += view.get_desired_size()
        h, ratios = length_and_ratios(hights)
        bounds = np.concatenate((np.array([0]), np.cumsum(ratios)),axis=0)

        bound_index = 0
        for view in self.views:
            axs =[] 
            axs.clear()
            for _ in range(view.get_plot_count()):
                bottom = bounds[bound_index]
                top = bounds[bound_index+1]
                axs.append(ax.inset_axes([0,bottom,1,top-bottom],sharex=ax))
                bound_index += 1  
            view.make_plots(axs, size)

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

    # Get length and ratios of view sets
    fig_hight, ratios = length_and_ratios(fig_hights)
    fig_width = size[0]

    # Create a gridspec to manage all figure set subplots
    nrows = len(view_sets)
    ncols = 1
    gs = GridSpec(nrows=nrows, ncols=ncols,height_ratios=fig_hights,figure=fig)

    # iterate through figures sets, assign each of them a subplot
    for i, view_set in enumerate(view_sets):
        # Make axis for view set 
        ax = fig.add_subplot(gs[i])
        view_set.plot(ax, size=size)
        print(f"Size here {size}")

    return fig_width, fig_hight
    
