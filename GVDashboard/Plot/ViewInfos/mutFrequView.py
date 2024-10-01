# This script calculates the frequency of a mutation occuring in a specific position
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from Util.box import Box
from .variantGridType import VariantGridView, ViewInfo_base, ViewPos, Y_STACK
    
MUTATION_FREQ_SPECTRUM = ['#81C4E7','#CEFFFF','#C6F7D6', '#A2F49B', '#BBE453', '#D5CE04', '#E7B503'] #, '#F6790B', '#F94902', '#E40515']

class MutFreqView(VariantGridView):
    """
    A Heatmap-style view to show the probability of a mutation occuring at each position.
    """

    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.LEFT
    
    def _get_samples_size(self) -> list[int]:
        return [self.ideal_block_size]

    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:
        self.active_axis = ax = axs[0]
        wrapped_data = self.dataset_info.get_data()
        all_prob_mat = np.matrix(wrapped_data.get_mutation_probability())

        if self.stack_mode != Y_STACK:
            all_prob_mat = np.transpose(all_prob_mat)       

        ax.imshow(all_prob_mat, cmap=colors.ListedColormap(MUTATION_FREQ_SPECTRUM), vmin=0, vmax=100)
        
        self._do_base_config(axs)
        return super().make_plots(axs, size) 
    
############################### KEY FUNCTS  (literally) ###########
    # # def has_key(self)->bool:
    # #     return True
    
    # # def make_key(self,key_ax:Axes, size:tuple[int,int])->Axes:
           
    # #     fig_mut_freq_key, ax = plt.subplots(layout='constrained')
    # #     # Create a continuous colormap
    # #     cmap = colors.LinearSegmentedColormap.from_list('custom_cmap', MUTATION_FREQ_SPECTRUM)
    # #     # Normalize the color scale
    # #     norm = colors.Normalize(vmin=0, vmax=100)
    # #     # Create the colorbar
    # #     cbar = fig_mut_freq_key.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='vertical', label="Zygosity Frequency key")
    # #     # Set custom ticks and labels
    # #     key_ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # #     cbar.set_ticks(key_ticks)
    # #     cbar.set_ticklabels([f'{tick}%' for tick in key_ticks])
    # #     key_ax = ax
        
    # #     ##### Transfer colorbar to a linspace
    # #     # fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),cax=ax, orientation='vertical', label="Zygosity Frequency key")
