import numpy as np
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from .variantGridType import VariantGridView, ViewInfo_base, ViewPos, GRID_TYPE_KEY
import matplotlib.patches as mpatches

from ._plot_config_ import CASE_COLORS, CTRL_COLORS

class CaseCtrlView(VariantGridView):
    """
    View used to indicate if an individual is a case or a control sample.
    """
    CASE_CTRL_COLORS = [CASE_COLORS[0], CTRL_COLORS[0]]
    def __init__(self) -> None:
        super().__init__()

        self._pos = ViewPos.TOP
        self._colors = colors.ListedColormap(self.CASE_CTRL_COLORS)

    def _get_variants_size(self) -> list[int]:

        return [self.ideal_block_size]
    
    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:
        dw = self.dataset_info.get_data()
        assert(dw is not None)
        ax:Axes = axs[0]
        _data = np.matrix(dw.get_ctrls()*1)
        ax.imshow(_data, cmap=self._colors, vmin=0, vmax=1)
        return super().make_plots(axs, size)
    
    def get_plot_names(self) -> list[str]:
        return ["Control samples & Case samples"]
    
    def has_key(self) -> bool:
        return True
    
    def make_key(self,key_ax:Axes, size:tuple[int,int])->Axes:
        _case = mpatches.Patch(color=self.CASE_CTRL_COLORS[0], label='Ctrl.')
        _ctrl = mpatches.Patch(color=self.CASE_CTRL_COLORS[1], label='Case')
        key_ax.legend(handles=[_ctrl, _case]
        )
        key_ax.axis('off')