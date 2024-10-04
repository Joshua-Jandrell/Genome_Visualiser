"""
Variant grid type views are views with samples on the first axis and variants on the second.\n
These view types are compatible with one another and can be set to share axes for each variant.\n
TODO: The views will need to be able to change orientation and axis sharing.
"""
from typing import Literal
import numpy as np
import matplotlib as plt

from VCF.dataWrapper import VcfDataWrapper as DataWrapper
import VCF.dataWrapper as dw

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .viewInfo import ViewInfo_base, ViewPos
from .variantGridType import GRID_TYPE_KEY, VariantGridView, Y_STACK

from Util.box import Box

from .__config__ import ALLELE_COLORS

class RefView(VariantGridView):
    ALLELE_COLORS = ALLELE_COLORS
    REF_LABEL = "Ref."
    ALT_LABEL = "Alt."
    VAR_MAX = 4
    VAR_MIN = -1
    # Annotation limits 
    ANNOTATION_MAX = 500
    def __init__(self,plot_alt:bool = True, annotated:bool = True) -> None:
        super().__init__()
        self.plot_alt = plot_alt
        self.annotated = annotated
        self.allele_colors = colors.ListedColormap(ALLELE_COLORS)

        self._has_key = True
        self._view_type = GRID_TYPE_KEY
        self._pos = ViewPos.LEFT

    def _get_samples_size(self) -> list[int]:
        l = [self.ideal_block_size]
        if self.plot_alt:
            wrapped_data = self.dataset_info.get_data()
            l += [wrapped_data.get_alt_int().shape[1] * self.ideal_block_size]
        return l

    def get_height_weights(self) -> list[int]:
        weight = [1]
        if self.plot_alt:
            wrapped_data = self.dataset_info.get_data()
            weight += [wrapped_data.get_alt_int().shape[0]]
        return weight
    def get_plot_count(self) -> int:
        if self.plot_alt: return 2
        else: return 1
    def make_plots(self,axs:list[Axes],size:tuple[int,int])->str:
        self.active_axis = axs[0]
        wrapped_data = self.dataset_info.get_data()
        data_matrix = np.matrix(wrapped_data.get_ref_ints())
        if self.stack_mode != Y_STACK:
            data_matrix = np.transpose(data_matrix)
        self.make_allele_plot(axs[0], data_matrix)
        
        if self.plot_alt:
            data_matrix = np.matrix(wrapped_data.get_alt_int())
            if self.stack_mode == Y_STACK:
                data_matrix = np.transpose(data_matrix)
            self.make_allele_plot(axs[1], data_matrix)
            axs[1].set_xlim([self._lim_offset,data_matrix.shape[1]+self._lim_offset])

        self._do_base_config(axs)

        return super().make_plots(axs, size)


    def make_allele_plot(self, axis:Axes, data:np.matrix):
        axis.imshow(data,cmap=self.allele_colors, vmin=self.VAR_MIN, vmax=self.VAR_MAX)
                    

    
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

            #tab.auto_set_column_width([0, 1])
            key_ax.set_xticklabels([])
            key_ax.set_yticklabels([])
            key_ax.set_xlabel("")
            key_ax.set_ylabel("")
            key_ax.axis('off')