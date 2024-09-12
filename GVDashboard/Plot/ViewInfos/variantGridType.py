"""
Variant grid type views are views with samples on the first axis and variants on the second.\n
These view types are compatible with one another and can be set to share axes for each variant.\n
TODO: The views will need to be able to change orientation and axis sharing.
"""
import numpy as np
import matplotlib as plt

from VCF.dataWrapper import VcfDataWrapper as DataWrapper
import VCF.dataWrapper as dw

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec

from .viewInfo import ViewInfo_base
GRID_TYPE_KEY = "Var-Grid"
# Plotter for zygosity view
class ZygoteView(ViewInfo_base):
    MUTATION_COLORS = ["#00000000","#002164", "g", "y"]
    def __init__(self) -> None:
        super().__init__()
        self.max_weight = 100
        self.min_block_size = 10 # the smallest blocksize acceptable
        self.ideal_block_size = 10
        self.max_block_size = 100 # The largest block size acceptable 
        self.ideal_hight = 8
        self.colors = colors.ListedColormap(self.MUTATION_COLORS)
        self.min_block_size = 0.25

        self.type_key = GRID_TYPE_KEY
        self._has_key = True
    
    def get_desired_size(self) -> list[int]:
        wrapped_data = self.dataset_info.get_data_wrapper()
        return [self.ideal_block_size * wrapped_data.n_samples]
        
    def get_height_weights(self) -> list[int]:
        wrapped_data = self.dataset_info.get_data_wrapper()
        return [min(wrapped_data.n_samples,self.max_weight)]
    
    def make_plots(self,axs:list[Axes],size:tuple[int,int],key_ax:Axes|None = None)->str:
        #axis =fig.add_axes([0.1,0.1,0.9,0.9])
        axis = axs[0]
        #key_axis = fig.add_subplot(gs[gs_pos], sharex = ref_x)
        wrapped_data = self.dataset_info.get_data_wrapper()
        p = axis.pcolorfast(np.matrix(wrapped_data.get_zygosity()), cmap=self.colors, vmax=2, vmin=-1)
        axis.set_xlim(0,20)
        if key_ax is not None:
            self.make_key(key_ax)

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