# This script contains simple constructors for various plot types
import numpy as np
import matplotlib as plt

from VCF.dataWrapper import VcfDataWrapper as DataWrapper
import VCF.dataWrapper as dw
from VCF.filterInfo import DataSetInfo

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
from matplotlib.widgets import Slider, Button, RadioButtons

from Plot.ViewInfos import ViewInfo_base, viewSetManager, get_view_sets, plot_sets
# Class used to store all plot infos and construct the final figure
class ViewPlotter:
    """ 
        Stores all plot information and constructs the final figure
    """
    def __init__(self,figure:Figure, views:list[ViewInfo_base]|None=None) -> None:
        self.fig = figure
        self.plots = []
        self.default_data_wrapper = None

    def plot_figure(self, views:list[ViewInfo_base], size:tuple[int, int]=tuple([0,0]), can_expand:tuple[bool, bool]=tuple([False, False]))->tuple[int, int]:
        """
        Plot a figure on the canvas.\n
        Size is the ideal size of the canvas [width, hight]. If set to 0 it is assumed that the plot can expand.\n
        Can expand determines if the plot can expand or if the given sie is an absolute limit.\n
        Returns the desired figure width and hight, or [0, 0] if figure should not be shown.
        """
        # clear any existing plots on the figure
        self.fig.clear()

        # Filter for only valid views
        views = [view for view in views if isinstance(view,ViewInfo_base) and view.can_plot()]

        if len(views) == 0: return 0, 0

        # group views into a collection of view sets
        view_sets = get_view_sets(views)

        width, hight = plot_sets(view_sets, self.fig, size=size, can_expand = can_expand)
        print(f"h: {hight}")
        return width, hight


# ========================================================================


# ========================================================================
#TODO: Plotter for frequency view
class FrequencyView(ViewInfo_base):
    def __init__(self) -> None:
        self.min_window = 750     ##make function to get window size
        self.plot_density = False
        super().__init__()
    
    def make_plots(self, fig: Figure, gs: GridSpec, start_index: int, ref_x:Axes|None)->Axes:
        gs_pos = 2*start_index # Awkward scaling needed to add key (will be removed later)
        axis = fig.add_subplot(gs[gs_pos+1], sharex = ref_x)
        
        #axis = fig.add_subplot(gs[start_index], sharex = ref_x)
        
        wrapped_data = self.dataset_info.get_data_wrapper()
        pos = wrapped_data.get_pos()
        
        # setup windows   #  Window_size:  Ratio recommened:  (750:100000)
        window_size = self.min_window
        
        bins = np.arange(pos.min(), pos.max(), window_size)
        
        if self.plot_density == False:
            axis.hist(x=pos, bins=bins, edgecolor='black', color = '#A2F49B') #DDCC77 <-sand yellow
            axis.set_mouseover(True)
            axis.set_facecolor('#FEFBE9')
            axis.set_xlabel('Chromosome position (bp)')
            axis.set_ylabel('Variant count, bp$^{-1}$')
            axis.set_title('Mutation Count frequency')

        else:     
        
            # compute variant density in each window
            h, _ = np.histogram(pos, bins=bins)
            y = h / window_size

            axis = fig.add_subplot(gs[gs_pos+1], sharex = ref_x)
            axis.bar(_[:-1], y, width=np.diff(_), align='edge', edgecolor='black', color='#CC6677')
            axis.set_mouseover(True)
            axis.set_facecolor('#E8ECFB')
            axis.set_xlabel('Chromosome position (bp)')
            axis.set_ylabel('Variant density (count per bp $^{-1}$)')
            axis.set_title('Mutation Density frequency')
            
        return axis
    
    def set_should_plot_density(self,plot_density):
        self.plot_density = plot_density

#########################################################################