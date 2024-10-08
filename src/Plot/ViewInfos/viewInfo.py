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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

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
    TOP_STAND_IN=5
    """Plotted on top, but promoted to main view if no main view is present""" 



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
        self._axs:list[Axes] = []
        self._plot_size = (0,0)
        """
        Defines where the view should be positioned in the group
        """

        self._can_compress = False
        
        self.update_event = Event()
        """
        Event to be called when a major update is made to a view info.\n
        All listeners should accept view info base and string = ['move', 'scale', 'draw'] as its arguments
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

        self._on_top = False
        """Set to ture if the given view is on top"""

        self._group_title = "Plot group"

        self._key_rows = 1

        self._is_plotted = False

    def get_priority(self)->int:
        return self._priority

    def set_main(self, is_main:bool):
        self._is_main = is_main
    def get_main(self)->bool:
        return self._is_main
        
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
    
    def get_plot_names(self)->list[str]:
        """Returns the name of the plot axes lables.\n"""
        return ["Plot"]
    
    def set_group_title(self, title:str):
        self._group_title = title
    
    def get_group_title(self)->str:
        return self._group_title
    
    def is_plotted(self)->bool:
        """Returns true if the current view has been plotted."""
        return self._is_plotted

    def set_plotted(self, plotted):
        self._is_plotted = plotted    

    
    def make_plots(self,axs:list[Axes],size:tuple[int,int])->str:
        """
        Method used to plot the data on a figure\n
        Returns the axis used for plotting and a log-string containing any errors or notes.\n
        NOTE: This function must be overridden, only then can the `ViewInfo_base` class is implemented.
        """
        self._axs = axs
        self._plot_size = size

    def make_key(self, key_ax):
        pass
    def fit_to_size(self,size:tuple[int,int]):
        """
        Scale the view to comfortably fit into the given size.
        """
        pass
    def can_plot(self)->bool:
        """Returns true if the view can be plotted."""
        return self.has_data()
    
    def has_data(self)->bool:
        """Returns true if the given viewinfo has a dataste to plot."""
        return self.dataset_info is not None and self.dataset_info.get_data() is not None
    def can_link(self, other):
        """Returns `True` if two view infos are compatible to be linked."""
        return self._view_type == other._view_type
    def has_key(self)->bool:
        return self._has_key
    def get_key_rows(self)->int:
        return self._key_rows
    
    # === Group/set type information ===
    def is_compressible(self)->bool:
        """Returns true if the given view can be scaled down."""
        return self._can_compress

    def is_fist_in_set(self):
        return self.order_in_set == 0
    
    def set_on_top(self, on_top:bool):
        self._on_top = on_top

    def is_on_top(self)->bool:
        return self._on_top

    
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
        return self.get_x_scroll_params()[1] < 1
        
    
    def get_x_scroll_params(self)->tuple[float, float]:
        """Returns a tuple of current proportional scroll value and proportional scroll window size."""
        return 0,1
        
    
    def scroll_x(self, x_pos:float):
        """
        Scrolls the view's left most point to the given (proportional) x position.\n
        MUST be overridden for functionality 
        """
        raise Exception(f"x scroll not supported by view type {type(self)}")

    def should_add_y_scroll(self)->bool:
        """Returns true if the graph requires a scroll bar in the y direction."""
        return self.get_y_scroll_params()[1] < 1
    
    def get_y_scroll_params(self)->tuple[float, float]:
        """Returns a tuple of current proportional scroll value and proportional scroll window size."""
        return 0,1
    
    def scroll_y(self, y_pos:float):
        """
        Scrolls the view's top most point to the given (proportional) y position.\n
        MUST be overridden for functionality 
        """
        raise Exception(f"y scroll not supported by view type {type(self)}")
    
############################################################################################################

TOP_PADDING = 100
BOTTOM_PADDING = 60
LEFT_PADDING = 100
RIGHT_PADDING = 40
KEY_WIDTH = 200
KEY_HEIGHT = 40
KEY_PAD = 20
KEY_SIDE_PAD = 30

class ViewSetManager:
    """Class used to store information about a group of linked (or similar) views."""
    SCROLLBAR_BREADTH = 20
  
    def __init__(self,view_info:ViewInfo_base|None = None) -> None:
        """
        Construct a plot set manager to link plots to a set of plots relating to the given axis.\n
        If stack is true views will be added and linked vertically.
        """
        self.is_linked = False
        self.view_type = None
        self.top_views:list[ViewInfo_base] = []
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
        _view_list = self.top_views
        if _pos in [ViewPos.LEFT, ViewPos.LEFT_STAND_IN]:
            _view_list = self.left_views

        if _pos == ViewPos.MAIN:
            if self._has_main():
                # Check to see if current main is a stand-in
                if self.main_view.get_view_pos() in [ViewPos.LEFT_STAND_IN, ViewPos.TOP_STAND_IN]:
                    self.main_view.set_main(False)
                else: raise Exception("Double main view")
            self.main_view = view_info
            view_info.set_main(True)
        else:
            view_info.set_main(False)


        view_info.order_in_set = len(_view_list)

        if view_info.order_in_set > 1:
            _view_list[-1].last_in_set = False
        _view_list.append(view_info)
        self.additional_views += view_info.get_set_views()


        return True
    
    def get_desired_hight(self):
        """Returns the desired hight of the full view set"""
        if STACK_MODE == Y_STACK: return sum([sum(view.get_desired_hight()) for view in self.top_views+self.additional_views])
        else: return sum(self.top_views[0].get_desired_hight())

    def plot(self, fig:Figure, ax:Axes, size:tuple[int,int], pad_l = LEFT_PADDING, pad_r = RIGHT_PADDING, pad_t = TOP_PADDING, pad_b = BOTTOM_PADDING)->tuple[int, int, Box|None, Box|None]:
        """Plot all views in the view set on the given axes"""

        # Find main view 
        if not self._has_main():
            for view in self.left_views + self.top_views:
                if view.get_view_pos() in [ViewPos.LEFT_STAND_IN, ViewPos.TOP_STAND_IN, ViewPos.MAIN]:
                    if self.main_view is None or self.main_view.get_priority() < view.get_priority():
                        # If there are multiple candidates main views, select the one with the highest priority
                        if self.main_view is not None:
                            self.main_view.set_main(False)
                        self.main_view = view
                        view._is_main = True

        # Find width of left views
        left_widths = []
        for v in self.left_views:
            if not v.get_main():
                v.set_on_top(False)
                left_widths += v.get_desired_width()
        left_width = sum(left_widths)

        
        plot_top = self.main_view is not None and self.main_view.get_view_pos() == ViewPos.MAIN

        top_hights = []
        top_set = False # Latch to see if view is on top
        if plot_top:
        # Find hight of top views

            for v in self.top_views:
                if not v.get_main():
                    
                    v.set_on_top(not top_set)
                    # Set top view latch
                    if not top_set:
                        top_set = True

                    # Update view title to match main view 
                    v.set_group_title(self.main_view.get_group_title())
                    top_hights += v.get_desired_hight()
        if self.main_view is not None: self.main_view.set_on_top(not top_set)
        top_hight = sum(top_hights)
        

        # Adjust width if keys will be plotted.
        full_view_list = [view for view in self.left_views if not view.get_main()]+[view for view in self.top_views if not view.get_main()]+[self.main_view]
        has_key = any([view.has_key() for view in full_view_list])
        if has_key:
            _key_w = KEY_WIDTH
            pad_r += _key_w
        else:
            _key_w = 0

        # Find dimensions of main view 
        desired_main_width = sum(self.main_view.get_desired_width())
        available_main_width = size[0] - (left_width + pad_l + pad_r)
        main_w = min(available_main_width, desired_main_width)
        main_h = min(size[1] - (top_hight + pad_t + pad_b), sum(self.main_view.get_desired_hight()))

        # adjust right padding if needed
        if available_main_width > desired_main_width:
            pad_r += (available_main_width - desired_main_width)

        # Get ratios and total length/hight
        w, w_ratios = length_and_ratios([pad_l]+left_widths+[main_w, pad_r])
        h, h_ratios = length_and_ratios([pad_t]+top_hights+[main_h, pad_b])

        # Scale figure padding
        fig.subplots_adjust(left=pad_l/w, right=1-(pad_r-_key_w)/w, top=1-pad_t/h, bottom=pad_b/h)
        #fig.subplots_adjust(left=pad_l/w, right=1-(pad_r)/w, top=1-pad_t/h, bottom=pad_b/h)
       
        # Make the main plot
        self.main_view.make_plots([ax],(main_w, main_h))    

        # Make a divider to locate and points for main axes
        divider = make_axes_locatable(ax)

        plot_i = 0
        _axs:list[Axes] = []
        for view in reversed([view for view in self.left_views if not view.get_main()]):
            _axes:list[Axes] = []
            _x_size = 0
            for _ in range(view.get_plot_count()):

                prop_size = left_widths[-(1+plot_i)]/main_w # Add 1 to index form the back

                _ax = divider.append_axes('left',size=f"{prop_size*100}%",pad=0, sharey = ax)
                _axes.append(_ax) 
                _axs.append(_ax)
                _x_size += left_widths[-(1+plot_i)]
                plot_i += 1
                _axes.reverse()
            view.make_plots(_axes, size=(_x_size, main_h))


        if plot_top:
            plot_i = 0
            for view in reversed([view for view in self.top_views if not view.get_main()]):
                _axes:list[Axes] = []
                _y_size = 0
                for _ in range(view.get_plot_count()):
                    prop_size =  top_hights[-(1+plot_i)]/main_h
                    _axes.append(divider.append_axes('top',size=f"{prop_size*100}%",pad=0, sharex=ax))
                    _y_size += top_hights[-(1+plot_i)]
                    plot_i += 1
                    _axes.reverse()
                view.make_plots(_axes, size=(main_w, _y_size))

        # Plot key on key axis
        if has_key:

            # Make key axs
            rel_w = _key_w/main_w
            key_ax:Axes = divider.append_axes('right', size=f"{rel_w*100}%", pad=0)
            key_ax.axis('off')
            key_views = [view for view in full_view_list if view.has_key()]
            key_sizes = [view.get_key_rows() * KEY_HEIGHT for view in key_views]
            key_h = sum(key_sizes) + (len(key_sizes)-1)*KEY_PAD
            x_spacing = KEY_SIDE_PAD/_key_w
            

            for _i, view in enumerate(key_views):
                rel_h = (view.get_key_rows() * KEY_HEIGHT)/main_h
                ax = key_ax.inset_axes([x_spacing,1-sum(key_sizes[:(_i+1)])/main_h,1-x_spacing,rel_h])
                # Make new axes for key 
                rel_h = (view.get_key_rows() * KEY_HEIGHT)/main_h
                view.make_key(key_ax=ax, size=(rel_w, rel_h))



        # Check if main view needs scroll bars
        x_scroll_box = None
        y_scroll_box = None
        x_scroll = self.main_view.should_add_x_scroll()
        if x_scroll:
            scroll_h =self.SCROLLBAR_BREADTH/h
            scroll_w = w_ratios[-2]
            top = h_ratios[-1]
            left = 1-sum(w_ratios[-2:])
            x_scroll_box = Box(left, top, scroll_w, scroll_h)

        y_scroll = self.main_view.should_add_y_scroll()
        if y_scroll:
            # Construct the bounding box for y scroll view to be 
            scroll_w = self.SCROLLBAR_BREADTH/w
            scroll_h = h_ratios[-2]
            top = sum(h_ratios[-2:])
            left = 1-w_ratios[-1]
            y_scroll_box = Box(left, top, scroll_w, scroll_h)
            
        return w,h, x_scroll_box, y_scroll_box


def get_view_sets(view_infos:ViewInfo_base)->list[ViewSetManager]:
    """Iterate through a list of view infos and return a list of view set managers for those views"""
    view_sets = []
    live_set = ViewSetManager()
    for info in view_infos:
        # Try to link a view to the live set
        if not live_set.link(info):
            # Link failed, append the live set an make a new one for this info
            view_sets.append(live_set)
            live_set = ViewSetManager(info)
    # Link the final set 
    view_sets.append(live_set)

    return view_sets

def length_and_ratios(requested_lengths:list[int])->tuple[int,NDArray]:
    """Task a list of lengths and return the total length an ratios between lengths."""
    full_length = sum(requested_lengths)
    if full_length <= 0: return 0, np.array([])
    weights = np.array(requested_lengths)/full_length
    return full_length, weights
   
