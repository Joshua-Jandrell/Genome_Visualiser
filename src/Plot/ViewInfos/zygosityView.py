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
from .variantGridType import GRID_TYPE_KEY, VariantGridView, Y_STACK, X_STACK
from Util.box import Box

from ._plot_config_ import CASE_COLORS, CTRL_COLORS

# Plotter for zygosity view
class ZygoteView(VariantGridView):
    MUTATION_COLORS = CASE_COLORS[1:] + CTRL_COLORS[1:]
    def __init__(self) -> None:
        super().__init__()
        self.max_weight = 100
        self.min_block_size = 10 # the smallest blocksize acceptable
        self.max_block_size = 100 # The largest block size acceptable 
        self.colors = colors.ListedColormap(self.MUTATION_COLORS)
        self.min_block_size = 0.25

        self._can_compress = True

        self._has_key = True

    # def get_samples_size(self) -> list[int]:
    #     wrapped_data = self.dataset_info.get_data_wrapper()
    #     return [self.ideal_block_size * wrapped_data.get_n_samples()]


    def get_height_weights(self) -> list[int]:
        wrapped_data = self.dataset_info.get_data()
        return [min(wrapped_data.get_n_samples(),self.max_weight)]
    
    def make_plots(self,axs:list[Axes],size:tuple[int,int])->str:
        axis = axs[0]
        self.active_axis = axis
        # Get wrapped data and make the plot
        wrapped_data = self.dataset_info.get_data()

        ctrls, cases = wrapped_data.get_zygosity(split=True)
        zygos_matrix = np.concat((ctrls,cases),axis=1)

        if self.stack_mode == Y_STACK:
            zygos_matrix = np.transpose(zygos_matrix)

        axis.imshow(zygos_matrix, cmap=self.colors, vmax=6, vmin=-1)

        self._do_base_config(axs)      
        self.fit_to_size(size=size) # Not fitting to size must be done AFTER base config


        return ""


    def has_key(self)->bool:
        return True
    
    def make_key(self,key_ax:Axes, size:tuple[int,int])->Axes:
                      
            key_txt = [["   ","No Mutation (ref)"],
                ["   ", "Heterozygous (alt)"],
                ["   ", "Homozygous (alt)"],
                ["   ", "No Data"]]
            key_colors = [[self.MUTATION_COLORS[1], "#00000000"],
                          [self.MUTATION_COLORS[2], "#00000000"],
                          [self.MUTATION_COLORS[3], "#00000000"],
                          [self.MUTATION_COLORS[0], "#00000000"]]
            tab = key_ax.table(cellText=key_txt,cellColours=key_colors, loc="center", colLoc="center", colWidths=[self.key_row_hight, self.key_column_width])
            # tab.auto_set_font_size([False, False])
            # tab.auto_set_column_width([0, 1])
            key_ax.axis('off')

    def get_plot_names(self) -> [str]:
        return ["Zygosity Map"]