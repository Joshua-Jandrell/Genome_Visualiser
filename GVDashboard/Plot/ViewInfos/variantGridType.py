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

from .viewInfo import ViewInfo_base, ViewPos, X_STACK, Y_STACK, STACK_MODE
from Util.box import Box

# For scroll view 
from Plot.scrollWidget import ScrollWidget, ScrollManager
GRID_TYPE_KEY = "Var-Grid"

class VariantGridView(ViewInfo_base):
    def __init__(self) -> None:
        super().__init__()

        self.stack_mode = STACK_MODE

        self.ideal_block_size = 20
        self.active_axis:Axes|None = None
        self._view_type = GRID_TYPE_KEY

        # Scroll properties
        self._blocks_per_window_x = 30
        """The number of blocks shown on the x axis."""

        # Key formats
        self.key_row_hight = 0.07
        self.key_column_width = 0.6

        self._lim_offset=-0.5

    def _do_base_config(self,axs:list[Axes]):
        """
        Simple method to re-used common configuration settings.
        """
        for _ax in axs:
            _ax.yaxis.set_tick_params(labelleft=False, left=False)

        if self.is_fist_in_set() and self._pos in [ViewPos.LEFT, ViewPos.LEFT_STAND_IN]:
            # Set axis title
            axs[0].set_ylabel("Variant Position", ha='left')
            self.make_y_labels(axs[0],)


    def make_y_labels(self, ax:Axes):
        ax.yaxis.set_tick_params(labelleft=True)
        dw = self.dataset_info.get_data()
        assert(dw is not None)
        y_labels = dw.get_pos()
        ax.set_yticks(ticks=range(len(y_labels)), labels=y_labels)

    def get_desired_hight(self) -> list[int]:
        if self.stack_mode == Y_STACK: return self._get_samples_size()
        else: return self._get_variants_size()

    def get_desired_width(self) -> list[int]:
        if self.stack_mode != Y_STACK: return self._get_samples_size()
        else: return self._get_variants_size()
    
    
    def _get_samples_size(self)-> list[int]:
        wrapped_data = self.dataset_info.get_data()
        return [wrapped_data.get_n_samples() * self.ideal_block_size]
    
    def _get_variants_size(self)-> list[int]:
        wrapped_data = self.dataset_info.get_data()
        return [wrapped_data.get_n_variants() * self.ideal_block_size]

    def fit_to_size(self, size:tuple[int,int]):
        ax = self.active_axis
        if not isinstance(self.active_axis, Axes): return 
        # Find x limit based on block size:
        if self._pos in [ViewPos.TOP, ViewPos.MAIN]:
            x_lim = float(size[0])/float(self.ideal_block_size)
            self._blocks_per_window_x = x_lim
            ax.set_xlim(self._lim_offset,x_lim+self._lim_offset)
        if self._pos in [ViewPos.LEFT, ViewPos.MAIN]:
            y_lim = float(size[1])/float(self.ideal_block_size)
            self._blocks_per_window_y = y_lim 
            print(f"y_lim {y_lim} with hight {size[1]}")
            ax.set_ylim(self._lim_offset,y_lim+self._lim_offset)


        self.update_event.invoke(self)

    # Scroll configuration 
    def should_add_x_scroll(self) -> bool:
        # Should scroll if this is the first view in the set
        return self.order_in_set == 0
    
    def get_x_scroll_params(self) -> tuple[float, float, float]:
        wrapped_data = self.dataset_info.get_data()
        return 0, wrapped_data.get_n_variants(), self._get_scroll_window()
    
    def scroll_x(self, x_pos: float):
        if not self.should_add_x_scroll() or not isinstance(self.active_axis, Axes): return
        self.active_axis.set_xlim(xmin=x_pos, xmax=x_pos+self._get_scroll_window())

    def should_add_y_scroll(self) -> bool:
        return True
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

    def get_desired_hight(self) -> list[int]:
        return [self.scroll_size]
    
    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:
        #ScrollManager.make_scroll(view=self.target_view, scroll_box=plot_box)
        self.target_view = None
        axs[0].set_visible(False)
        return super().make_plots(axs, size)
        