"""
The viewInfo call is used to define how each view should be plotted on the canvas.
"""
from enum import Enum
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

class ViewPos(Enum):
    MAIN=1,
    """The main central plot of the view group."""
    LEFT=2,
    """Plotted to the left of the main plot."""
    TOP=3,
    """Plotted above the main plot"""
    LEFT_STAND_IN=4,
    """Plotted on left, but promoted to main view if no main view is present"""  


BASE_TYPE_KEY = "BASE"
X_STACK = 0
Y_STACK =1
STACK_MODE = X_STACK

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

        self._pos:ViewPos = ViewPos.MAIN
        """
        Defines where the view should be positioned in the group
        """

        self._can_compress = False
        
        self.update_event = Event()
        """
        Event to be called when a major update is made to a view info.\n
        All listeners should accept view info base as their only argument.
        """

        self.key_row_size = 12
        """The type key is used to link like views."""

        self.order_in_set = -1 
        """The order of the plot in the set."""

        self.last_in_set = False
        # Set a default dataset for the view

        self._priority = 0
        """How important is this view. Higher number indicate that it should be a main view if conflicts occur."""

        self._is_main = False
        """Set to true if this view is the main view."""

    def get_priority(self)->int:
        return self._priority

    def set_main(self, is_main:bool):
        self._is_main = is_main
        
    def get_view_pos(self)->ViewPos:
        return self._pos
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
        return [500]
    
    def get_desired_hight(self)->list[int]:
        """
        Returns the the hight, in pixes, that the given plot will ideally occupy.
        """
        return [500]
    
    def get_desired_width(self)->list[int]:
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
        return self.dataset_info is not None and self.dataset_info.get_data() is not None
    def can_link(self, other):
        """Returns `True` if two view infos are compatible to be linked."""
        return self._view_type == other._view_type
    def has_key(self)->bool:
        return self._has_key
    
    # === Group/set type information ===
    def is_compressible(self)->bool:
        """Returns true if the given view can be scaled down."""
        return self._can_compress

    def is_fist_in_set(self):
        return self.order_in_set == 0
    
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
    TOP_PADDING = 60
    BOTTOM_PADDING = 60
    LEFT_PADDING = 60
    RIGHT_PADDING = 20
  
    def __init__(self,view_info:ViewInfo_base|None = None) -> None:
        """
        Construct a plot set manager to link plots to a set of plots relating to the given axis.\n
        If stack is true views will be added and linked vertically.
        """
        self.is_linked = False
        self.view_type = None
        self.views:list[ViewInfo_base] = []
        self.additional_views:list[ViewInfo_base] = []
        self.main_view:ViewInfo_base = None
        self.left_views:list[ViewInfo_base] = []

        if view_info is not None:
            self.link(view_info)

        "Link new plot vertically if stack set to true. " 

    def _has_main(self):
        """Returns true is the given viewset has a main view."""
        return self.main_view is not None
    
    def link(self,view_info:ViewInfo_base)->bool:
        """
        Link a new set of axes to the view set manger if type keys are compatible.\n
        Returns true if linking was successful.
        """

        # The base type view is not compatible, event with itself, by default.
        if self.is_linked and (self.view_type == BASE_TYPE_KEY or not view_info.can_link(self.base_info)): return False

        # check to see if a link has occurred
        if not self.is_linked:
            self.view_type = view_info.get_view_type
            self.base_info = view_info
            self.is_linked = True

        # Add view to correct list depending on intended position
        _pos = view_info.get_view_pos()
        _view_list = self.views
        if _pos == ViewPos.LEFT:
            _view_list = self.left_views

        if _pos == ViewPos.MAIN:
            self.main_view = view_info


        view_info.order_in_set = len(_view_list)

        if view_info.order_in_set > 1:
            _view_list[-1].last_in_set = False
        _view_list.append(view_info)
        self.additional_views += view_info.get_set_views()

        return True
    
    def get_desired_hight(self):
        """Returns the desired hight of the full view set"""
        if STACK_MODE == Y_STACK: return sum([sum(view.get_desired_hight()) for view in self.views+self.additional_views])
        else: return sum(self.views[0].get_desired_hight())

    def plot(self, fig:Figure, ax:Axes, size:tuple[int,int], plot_box:Box, pad_l = 20, pad_r = 20, pad_t = 20, pad_b = 20)->tuple[int, int]:
        """Plot all views in the view set on the given axes"""



        # Find main view 
        if not self._has_main():
            for view in self.left_views:
                if view.get_view_pos() == ViewPos.LEFT_STAND_IN:
                    if self.main_view is None or self.main_view.get_priority() < view.get_priority():
                        # If there are multiple candidates main views, select the one with the highest priority
                        self.main_view = view

        # Remove main for view lists 
        if self._has_main():
            if self.main_view in self.views: self.views.remove(self.main_view)
            elif self.main_view in self.left_views: self.left_views.remove(self.main_view)


        print(f"min view is {self.main_view}")
        print(f"The size if {size}")
        print(f"the plot bo is {plot_box.get_width()} by {plot_box.get_height()}")

        # Find width of left views
        left_widths = []
        for v in self.left_views:
            left_widths += v.get_desired_width()
        left_width = sum(left_widths)

        # Find hight of top views
        top_hights = []
        for v in self.views:
            top_hights += v.get_desired_hight()
        top_hight = sum(top_hights)

        # Find dimensions of main view 
        desired_main_width = sum(self.main_view.get_desired_width())
        available_main_width = size[0] - (left_width + pad_l + pad_r)
        main_w = min(available_main_width, desired_main_width)
        main_h = min(size[1] - (top_hight + pad_t + pad_b), sum(self.main_view.get_desired_hight()))

        # adjust right padding if needed
        if available_main_width > desired_main_width:
            pad_r += (available_main_width - desired_main_width)

        print(f"the dims are {main_w} by {main_h}")
        print(f"the widths arequired {left_widths}")

        # Get ratios and total length/hight
        w, w_ratios = length_and_ratios([pad_l]+left_widths+[main_w, pad_r])
        h, h_ratios = length_and_ratios([pad_t]+top_hights+[main_h, pad_b])
        print(f"w={w} and wr = {w_ratios}")

        
        # Make the main plot
        self.main_view.make_plots([ax],(main_w, main_h))

        # Make a divider to locate and points for main axes
        divider = make_axes_locatable(ax)

        plot_i = 0
        n_plots = len(self.left_views)
        for view in reversed(self.left_views):
            _axes:list[Axes] = []
            _x_size = 0
            for _ in range(view.get_plot_count()):
                prop_size = left_widths[-plot_i]/main_w # Add 1 because first ratio will be padding
                _axes.append(divider.append_axes('left',size=f"{prop_size*100}%",pad=0, sharey = ax)) 
                _x_size += left_widths[-plot_i]
                plot_i += 1
                _axes.reverse()
            view.make_plots(_axes, size=(_x_size, main_h))
        
        plot_i = 1
        for view in self.views:
            _axes:list[Axes] = []
            for _ in range(view.get_plot_count()):
                _axes.append(divider.append_axes('top',size=h_ratios[plot_i],pad=0))
                plot_i += 1
            view.make_plots(_axes)


        # Scale figure padding
        fig.subplots_adjust(left=w_ratios[0], right=1-w_ratios[-1], top=1-h_ratios[0], bottom=h_ratios[-1])
        

        return (w,h)

    def __plot_vertical_stack(self, ax:Axes, size:tuple[int,int], plot_box:Box):
        """Method used to pack like views horizontally instead of vertically."""

        widths = []
        fixed_width = 0
        n_compressible = 0
        for view in self.views:
            widths += view.get_desired_width()
            if not view.is_compressible():
                fixed_width += sum(view.get_desired_width())
            else:
                n_compressible +=1 
        w = sum(widths)
        if w > size[0]:

            # Find the width available for compressible views 
            rem_width = size[0]-fixed_width
            compressible_width = rem_width/n_compressible

            # Get array of all widths
            widths = []
            for view in self.views:
                if view.is_compressible(): widths.append(compressible_width)
                else: widths += view.get_desired_width()
        else:
            widths += [size[0]-w]
        # find hights 'normally'
        heights=[]
        for view in self.additional_views + [self.views[0]]: # only the first view is needed here... all have same hight
            heights += view.get_desired_hight()

        h, ratios = length_and_ratios(heights)
        bounds = np.concatenate((np.array([0]), np.cumsum(ratios)),axis=0)
        bound_index = 0
        # Get relative box bounds
        left_edge, top_edge = plot_box.get_top_left() # Get the top of the bounding plot box (which hold the size relative to the the full figure)
        right_edge = plot_box.get_right()
        # Plot addtional views (on top) only
        for view in self.additional_views:
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

        # Now plot vertical views 
        w, ratios = length_and_ratios(widths)
        bounds = np.concatenate((np.array([0]), np.cumsum(ratios)),axis=0)
        bound_index = 0
        for view in self.views:
            axs =[] 
            # Move top edge down as more axes are packed 
            start_bound = top_edge - bounds[bound_index] * plot_box.get_height() # scale by proportional hight
            for _ in range(view.get_plot_count()):
                left = bounds[bound_index]
                right = bounds[bound_index+1]
                axs.append(ax.inset_axes([left,0,right-left,1],sharey=ax))
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
    if full_length <= 0: return 0, np.array([])
    weights = np.array(requested_lengths)/full_length
    return full_length, weights

