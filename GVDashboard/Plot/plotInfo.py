# This script contains simple constructors for various plot types
import numpy as np
import matplotlib as plt

from VCF.dataWrapper import VcfDataWrapper as DataWrapper
import VCF.dataWrapper as dw
from VCF.filterInfo import DataSetInfo

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
from matplotlib.widgets import Slider, Button, RadioButtons

from Plot.ViewInfos import ViewInfo_base, viewSetManager, get_view_sets, plot_sets
# Class used to store all plot infos and construct the final figure
class ViewPlotter:
    """ 
        Stores all plot information and constructs the final figure
    """
    def __init__(self,figure:Figure, views:list[ViewInfo_base]|None=None) -> None:
        self.fig = figure
        self.plots = []
        self.default_data_wrapper = None

    def plot_figure(self, views:list[ViewInfo_base], size:tuple[int, int]=tuple([0,0]), can_expand:tuple[bool, bool]=tuple([False, False]))->tuple[int, int]:
        """
        Plot a figure on the canvas.\n
        Size is the ideal size of the canvas [width, hight]. If set to 0 it is assumed that the plot can expand.\n
        Can expand determines if the plot can expand or if the given sie is an absolute limit.\n
        Returns the desired figure width and hight, or [0, 0] if figure should not be shown.
        """
        # clear any existing plots on the figure
        self.fig.clear()

        # group views into a collection of view sets
        view_sets = get_view_sets(views)

        width, hight = plot_sets(view_sets, self.fig, size=size, can_expand=can_expand,)
        return width, hight