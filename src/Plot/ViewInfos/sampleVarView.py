"""
View that shows the variant type at for each ample at a given position (or grey ) if no mutation occurs
"""
import numpy as np
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from .variantGridType import VariantGridView, ViewPos, Y_STACK
from ._plot_config_ import ALLELE_COLORS, NO_DATA
from VCF.dataWrapper import VcfDataWrapper, vars_to_numbers

class SampleVarView(VariantGridView):
    def __init__(self) -> None:
        super().__init__()
        #self._pos = ViewPos.VAR_STAND_IN
        self._priority = 5

        self.cmap = colors.ListedColormap([NO_DATA]+ALLELE_COLORS)

    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:

        # Get data
        dw = self.dataset_info.get_data()
        assert(dw is not None)

        self.active_axis = ax = axs[0]
        ctrl_pos_ints, case_pos_ints  = dw.get_pos_var_ints(split=True)
        mat = np.concat((ctrl_pos_ints,case_pos_ints),axis=1)
        if self.stack_mode == Y_STACK:
            mat = np.transpose(mat)
            # ctrl_pos_ints = np.transpose(ctrl_pos_ints)
            # case_pos_ints = np.transpose(case_pos_ints)
            # axis_n = 2

        ax.imshow(mat, cmap=self.cmap, vmin=-2, vmax=7)

        return super().make_plots(axs, size)