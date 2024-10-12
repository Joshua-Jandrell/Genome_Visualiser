"""
Variant grid type views are views with samples on the first axis and variants on the second.\n
These view types are compatible with one another and can be set to share axes for each variant.\n
TODO: The views will need to be able to change orientation and axis sharing.
"""
from mpl_toolkits.axes_grid1 import make_axes_locatable

from VCF.filterInfo import DataSetInfo, FilterError
from VCF.dataWrapper import VcfDataWrapper as DataWrapper

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib.gridspec import GridSpec as GridSpec

from .viewInfo import ViewInfo_base, ViewPos, X_STACK, Y_STACK, STACK_MODE, pos_is_on_x, pos_is_on_y
from Util.box import Box

import numpy as np

GRID_TYPE_KEY = "Var-Grid"
IS_DYNAMIC = False

class VariantGridView(ViewInfo_base):
    def __init__(self) -> None:
        super().__init__()

        self.stack_mode = STACK_MODE

        self.ideal_block_size = 20
        self.active_axis:Axes|None = None
        self._view_type = GRID_TYPE_KEY
        self._group_title = 'Zygosity Map'

        # Data dimensions
        self._n_samps = 0
        self._n_vars = 0

        # Replot rules
        self._replot_on_vars = True
        self._replot_on_samps = True

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

        # Configure axis labels 
        if self.stack_mode == Y_STACK:
            if self.is_fist_in_set() and pos_is_on_x(self._pos):
            # Set axis title
                axs[0].set_xlabel("Variant Position")
                self.make_var_labels(axs[0])
                axs[0].xaxis.set_label_position('top')
        else:
            if self.is_fist_in_set() and pos_is_on_y(self._pos):
            # Set axis title
                axs[0].set_ylabel("Variant Position", ha='left')
                self.make_var_labels(axs[0])

        if self.is_on_top():
            axs[0].set_title(self.get_group_title())

        # Configure plot labels
        _ax_names = self.get_plot_names()

        if not self._is_main and (self.stack_mode != Y_STACK and self._pos and self._pos in [ViewPos.VAR, ViewPos.VAR_STAND_IN]):
            for _i, _ax in enumerate(axs):
                if len(_ax_names) > _i:
                    _ax.set_xlabel(_ax_names[_i], va='top', rotation=90)
                    _ax.xaxis.set_label_position('top')
            

    def make_sample_labels(self, ax:Axes):
        dw = self.dataset_info.get_data()
        assert(dw is not None)
        
        _labels = dw.get_samples()
        if self.stack_mode != Y_STACK:
            ax.xaxis.set_tick_params(labeltop=True)
            ax.set_xticks(ticks=range(len(_labels)), labels=_labels, rotation=90)
            ax.xaxis.set_tick_params(labelsize=8)
        else:
            ax.yaxis.set_tick_params(labelleft=True)
            ax.set_yticks(ticks=range(len(_labels)), labels=_labels)
            ax.yaxis.set_tick_params(labelsize=8)


    def make_var_labels(self, ax:Axes):
        dw = self.dataset_info.get_data()
        assert(dw is not None)
        _labels = dw.get_pos()
        if self.stack_mode == Y_STACK:
            ax.xaxis.set_tick_params(labeltop=True)
            ax.set_xticks(ticks=range(len(_labels)), labels=_labels, rotation=90)
            ax.xaxis.set_tick_params(labelsize=8)
        else:
            ax.yaxis.set_tick_params(labelleft=True)
            ax.set_yticks(ticks=range(len(_labels)), labels=_labels)
            ax.yaxis.set_tick_params(labelsize=8)

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
        if not isinstance(self.active_axis, Axes): return 
        # Find x limit based on block size:
        if pos_is_on_x(self._pos):
            self._blocks_per_window_x = float(size[0])/float(self.ideal_block_size)
            self._move_x(0)

        if pos_is_on_y(self._pos):
            self._blocks_per_window_y = float(size[1])/float(self.ideal_block_size)
            self._move_y(0)

        self.update_event.invoke(self, 'scale')

    def _move_y(self,value:float):
        """Move the view vertically to the given y value."""
        ax = self.active_axis
        self._curr_y_pos = value
        ax.set_ylim(value+self._blocks_per_window_y+self._lim_offset,
                    value+self._lim_offset)
        
        self.update_event.invoke(self, 'move')
        
    def _move_x(self,value:float):
        """Move the view vertically to the given y value."""
        ax = self.active_axis
        self._curr_x_pos = value
        ax.set_xlim(value+self._lim_offset,
                    value+self._blocks_per_window_x+self._lim_offset)
        
        self.update_event.invoke(self, 'move')
        
    def set_data(self, dataset_info: DataSetInfo|None):
        if dataset_info == self.dataset_info: return

        # unsubscribe from event if required
        if self.dataset_info is not None:
            self.dataset_info.remove_listener(self._on_vargird_dataset_update)

        if dataset_info is not None:
            dw = dataset_info.get_data()
            self._n_vars = dw.get_n_variants()
            self._n_samps = dw.get_n_samples()
            dataset_info.add_listener(self._on_vargird_dataset_update)
        else:
            self._n_vars = 0
            self._n_samps = 0
        return super().set_data(dataset_info)
    
    def _on_vargird_dataset_update(self,dataset:DataSetInfo,update_type):
        if update_type == 'variants' and self._replot_on_vars:
            _n_vars = dataset.get_data().get_n_variants()
            self._n_vars = _n_vars
            self._replot()
        elif update_type == 'samples' and self._replot_on_samps:
            self._n_samps = dataset.get_data().get_n_samples()
            self._replot()

    def _replot(self):
        if not IS_DYNAMIC:
            return
        for ax in self._axs:
            ax.clear()
        if self.can_plot():
            self.make_plots(self._axs, self._plot_size)
        else:
            raise FilterError()
            

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
        self._plot_size = size
        self._do_base_config(axs)
        self.active_axis = axs[0]
        self.fit_to_size(size)
        return super().make_plots(axs, size)
    
    def can_plot(self) -> bool:
        if self._n_samps == 0 or self._n_vars == 0:
            return False
        return super().can_plot()

        