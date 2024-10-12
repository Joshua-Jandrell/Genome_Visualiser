"""
View that shows the variant type at for each ample at a given position (or grey ) if no mutation occurs
"""
from matplotlib.axes import Axes as Axes
from .variantGridType import VariantGridView, ViewPos, Y_STACK
from ._plot_config_ import ALLELE_COLORS
from VCF.dataWrapper import VcfDataWrapper, vars_to_numbers

class SampleVarView(VariantGridView):
    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.VAR_STAND_IN
        self._priority = 5

    def make_plots(self, axs: list[Axes], size: tuple[int, int]) -> str:

        # Get data
        wrapped_data = self.dataset_info.get_data()
        assert(wrapped_data is not None)

        


        return super().make_plots(axs, size)