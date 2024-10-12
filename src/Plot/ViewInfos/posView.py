from matplotlib.cm import ScalarMappable
import numpy as np

from matplotlib.axes import Axes as Axes
from matplotlib import colors
from Util.box import Box
from .variantGridType import VariantGridView, ViewPos, Y_STACK
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

class VarPosView(VariantGridView):
    """
    A Heatmap-style view to show the position of each variant.
    """
    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.VAR
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
    
    def has_key(self) -> bool:
        return True
    
    def make_key(self, key_ax:Axes, size:tuple[int,int]):

        dw = self.dataset_info.get_data()
        assert(dw is not None)
        min, max = dw.get_file_pos_range()

        fig = key_ax.figure
        norm = colors.Normalize(vmin=min, vmax=max)
        prop_size = 2*self.ideal_block_size/size[1]
        cax = inset_axes(key_ax,width="100%",height=f"{prop_size*100}%")
        cbar = fig.colorbar(ScalarMappable(norm=norm, cmap='plasma'), cax=cax, orientation='horizontal', fraction=prop_size, label="Variant position")
        key_ticks = [min, max]
        cbar.set_ticks(key_ticks)
        #cbar.set_ticklabels([f'{tick}%' for tick in key_ticks])
        key_ax.axis('off')

        return super().make_key(key_ax)
    
    def get_plot_names(self) -> list[str]:
        return ['Pos,']