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

def inch_to_cm(inches:float)->float:
    """Converts inches to centimeters"""
    return inches * 2.54
class ViewInfo_base:
    """
    Base class used to define and plot different views
    """
    def __init__(self) -> None:
        self.plots = []
        self.dataset_info = None
        self.link_to_prev = True # Link the 'long' axis of this plot to the plot that came before it.
        self.link_to_next = True # Link the 'long' axis of this plot to the next plot
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
    
    def get_desired_hight(self)->int:
        """
        Returns the the hight, in pixes, that the given plot will ideally occupy.
        """
        return 200
    def make_plots(self,fig:Figure, gs:GridSpec ,start_index:int, ref_x:Axes|None)->tuple[Axes,str]:
        """
        Method used to plot the data on a figure\n
        Returns the axis used for plotting and a log-string containing any errors or notes\n
        NOTE: This function must be overridden, only then can the `ViewInfo_base` class is implemented.
        """
        pass
    def can_plot(self)->bool:
        """Returns true if the view can be plotted."""
        return self.dataset_info is not None and self.dataset_info.get_data_wrapper() is not None


# Class used to store all plot infos and construct the final figure
class ViewPlotter:
    """ 
        Stores all plot information and constructs the final figure
    """
    def __init__(self,figure:Figure, views:list[ViewInfo_base]|None=None) -> None:
        self.fig = figure
        self.plots = []
        self.default_data_wrapper = None

    
    def plot_figure(self, views:list[ViewInfo_base])->bool:
        """Plot a figure on the canvas.\n
        Returns true if a plot should be shown.
        """
        # clear any existing plots on the figure
        self.fig.clear()

        # Determine number of sub_plots and their weights
        height_ratios = []
        n_subplots = 0

        # Filter for only valid views
        views = [view for view in views if isinstance(view,ViewInfo_base) and view.can_plot()]

        if len(views) == 0: return False

        fig_hight = 0
        for info in views:
            
            n_subplots += info.get_plot_count()
            height_ratios += info.get_height_weights()

        # Gridspec width ratios TODO Make this a variable
        w_ratios = [1,5]
        gs = GridSpec(n_subplots, 2, height_ratios=height_ratios, width_ratios=w_ratios)

        # Add all subplots
        subplot_index = 0
        ref_x = None
        for info in views:
            assert(isinstance(info,ViewInfo_base))
            ax = info.make_plots(self.fig,gs=gs,start_index=subplot_index, ref_x=ref_x)
            if ref_x is None: ref_x = ax
            subplot_index += info.get_plot_count()
        
        # Remove spacing between plots
        self.fig.subplots_adjust(hspace=0, wspace=0.2)
        return True


# ========================================================================
# Plotter for zygosity view
class ZygoteView(ViewInfo_base):
    MUTATION_COLORS = ["#00000000","#002164", "g", "y"]
    def __init__(self) -> None:
        self.max_weight = 100
        self.min_block_size = 10 # the smallest blocksize acceptable
        self.max_block_size = 100 # The largest block size acceptable 
        self.colors = colors.ListedColormap(self.MUTATION_COLORS)
        self.min_block_size = 0.25
        super().__init__()
        
    def get_height_weights(self) -> list[int]:
        wrapped_data = self.dataset_info.get_data_wrapper()
        return [min(wrapped_data.n_samples,self.max_weight)]
    
    def make_plots(self, fig: Figure, gs: GridSpec, start_index: int, ref_x:Axes|None)->Axes:
        #axis =fig.add_axes([0.1,0.1,0.9,0.9])
        gs_pos = 2*start_index # Akward scaling needed to add key (will be removed later)
        axis = fig.add_subplot(gs[gs_pos+1], sharex = ref_x)
        key_axis = fig.add_subplot(gs[gs_pos], sharex = ref_x)
        wrapped_data = self.dataset_info.get_data_wrapper()
        p = axis.pcolorfast(np.matrix(wrapped_data.get_zygosity()), cmap=self.colors, vmax=2, vmin=-1)
        axis.set_xlim(0,20)
        axis.set_ylim(0,20)
        self.make_key(key_axis)

        return axis
    
    def make_key(self,key_ax:Axes)->Axes:
            key_txt = [["   ","No Mutation (ref)"],
                ["   ", "Heterozygous (alt)"],
                ["   ", "Homozygous (alt)"],
                ["   ", "No Data"]]
            key_colors = [[self.MUTATION_COLORS[1], "#00000000"],
                          [self.MUTATION_COLORS[2], "#00000000"],
                          [self.MUTATION_COLORS[3], "#00000000"],
                          [self.MUTATION_COLORS[0], "#00000000"]]
            tab = key_ax.table(cellText=key_txt,cellColours=key_colors, loc="center")
            tab.auto_set_font_size([False, False])
            tab.auto_set_column_width([0, 1])
            key_ax.set_xticklabels([])
            key_ax.set_yticklabels([])
            key_ax.set_xlabel("")
            key_ax.set_ylabel("")
            key_ax.axis('off')

