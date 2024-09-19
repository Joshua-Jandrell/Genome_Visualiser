"""Contains various plot methods for generating zygosity plots."""

from matplotlib import figure, colors

ZYGOSITY_CMAP = colors.ListedColormap(["#00000000","#002164", "g", "y"])

def pcolor_plot(data, fig:figure.Figure):
    fig.clear()
    axes = fig.add_subplot(111)
    axes.pcolor(data, cmap=ZYGOSITY_CMAP)

def pcolor_fast(data, fig:figure.Figure):
    fig.clear()
    axes = fig.add_subplot(111)
    axes.pcolorfast(data, cmap=ZYGOSITY_CMAP)

def pcolor_mesh(data, fig:figure.Figure):
    fig.clear()
    axes = fig.add_subplot(111)
    axes.pcolormesh(data,cmap=ZYGOSITY_CMAP)

def mat_show(data, fig:figure.Figure):
    fig.clear()
    axes = fig.add_subplot(111)
    axes.matshow(data,cmap=ZYGOSITY_CMAP)

def im_show(data, fig:figure.Figure):
    fig.clear()
    axes = fig.add_subplot(111)
    axes.imshow(data, cmap=ZYGOSITY_CMAP)

# Useful constants 

ZYGO_PLOT_METHOD_NAMES = ["pcolor", "pcolorfast", "pcolormesh", "matshow", "imshow"]
ZYGO_PLOT_METHODS = [pcolor_plot, pcolor_fast, pcolor_mesh, mat_show, im_show]