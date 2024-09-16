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
from Util.box import Box

# For scroll view 
from Plot.scrollWidget import ScrollWidget, ScrollManager

GRID_TYPE_KEY = "Var-Grid"
MIN_BLOCKS_PER_COL = 20
"""The Minimum number of blocks allowed per column.\n
If the number of blocks is smaller than this then a larger block size is used.
"""
class GridParams():
    """
    Simple static class that contains genal grid-based parameters.
    """


class VariantGridView(ViewInfo_base):
    def __init__(self) -> None:
        super().__init__()

        self.ideal_block_size = 10
        self.active_axis:Axes|None = None
        self._view_type = GRID_TYPE_KEY

        # Scroll properties
        self._blocks_per_window_x = 30
        """The number of blocks shown on the x axis."""

        # Key formats
        self.key_row_hight = 0.07
        self.key_column_width = 0.6

    def _do_base_config(self,axs:list[Axes]):
        """
        Simple method to re-used common configuration settings.
        """
        if self.is_fist_in_set():
            # Set axis title
            axs[0].set_title("Genotype Variant-Position Grid")
        

    def fit_to_size(self,size:tuple[int,int]):
        if not isinstance(self.active_axis, Axes): return 
        # Find x limit based on block size:
        x_lim = int(np.round(size[0]/self.ideal_block_size))
        self.active_axis.set_xlim(0,x_lim)
        self._blocks_per_window_x = x_lim

        self.update_event.invoke(self)

    def get_set_views(self) -> list:
        views = super().get_set_views()
        if self.is_fist_in_set():
            scroll_view = VariantGridScrollView()
            scroll_view.set_target_view(self)
            views += [scroll_view]
        return views

    # Scroll configuration 
    def should_add_x_scroll(self) -> bool:
        # Should scroll if this is the first view in the set
        return self.pos_in_set == 0
    
    def get_x_scroll_params(self) -> tuple[float, float, float]:
        wrapped_data = self.dataset_info.get_data_wrapper()
        return 0, wrapped_data.n_variants, self._get_scroll_window()
    
    def scroll_x(self, x_pos: float):
        if not self.should_add_x_scroll() or not isinstance(self.active_axis, Axes): return
        self.active_axis.set_xlim(xmin=x_pos, xmax=x_pos+self._get_scroll_window())

    def _get_scroll_window(self)->float:
        return self._blocks_per_window_x
    
# ============== Special views ===================================================

class VariantGridScrollView(ViewInfo_base):
    """Special view type used to allow the user to scroll on the variant grid system."""
    def __init__(self) -> None:
        super().__init__()

        self.scroll_size = 60

    def set_target_view(self,view:VariantGridView):
        self.target_view = view

    def get_desired_size(self) -> list[int]:
        return [self.scroll_size]
    
    def make_plots(self, axs: list[Axes], size: tuple[int, int], plot_box: Box) -> str:
        ScrollManager.make_scroll(view=self.target_view, scroll_box=plot_box)
        self.target_view = None
        axs[0].set_visible(False)
        return super().make_plots(axs, size, plot_box)
        