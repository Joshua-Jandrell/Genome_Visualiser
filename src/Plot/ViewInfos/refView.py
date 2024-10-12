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

from matplotlib.cm import ScalarMappable
from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches

from .viewInfo import ViewInfo_base, ViewPos
from .variantGridType import GRID_TYPE_KEY, VariantGridView, Y_STACK

from Util.box import Box

from ._plot_config_ import ALLELE_COLORS

class RefView(VariantGridView):
    ALLELE_COLORS = ALLELE_COLORS
    REF_LABEL = "Ref."
    ALT_LABEL = "Alt."
    VAR_MAX = 7
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
        self._pos = ViewPos.VAR

        self._key_rows = 3

        self.mat = None
        

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
        self.mat = self.make_allele_plot(axs[0], data_matrix)
        
        if self.plot_alt:
            data_matrix = np.matrix(wrapped_data.get_alt_int())
            if self.stack_mode == Y_STACK:
                data_matrix = np.transpose(data_matrix)
            self.make_allele_plot(axs[1], data_matrix)
            axs[1].set_xlim([self._lim_offset,data_matrix.shape[1]+self._lim_offset])

        return super().make_plots(axs, size)


    def make_allele_plot(self, axis:Axes, data:np.matrix):
        return axis.imshow(data,cmap=self.allele_colors, vmin=self.VAR_MIN, vmax=self.VAR_MAX)
                    

    
    def make_key(self,key_ax:Axes, size:tuple[int,int]):

        _a = mpatches.Patch(color=self.ALLELE_COLORS[2], label='A')
        _c = mpatches.Patch(color=self.ALLELE_COLORS[3], label='C')
        _g = mpatches.Patch(color=self.ALLELE_COLORS[4], label='G')
        _t = mpatches.Patch(color=self.ALLELE_COLORS[5], label='T')
        _other = mpatches.Patch(color=self.ALLELE_COLORS[1], label='Other')
        _in = mpatches.Patch(color=self.ALLELE_COLORS[6], label='Insertion')
        _del = mpatches.Patch(color=self.ALLELE_COLORS[8], label='Deletion')
        _none = mpatches.Patch(color=self.ALLELE_COLORS[0], label='None')
        key_ax.legend(handles=[_a,_c,_g,_t,_other,_in,_del,_none],ncol=2)
        key_ax.axis('off')

    def get_plot_names(self) -> list[str]:
        return ['Ref.', 'Alt.']