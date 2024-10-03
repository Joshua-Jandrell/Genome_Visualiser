import sys
import numpy as np
import matplotlib as mpl
from matplotlib.axes import Axes as Axes
from .variantGridType import VariantGridView, DataWrapper, ViewPos, Y_STACK

class MutationBarView(VariantGridView):
    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.LEFT_STAND_IN

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
        if self._is_main:
            if self.stack_mode == Y_STACK:
                print("yyyy")
            else:
                # Plot cases 
                ax.barh(_y_pts, homo_z[1])
                ax.barh(_y_pts, hetro_z[1], left=homo_z[1])
                ax.grid()
                if dw.get_n_ctrls() > 0:
                    ax.barh(_y_pts, -homo_z[0], color="yellow")
                    ax.barh(_y_pts, -hetro_z[0], left=-homo_z[0], color="green")

                    ax.set_xlim([-1,1])
                else:
                    ax.set_xlim([0,1])

        else:
            if dw.get_n_ctrls() > 0:
                ax.barh(_y_pts+0.25, homo_z[1], 0.4, align='center', color='yellow')
                ax.barh(_y_pts+0.25, hetro_z[1], 0.4, left=homo_z[1], align='center', color='green')
                ax.barh(_y_pts-0.25, homo_z[0], 0.4, color="yellow")
                ax.barh(_y_pts-0.25, hetro_z[0], 0.4, left=homo_z[0], color="green")
            else:
                ax.barh(_y_pts, homo_z[1])
                ax.barh(_y_pts, hetro_z[1], left=homo_z[1])

                

        self._do_base_config(axs=axs)
        return super().make_plots(axs, size)
    

    # === Override for functionality ===
    def should_add_x_scroll(self) -> bool:
        if self.stack_mode != Y_STACK:
            return False
        return super().should_add_x_scroll()
