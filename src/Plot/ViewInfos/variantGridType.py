"""
Variant grid type views are views with samples on the first axis and variants on the second.\n
These view types are compatible with one another and can be set to share axes for each variant.\n
TODO: The views will need to be able to change orientation and axis sharing.
"""
from typing import Literal
import numpy as np
import matplotlib as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from VCF.filterInfo import DataSetInfo
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

        # Data dimensions
        self._n_samps = 0
        self._n_vars = 0

        # Scroll properties
        self._blocks_per_window_x = 0
        """The number of blocks shown on the x axis."""
        self._curr_x_pos = 0
        """The position of the leftmost view corner."""

        self._blocks_per_window_y  = 0
        """The number of blocks shown on the y axis."""
        self._curr_y_pos = 0
        """The position of the topmost view corner."""

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
            _ax.xaxis.set_tick_params(labeltop=False, labelbottom=False, top=False, bottom=False)

        # Configure y axis labels 
        if self.is_fist_in_set() and self._pos in [ViewPos.LEFT, ViewPos.LEFT_STAND_IN]:
            # Set axis title
            axs[0].set_ylabel("Variant Position", ha='left')
            self.make_y_labels(axs[0],)

        # Configure x labels 
        if self.stack_mode == Y_STACK:
            print("good")


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
        return [self._n_samps * self.ideal_block_size]
    
    def _get_variants_size(self)-> list[int]:
        return [self._n_vars * self.ideal_block_size]

    def fit_to_size(self, size:tuple[int,int]):
        ax = self.active_axis
        if not isinstance(self.active_axis, Axes): return 
        # Find x limit based on block size:
        if self._pos in [ViewPos.TOP, ViewPos.MAIN]:
            x_lim = float(size[0])/float(self.ideal_block_size)
            self._blocks_per_window_x = x_lim
            ax.set_xlim(self._lim_offset,x_lim+self._lim_offset)
        if self._pos in [ViewPos.LEFT, ViewPos.LEFT_STAND_IN, ViewPos.MAIN]:
            self._blocks_per_window_y = float(size[1])/float(self.ideal_block_size)
            self._move_y(0)

        self.update_event.invoke(self)

    def _move_y(self,value:float):
        """Move the view vertically to the given y value."""
        ax = self.active_axis
        self._curr_y_pos = value
        ax.set_ylim(value+self._blocks_per_window_y+self._lim_offset,
                    value+self._lim_offset)
        
    def _move_x(self,value:float):
        """Move the view vertically to the given y value."""
        ax = self.active_axis
        self._curr_x_pos = value
        ax.set_xlim(value+self._lim_offset,
                    value+self._blocks_per_window_x+self._lim_offset)
        
    def set_data(self, dataset_info: DataSetInfo|None):
        print("add update event to dw")
        if dataset_info is not None:
            dw = dataset_info.get_data()
            self._n_vars = dw.get_n_variants()
            self._n_samps = dw.get_n_samples()
        else:
            self._n_vars = 0
            self._n_samps = 0
        return super().set_data(dataset_info)

    # Scroll configuration 

    def get_data_dims(self) -> tuple[int, int]:
        """Returns the size of data (ie number of variants and number of samples)"""
        if STACK_MODE == Y_STACK:
            return self._n_vars, self._n_samps
        else:
            return self._n_samps, self._n_vars
    def _get_data_x(self) -> int:
        """Returns the number of columns of the dataset used."""
        x, _ = self.get_data_dims()
        return x

    def _get_data_y(self) -> int:
        """Returns the number of rows of the data used."""
        _, y = self.get_data_dims()
        return y
           
    def get_x_scroll_params(self) -> tuple[float, float]:
        _x = self._get_data_x()
        return self._curr_x_pos/_x, self._blocks_per_window_x/_x

    
    def scroll_x(self, x_pos: float):
        _x = self._get_data_x()
        x_pt = x_pos * _x
        self._move_x(x_pt)
   
    def get_y_scroll_params(self) -> tuple[float, float]:
        _y = self._get_data_y()

        return self._curr_y_pos/_y, self._blocks_per_window_y/_y

    def scroll_y(self, y_pos: float):
        _y = self._get_data_y()
        y_pt = y_pos * _y
        self._move_y(y_pt)
    
    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:
        self.active_axis = axs[0]
        self.fit_to_size(size)
        return super().make_plots(axs, size)
        