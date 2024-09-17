import numpy as np

from matplotlib.axes import Axes as Axes
from matplotlib import colors
from Util.box import Box
from .variantGridType import VariantGridView, ViewInfo_base

class VarPosView(VariantGridView):
    """
    A Heatmap-style view to show the position of each variant.
    """
    def get_desired_hight(self) -> list[int]:
        return [self.ideal_block_size*3]

    def make_plots(self, axs: list[Axes], size: tuple[int, int], plot_box: Box) -> str:
        self.active_axis = ax = axs[0]
        wrapped_data = self.dataset_info.get_data_wrapper()
        pos_mat = np.matrix(wrapped_data.get_pos())

        ax.pcolorfast(pos_mat, cmap='RdPu')
        #ax.plot(wrapped_data.get_pos())
        #ax.stem(wrapped_data.get_pos())
        #ax.bar(wrapped_data.get_pos())

        return super().make_plots(axs, size, plot_box)