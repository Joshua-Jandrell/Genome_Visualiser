from typing import Literal
import numpy as np
import matplotlib as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from VCF.dataWrapper import VcfDataWrapper as DataWrapper
import VCF.dataWrapper as dw

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec

from .viewInfo import ViewInfo_base
from .variantGridType import GRID_TYPE_KEY, VariantGridView
from Util.box import Box


class FrequencyView(ViewInfo_base):
    def __init__(self) -> None:
        super().__init__()
        self.min_window = 400
        self.plot_density = False
        self.n_bins = 50

    def get_desired_hight(self) -> list[int]:
        return [self.min_window]
    def get_desired_width(self) -> list[int]:
        return [100000]
    
    def make_plots(self,axs:list[Axes],size:tuple[int,int])->str:
        axis = axs[0]
    
        
        wrapped_data = self.dataset_info.get_data()
        pos = wrapped_data.get_pos()

        min = pos.min()
        max = pos.max()
        # setup windows   #  bin_size:  Ratio recommened:  (750:100000)
        bin_size = (max-min)/self.n_bins
        
        bins = np.arange(min, max, bin_size)
        bin_size = int(bin_size)
        if self.plot_density == False:
            axis.hist(x=pos, bins=bins, edgecolor='black', color = '#A2F49B') #DDCC77 <-sand yellow  #A2F49B <- mint green
            axis.set_mouseover(True)
            axis.set_facecolor('#FEFBE9')  #FEFBE9 <- pale biege
            axis.set_xlabel('Chromosome position (bp)')
            axis.set_ylabel('Variant count, bp$^{-1}$')
            axis.set_title(f'Number of Mutations per {bin_size} positions')

        else:     
        
            # compute variant density in each window
            h, _ = np.histogram(pos, bins=bins)
            y = h / bin_size

            axis.bar(_[:-1], y, width=np.diff(_), align='edge', edgecolor='black', color='#CC6677') #CC6677 <- rose
            axis.set_mouseover(True)
            axis.set_facecolor('#E8ECFB')
            axis.set_xlabel('Chromosome position (bp)')
            axis.set_ylabel('Variant density (count per bp $^{-1}$)')
            axis.set_title('Mutation Frequency Density')

        return super().make_plots(axs, size)
            
    
    def set_should_plot_density(self,plot_density):
        self.plot_density = plot_density