import sys
import numpy as np
import matplotlib as mpl
from matplotlib.axes import Axes as Axes
from .variantGridType import VariantGridView, DataWrapper, ViewPos, Y_STACK

from ._plot_config_ import CASE_COLORS, CTRL_COLORS

class MutationBarView(VariantGridView):
    def __init__(self) -> None:
        super().__init__()
        self._pos = ViewPos.LEFT_STAND_IN
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
                print("yyyy")
            else:
                # Plot cases 
                ax.barh(_y_pts, homo_z[1], color=CASE_COLORS[homo_i])
                ax.barh(_y_pts, hetro_z[case_i], left=homo_z[case_i], color=CASE_COLORS[hetro_i])
                ax.grid()
                if dw.get_n_ctrls() > 0:
                    ax.barh(_y_pts, -homo_z[ctrl_i], color=CTRL_COLORS[homo_i])
                    ax.barh(_y_pts, -hetro_z[ctrl_i], left=-homo_z[ctrl_i], color=CTRL_COLORS[hetro_i])

                    ax.set_xlim([-1,1])
                else:
                    ax.set_xlim([0,1])

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

        # fig = key_ax.figure
        # key_txt = ["Holo. Ref.","Hetro.","Homo. alt.","No Data"]
        # sm = ScalarMappable(cmap=colors.ListedColormap([CASE_COLORS[1],CASE_COLORS[2], CASE_COLORS[3],'#FFFFFF']))
        # cbar = fig.colorbar(sm,cax=key_ax, orientation="horizontal")
        # l = len(key_txt)
        # cbar.set_ticks(ticks=((np.arange(l)/l)+(1/(2*l))), labels=key_txt)
        _blank = "   "         
        key_txt = [
            ["Ctrl/Case", _blank, _blank],
            ["Homo. Ref",_blank, _blank],
            ["Hetrozygos", _blank,_blank],
            ["Home Alt.", _blank, _blank],
            ["No Data", _blank, _blank]]
        key_colors = [
                        ["#00000000", "#00000000", "#00000000"],
                        ["#00000000", CTRL_COLORS[2], CASE_COLORS[2]],
                        ["#00000000", CTRL_COLORS[3], CASE_COLORS[3]],
                        ["#00000000", CTRL_COLORS[4], CASE_COLORS[4]],
                        ["#00000000", CTRL_COLORS[1], CASE_COLORS[1]]]
        tab = key_ax.table(cellText=key_txt,cellColours=key_colors, loc="center", colLoc="center", colWidths=[self.key_column_width, self.key_row_hight,self.key_row_hight])
        tab.auto_set_font_size([False, False, False])
        tab.auto_set_column_width([1, 0,0])
        key_ax.axis('off')
    

    # === Override for functionality ===
    def should_add_x_scroll(self) -> bool:
        if self.stack_mode != Y_STACK:
            return False
        return super().should_add_x_scroll()
    
    def get_plot_names(self) -> list[str]:
        if self._is_main:
            return ["Mutation Frequency"]
        else:
            return ["Mut\nFreq."]
