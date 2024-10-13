import sys
import numpy as np
import matplotlib as mpl
from matplotlib.axes import Axes as Axes
import matplotlib.patches as mpatches
from .variantGridType import VariantGridView, DataWrapper, ViewPos, Y_STACK

from ._plot_config_ import CASE_COLORS, CTRL_COLORS

class MutationBarView(VariantGridView):
    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.VAR_STAND_IN
        self._priority = 100
        self._group_title = "Zygosity Frequency"

    def _get_samples_size(self) -> list[int]:
        if self._is_main:
            # View requests to be as large as possible
            return [sys.maxsize]
        else:
            return [self.ideal_block_size *2]

    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:
        dw = self.get_data().get_data()
        assert(dw is not None)
        ax = axs[0]

        hetro_z = dw.get_heterozygous_probability(split=True, format="fraction")
        homo_z = dw.get_homozygous_probability(split=True, format="fraction")
        _y_pts = np.arange(dw.get_n_variants())
        
        case_i = 1
        ctrl_i = 0
        homo_i = 4
        hetro_i = 3
        if self._is_main:
            if self.stack_mode == Y_STACK:
                # Plot cases 
                ax.bar(_y_pts, homo_z[1], color=CASE_COLORS[homo_i])
                ax.bar(_y_pts, hetro_z[case_i], bottom=homo_z[case_i], color=CASE_COLORS[hetro_i])
                #ax.grid()
                if dw.get_n_ctrls() > 0:
                    ax.bar(_y_pts, -homo_z[ctrl_i], color=CTRL_COLORS[homo_i])
                    ax.bar(_y_pts, -hetro_z[ctrl_i], bottom=-homo_z[ctrl_i], color=CTRL_COLORS[hetro_i])
                    ax.hlines([0],xmin=_y_pts[0]-1,xmax=_y_pts[-1]+1, colors=['black'])

                    ax.set_ylim([-1,1])
                else:
                    ax.set_ylim([0,1])
            else:
                # Plot cases 
                ax.barh(_y_pts, homo_z[1], color=CASE_COLORS[homo_i])
                ax.barh(_y_pts, hetro_z[case_i], left=homo_z[case_i], color=CASE_COLORS[hetro_i])
                #ax.grid()
                if dw.get_n_ctrls() > 0:
                    ax.barh(_y_pts, -homo_z[ctrl_i], color=CTRL_COLORS[homo_i])
                    ax.barh(_y_pts, -hetro_z[ctrl_i], left=-homo_z[ctrl_i], color=CTRL_COLORS[hetro_i])

                    ax.set_xlim([-1,1])
                else:
                    ax.set_xlim([0,1])

        else:
            if self.stack_mode == Y_STACK:
                if dw.get_n_ctrls() > 0:
                    ax.bar(_y_pts+0.25, homo_z[case_i], 0.4, align='center', color=CASE_COLORS[homo_i])
                    ax.bar(_y_pts+0.25, hetro_z[case_i], 0.4, bottom=homo_z[case_i], align='center', color=CASE_COLORS[hetro_i])
                    ax.bar(_y_pts-0.25, homo_z[ctrl_i], 0.4, color=CTRL_COLORS[homo_i])
                    ax.bar(_y_pts-0.25, hetro_z[ctrl_i], 0.4, bottom=homo_z[ctrl_i], color=CTRL_COLORS[hetro_i])
                else:
                    ax.bar(_y_pts, homo_z[case_i], color=CASE_COLORS[homo_i])
                    ax.bar(_y_pts, hetro_z[case_i], bottom=homo_z[case_i], color=CASE_COLORS[hetro_i])
            else:
                if dw.get_n_ctrls() > 0:
                    ax.barh(_y_pts+0.25, homo_z[case_i], 0.4, align='center', color=CASE_COLORS[homo_i])
                    ax.barh(_y_pts+0.25, hetro_z[case_i], 0.4, left=homo_z[case_i], align='center', color=CASE_COLORS[hetro_i])
                    ax.barh(_y_pts-0.25, homo_z[ctrl_i], 0.4, color=CTRL_COLORS[homo_i])
                    ax.barh(_y_pts-0.25, hetro_z[ctrl_i], 0.4, left=homo_z[ctrl_i], color=CTRL_COLORS[hetro_i])
                else:
                    ax.barh(_y_pts, homo_z[case_i], color=CASE_COLORS[homo_i])
                    ax.barh(_y_pts, hetro_z[case_i], left=homo_z[case_i], color=CASE_COLORS[hetro_i])

                

        self._do_base_config(axs=axs)
        return super().make_plots(axs, size)
    
    def has_key(self) -> bool:
        return self.get_main()
    
    def make_key(self,key_ax:Axes, size:tuple[int,int])->Axes:

        homor = mpatches.Patch(color=CASE_COLORS[2], label='Homozygous Ref.')
        hetro = mpatches.Patch(color=CASE_COLORS[3], label='Heterozygous')
        homoa = mpatches.Patch(color=CASE_COLORS[4], label='Homozygous Alt')
        key_ax.legend(handles=[homor, hetro, homoa])
        key_ax.axis('off')
    

    # === Override for functionality ===
    def should_add_x_scroll(self) -> bool:
        if self.stack_mode != Y_STACK:
            return False
        return super().should_add_x_scroll()
    
    def should_add_y_scroll(self) -> bool:
        if self.stack_mode == Y_STACK:
            return False
        return super().should_add_y_scroll()
    
    def get_plot_names(self) -> list[str]:
        if self._is_main:
            return ["Zygosity Proportion"]
        else:
            return ["Zygo-\nProp."]
