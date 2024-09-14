"""
Variant grid type views are views with samples on the first axis and variants on the second.\n
These view types are compatible with one another and can be set to share axes for each variant.\n
TODO: The views will need to be able to change orientation and axis sharing.
"""
from typing import Literal
import numpy as np
import matplotlib as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from VCF.dataWrapper import VcfDataWrapper as DataWrapper
import VCF.dataWrapper as dw

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec

from .viewInfo import ViewInfo_base
from .variantGridType import GRID_TYPE_KEY, GridParams, VariantGrindType


class RefView(VariantGrindType):
    REF_LABEL = "Ref."
    ALT_LABEL = "Alt."
    # Boundaries   #TODO What boundaries???
    VAR_MAX = 4
    VAR_MIN = -1
    # Annotation limits 
    ANNOTATION_MAX = 500
    ALLELE_COLORS = ["#00000000","grey", "#29E838", "#E829D8", "#E89829", "#2979E8"]

    def __init__(self,plot_alt:bool = True, annotated:bool = True) -> None:
        super().__init__()
        self.plot_alt = plot_alt
        self.annotated = annotated
        self.allele_colors = colors.ListedColormap(self.ALLELE_COLORS)

        self._has_key = True
        self._view_type = GRID_TYPE_KEY
    def get_desired_size(self) -> list[int]:
        l = [self.ideal_block_size]
        if self.plot_alt:
            wrapped_data = self.dataset_info.get_data_wrapper()
            l += [wrapped_data.get_alt().shape[0] * self.ideal_block_size]
        return l

    def get_height_weights(self) -> list[int]:
        weight = [1]
        if self.plot_alt:
            wrapped_data = self.dataset_info.get_data_wrapper()
            weight += [wrapped_data.get_alt().shape[0]]
        return weight
    def get_plot_count(self) -> int:
        if self.plot_alt: return 2
        else: return 1
    def make_plots(self,axs:list[Axes],size:tuple[int,int], label:Literal["top", "bottom", "left", "right"]="none")->Axes:
        self.active_axis = axs[0]
        wrapped_data = self.dataset_info.get_data_wrapper()
        self.make_allele_plot(axs[0], np.matrix(wrapped_data.get_ref()),self.REF_LABEL, wrapped_data.data[dw.REF], wrapped_data)
        if self.plot_alt:
            self.make_allele_plot(axs[1], np.matrix(wrapped_data.get_alt()),self.ALT_LABEL,wrapped_data.data[dw.ALT], wrapped_data)

        if self.pos_in_set == 0:
            self.fit_to_size(size=size)

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
    
    def make_key(self,key_ax:Axes, size:tuple[int,int])->Axes:
            key_txt = [["   ","A"],
                ["   ", "C"],
                ["   ", "G"],
                ["   ", "T"],
                ["   ", "Multiple"],
                ["   ", "Deletion"],
                ["   ", "None"]]
            key_colors = [[self.ALLELE_COLORS[2], "#00000000"],
                          [self.ALLELE_COLORS[3], "#00000000"],
                          [self.ALLELE_COLORS[4], "#00000000"],
                          [self.ALLELE_COLORS[5], "#00000000"],
                          [self.ALLELE_COLORS[1], "#00000000"],
                          [self.ALLELE_COLORS[1], "#00000000"],
                          [self.ALLELE_COLORS[0], "#00000000"]]
            tab = key_ax.table(cellText=key_txt,cellColours=key_colors, loc="center", colLoc="center", colWidths=[self.key_row_hight, self.key_column_width])
            #tab.auto_set_font_size([False, False])
            cellDict=tab.get_celld()

            #tab.auto_set_column_width([0, 1])
            key_ax.set_xticklabels([])
            key_ax.set_yticklabels([])
            key_ax.set_xlabel("")
            key_ax.set_ylabel("")
            key_ax.axis('off')