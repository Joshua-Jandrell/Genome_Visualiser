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

class ViewInfo_base:
    """
    Base class used to define and plot different views
    """
    def __init__(self) -> None:
        self.plots = []
        self.dataset_info = None

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

        for info in views:
            n_subplots += info.get_plot_count()
            height_ratios += info.get_height_weights()

        gs = GridSpec(n_subplots, 1, height_ratios=height_ratios)

        # Add all subplots
        subplot_index = 0
        ref_x = None
        for info in views:
            assert(isinstance(info,ViewInfo_base))
            ax = info.make_plots(self.fig,gs=gs,start_index=subplot_index, ref_x=ref_x)
            if ref_x is None: ref_x = ax
            subplot_index += info.get_plot_count()
        
        # Remove spacing between plots
        self.fig.subplots_adjust(hspace=0, wspace=0)
        return True


# ========================================================================
# Plotter for zygosity view
class ZygoteView(ViewInfo_base):
    def __init__(self) -> None:
        self.max_weight = 100
        self.colors = colors.ListedColormap(["#00000000","#002164", "g", "y"])
        super().__init__()
        
    def get_height_weights(self) -> list[int]:        #TODO: What are height weights???
        wrapped_data = self.dataset_info.get_data_wrapper()
        return [min(wrapped_data.n_samples,self.max_weight)]
    
    def make_plots(self, fig: Figure, gs: GridSpec, start_index: int, ref_x:Axes|None)->Axes:
        axis = fig.add_subplot(gs[start_index], sharex = ref_x)
        wrapped_data = self.dataset_info.get_data_wrapper()
        p = axis.pcolorfast(np.matrix(wrapped_data.get_zygosity()), cmap=self.colors, vmax=2, vmin=-1)
        self.plots.append(p)
        return axis

class RefView(ViewInfo_base):
    REF_LABEL = "Ref."
    ALT_LABEL = "Alt."
    # Boundaries   #TODO What boundaries???
    VAR_MAX = 4
    VAR_MIN = -1
    # Annotation limits 
    ANNOTATION_MAX = 500
    ALLELE_COLORS = colors.ListedColormap(["#00000000","grey", "#29E838", "#E829D8", "#E89829", "#2979E8"])
    def __init__(self,plot_alt:bool = True, annotated:bool = True) -> None:
        self.plot_alt = plot_alt
        self.annotated = annotated
        self.allele_colors = self.ALLELE_COLORS
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
        ref_ax = fig.add_subplot(gs[start_index], sharex = ref_x)
        self.make_allele_plot(ref_ax, np.matrix(wrapped_data.get_ref()),self.REF_LABEL, wrapped_data.data[dw.REF], wrapped_data)
        if self.plot_alt:
            alt_ax = fig.add_subplot(gs[start_index+1], sharex=ref_ax)
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
        self.min_window = 500     ##am confused
        super().__init__()
        
    def get_pos_counts(self,wrapped_data:DataWrapper) -> list[int]:
        return [min(wrapped_data._pos,self.min_window)]
    
    ######################################################################
    def plot_windowed_variant_count(pos, window_size, title=None):

        #window_size:  Ratio recommened:  (500:100000)
        
        # Make get data
        pos = get_pos()
        
        # setup windows 
        bins = np.arange(pos.min(), pos.max(), window_size)
        
        # plot
        fig, ax = plt.subplots(figsize=(12,5))
        
        print("Count plot!",ax)
        ax.hist(x=pos, bins=bins, edgecolor='black', color = '#A2F49B') #DDCC77 <-sand yellow
        ax.set_mouseover(True)
        ax.set_facecolor('#FEFBE9')
        ax.set_xlabel('Chromosome position (bp)')
        ax.set_ylabel('Variant count, bp$^{-1}$')
        if title:
            ax.set_title(title)

    plt.show()
    ######################################################################
    def make_plots(self, fig: Figure, gs: GridSpec, start_index: int, wrapped_data: DataWrapper, ref_x:Axes|None)->Axes:
        axis = fig.add_subplot(gs[start_index], sharex = ref_x)
        #p = axis.pcolorfast(np.matrix(wrapped_data.get_pos()))
        p = plot_windowed_variant_count()
        self.plots.append(p)
        return axis
    
    # ######################################################################
    # def plot_windowed_variant_count(pos, window_size=500):

    #     window_size=500  #Ratio recommened:  (500:100000)
        
    #     #data = get_pos()
    #     # Make data into dataframe
    #     df = al.vcf_to_dataframe(TEST_FILE)
    #     pos = df['POS'][:]
        
    #     # setup windows 
    #     bins = np.arange(pos.min(), pos.max(), window_size)
        
    #     # plot
    #     fig, ax = plt.subplots(figsize=(12,5))
        
    #     print("Count plot!",ax)
    #     ax.hist(x=pos, bins=bins, edgecolor='black', color = '#A2F49B') #DDCC77 <-sand yellow
    #     ax.set_mouseover(True)
    #     ax.set_facecolor('#FEFBE9')
    #     ax.set_xlabel('Chromosome position (bp)')
    #     ax.set_ylabel('Variant count, bp$^{-1}$')
    #     if title:
    #         ax.set_title(title)

    # plt.show()
    # ######################################################################
    