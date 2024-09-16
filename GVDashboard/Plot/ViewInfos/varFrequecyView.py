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
from .variantGridType import GRID_TYPE_KEY, GridParams, VariantGridView
from Util.box import Box


class FrequencyView(ViewInfo_base):
    def __init__(self) -> None:
        self.min_window = 400
        self.plot_density = False
        super().__init__()

    def get_desired_size(self) -> list[int]:
        return [self.min_window]
    
    def make_plots(self,axs:list[Axes],size:tuple[int,int], plot_box:Box, label:Literal["top", "bottom", "left", "right"]="none")->str:
        axis = axs[0]
        print("plotting")
        
        wrapped_data = self.dataset_info.get_data_wrapper()
        pos = wrapped_data.get_pos()
        
        # setup windows   #  Window_size:  Ratio recommened:  (750:100000)
        window_size = self.min_window
        
        bins = np.arange(pos.min(), pos.max(), window_size)
        
        if self.plot_density == False:
            axis.hist(x=pos, bins=bins, edgecolor='black', color = '#A2F49B') #DDCC77 <-sand yellow
            axis.set_mouseover(True)
            axis.set_facecolor('#FEFBE9')
            axis.set_xlabel('Chromosome position (bp)')
            axis.set_ylabel('Variant count, bp$^{-1}$')
            axis.set_title('Mutation Count frequency')

        else:     
        
            # compute variant density in each window
            h, _ = np.histogram(pos, bins=bins)
            y = h / window_size

            axis.bar(_[:-1], y, width=np.diff(_), align='edge', edgecolor='black', color='#CC6677')
            axis.set_mouseover(True)
            axis.set_facecolor('#E8ECFB')
            axis.set_xlabel('Chromosome position (bp)')
            axis.set_ylabel('Variant density (count per bp $^{-1}$)')
            axis.set_title('Mutation Density frequency')
            
        return axis
    
    def set_should_plot_density(self,plot_density):
        self.plot_density = plot_density