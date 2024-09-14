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
GRID_TYPE_KEY = "Var-Grid"
MIN_BLOCKS_PER_COL = 20
"""The Minimum number of blocks allowed per column.\n
If the number of blocks is smaller than this then a larger block size is used.
"""
class GridParams():
    """
    Simple static class that contains genal grid-based parameters.
    """


class VariantGrindType(ViewInfo_base):
    def __init__(self) -> None:
        super().__init__()

        self.ideal_block_size = 7
        self.active_axis = None
        self._view_type = GRID_TYPE_KEY

        # Key formats
        self.key_row_hight = 0.07
        self.key_column_width = 0.6

    def fit_to_size(self,size:tuple[int,int]):
        if not isinstance(self.active_axis, Axes): return 
        # Find x limit based on block size:
        x_lim = int(np.round(size[0]/self.ideal_block_size))
        self.active_axis.set_xlim(0,x_lim)