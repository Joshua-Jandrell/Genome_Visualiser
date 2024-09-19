"""
Contains functions used to set up data for plot speed testing.
"""

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.axes import Axes

DPI = 100

def get_plot_figure(x_pixels=300, y_pixels=300, dpi=DPI)->tuple[Figure, Axes]:
    """
    Creates a matplotlib figure to be used to test plot speeds.
    """
    px = 1/dpi
    fig = Figure((x_pixels*px, y_pixels*px), dpi=dpi)
    ax = fig.add_subplot(111)
    return fig, ax