class RefView(ViewInfo_base):
    REF_LABEL = "Ref."
    ALT_LABEL = "Alt."
    # Boundaries   #TODO What boundaries???
    VAR_MAX = 4
    VAR_MIN = -1
    # Annotation limits 
    ANNOTATION_MAX = 500
    ALLELE_COLORS = ["#00000000","grey", "#29E838", "#E829D8", "#E89829", "#2979E8"]
    def __init__(self,plot_alt:bool = True, annotated:bool = True) -> None:
        self.plot_alt = plot_alt
        self.annotated = annotated
        self.allele_colors = colors.ListedColormap(self.ALLELE_COLORS)
        super().__init__()
    def get_height_weights(self) -> list[int]:
        weight = [1]
        if self.plot_alt:
            wrapped_data = self.dataset_info.get_data_wrapper()
            weight += [wrapped_data.get_alt().shape[0]]
        return weight
    def get_plot_count(self) -> int:
        if self.plot_alt: return 2
        else: return 1
    def make_plots(self, fig: Figure, gs: GridSpec, start_index: int, ref_x:Axes|None)->Axes:
        wrapped_data = self.dataset_info.get_data_wrapper()
        gs_pos = 2*start_index # Akward scaling needed to add key (will be removed later)
        ref_ax = fig.add_subplot(gs[gs_pos+1], sharex = ref_x)
        #ref_ax = fig.add_subplot(gs[start_index], sharex = ref_x)
        self.make_allele_plot(ref_ax, np.matrix(wrapped_data.get_ref()),self.REF_LABEL, wrapped_data.data[dw.REF], wrapped_data)
        if self.plot_alt:
            alt_ax = fig.add_subplot(gs[start_index+1], sharex=ref_ax)
            alt_ax = fig.add_subplot(gs[gs_pos+3], sharex=ref_ax)
            self.make_allele_plot(alt_ax, np.matrix(wrapped_data.get_alt()),self.ALT_LABEL,wrapped_data.data[dw.ALT], wrapped_data)
        return ref_ax

    def make_allele_plot(self, axis:Axes, data:np.matrix, label:str, data_labels, wrapped_data: DataWrapper):
        # linewidth=1,edgecolors="k"
        axis.pcolorfast(data,cmap=self.allele_colors, vmin=self.VAR_MIN, vmax=self.VAR_MAX)
        # Remove tick labels
        axis.set_xticks([])
        axis.set_yticks([])
        # Label y-axis
        axis.set_ylabel(label, rotation=0, va="center", ha="right")

        # Add annotations
        if self.should_annotate(wrapped_data):
            for y in range(data.shape[0]):
                for x in range(data.shape[1]):
                    axis.annotate(f"{data_labels[x][y]}", 
                                  xy=(x+0.5,y+0.5),
                                  horizontalalignment='center',
                                  verticalalignment='center', 
                                  fontsize=8)
                    
    def should_annotate(self,wrapped_data:DataWrapper)->bool:
        return self.annotated and wrapped_data.get_alt().shape[1] < self.ANNOTATION_MAX


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