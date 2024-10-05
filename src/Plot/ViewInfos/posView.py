import numpy as np

from matplotlib.axes import Axes as Axes
from matplotlib import colors
from Util.box import Box
from .variantGridType import VariantGridView, ViewPos, Y_STACK

class VarPosView(VariantGridView):
    """
    A Heatmap-style view to show the position of each variant.
    """
    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.LEFT
    def _get_samples_size(self) -> list[int]:
        return [self.ideal_block_size]

    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:
        self.active_axis = ax = axs[0]
        wrapped_data = self.dataset_info.get_data()
        pos_mat = np.matrix(wrapped_data.get_pos())
        if self.stack_mode != Y_STACK:
            pos_mat = np.transpose(pos_mat)    

        ax.imshow(pos_mat, cmap='plasma')
              
        return super().make_plots(axs, size)
    
    def get_plot_names(self) -> [str]:
        return ['Pos']