def plot_sets(view_sets:list[viewSetManager], fig:Figure, size:tuple[int,int]=tuple([0,0]), can_expand=tuple([False, False]))->int:
    """Plots the list of view sets on the given figure and returns its desired hight in pixels"""

    # Determine which axes can expand
    # can_expand = tuple([can_expand[0] or size[0] == 0,can_expand[1] or size[1] == 0])

    # fig_hights = []
    # for view_set in view_sets:
    #     fig_hights.append(view_set.get_desired_hight())

    # fig_widths = [size[0]]

    # # Get length and ratios of view sets
    # fig_hight, h_ratios = length_and_ratios([viewSetManager.TOP_PADDING]+fig_hights+[viewSetManager.BOTTOM_PADDING])
    # fig_width, w_ratios = length_and_ratios([viewSetManager.LEFT_PADDING]+fig_widths+[viewSetManager.RIGHT_PADDING])

    # print(h_ratios, " addddddddd")
    # print(w_ratios, " wwwww")
    # # Scale figure side padding
    # fig.subplots_adjust(left=w_ratios[0], right=1-w_ratios[-1], top=1-h_ratios[0], bottom=h_ratios[-1])

    # # Create a gridspec to manage all figure set subplots
    # nrows = len(view_sets)
    # ncols = 1
    # gs = GridSpec(nrows=nrows, ncols=ncols,height_ratios=fig_hights,figure=fig)

    # # iterate through figures sets, assign each of them a subplot
    # top_edge = 1-h_ratios[0]
    # for i, view_set in enumerate(view_sets):
    #     x = w_ratios[0]
    #     y = top_edge
    #     w = w_ratios[1]
    #     h = h_ratios[i+1]
    #     # Shift top edge down to account for the next view
    #     top_edge -= h
    #     # Construct bounding box
    #     box = Box(x,y,w,h)
    #     # Make axis for view set 
    #     ax = fig.add_subplot(gs[i])

    #     true_h = fig_hight*h
    #     true_w = fig_width*w

    print(f"TODO: fix size")
    ax = fig.add_subplot(111)
    fig_width, fig_hight = view_sets[0].plot(fig=fig, ax=ax, size=(size[0],500), plot_box=Box(0,0,1,1))


    return fig_width, fig_hight



#def scale_sets(view_sets:list[viewSetManager], fig:Figure, size:tuple[int,int]=tuple([0,0]), can_expand=tuple([False, False])):
    """Function used to update the scale of a list of view sets without re-plotting"""

    
