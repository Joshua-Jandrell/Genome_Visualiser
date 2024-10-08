# This script calculates the frequency of a mutation occuring in a specific position
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.cm import ScalarMappable
from Util.box import Box
from .variantGridType import VariantGridView, ViewInfo_base, ViewPos, Y_STACK
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    
MUTATION_FREQ_SPECTRUM = ['#81C4E7','#CEFFFF','#C6F7D6', '#A2F49B', '#BBE453', '#D5CE04', '#E7B503', '#F19903', '#E94C1F', '#D11807'] #, '#F6790B', '#F94902']

class MutFreqView(VariantGridView):
    """
    A Heatmap-style view to show the probability of a mutation occuring at each position.
    """

    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.LEFT
        self.img = None
        self._key_rows = 2
    
    def _get_samples_size(self) -> list[int]:
        return [2*self.ideal_block_size]

    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:
        self.active_axis = ax = axs[0]
        wrapped_data = self.dataset_info.get_data()
        all_prob_mat = np.matrix(wrapped_data.get_mutation_probability())

        if self.stack_mode != Y_STACK:
            all_prob_mat = np.transpose(all_prob_mat)      

        _cmap = colors.ListedColormap(MUTATION_FREQ_SPECTRUM)
        ax.imshow(all_prob_mat, cmap=_cmap, vmin=0, vmax=1, aspect='auto')
        # ax.barh(np.arange(len(wrapped_data.get_mutation_probability())),
        #         wrapped_data.get_mutation_probability(),
        #         color=_cmap(wrapped_data.get_mutation_probability()))
        
        self._do_base_config(axs)
        return super().make_plots(axs, size) 
    
############################### KEY FUNCTS  (literally) ###########
    def has_key(self)->bool:
        return True
    
    def make_key(self,key_ax:Axes, size:tuple[int,int]):
        fig = key_ax.figure
        cmap = colors.LinearSegmentedColormap.from_list('custom_cmap', MUTATION_FREQ_SPECTRUM)
        norm = colors.Normalize(vmin=0, vmax=100)
        prop_size = size[1]
        cax = inset_axes(key_ax,width="90%",height=f"{prop_size*100}%")
        cbar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation='horizontal', label="Mutation Frequency")
        key_ticks = [0, 50, 100]
        cbar.set_ticks(key_ticks)
        cbar.set_ticklabels([f'{tick}%' for tick in key_ticks])
        key_ax.axis('off')

    def get_plot_names(self) -> list[str]:
            return ['Mut-\n Freq.']