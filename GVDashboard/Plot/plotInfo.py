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

from Plot.ViewInfos import ViewInfo_base, ViewSetManager, get_view_sets

from .scrollWidget import ScrollWidget, ScrollManager
from Util.box import Box

# Class used to store all plot infos and construct the final figure
class ViewPlotter:
    """ 
        Stores all plot information and constructs the final figure
    """
    def __init__(self,figure:Figure, views:list[ViewInfo_base]|None=None) -> None:
        self.fig = figure
        self.plots = []
        self.default_data_wrapper = None
        