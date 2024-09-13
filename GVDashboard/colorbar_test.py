import matplotlib as mpl
import numpy as np

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.widgets import Slider
import allel as al
from VCF.dataFetcher import DataFetcher, DataWrapper

from VCF.vcfTest import getData
from VCF.vcfTest import TEST_FILE

def update(val):
    ax.set_ylim(dw.n_variants-val, dw.n_variants-val-span)
    
if __name__ == "__main__":
    dw = DataFetcher.load_data("./Data/afr-small.vcf")
    assert(isinstance(dw,DataWrapper))
    fig, ax = plt.subplots(figsize=(12,8))
    cmap = colors.ListedColormap(["#00000000","#002164", "g", "y"])
    #ax.pcolormesh(dw.get_zygosity(), cmap=cmap, vmax=2, vmin=-1)
    gs = GridSpec(ncols=3, nrows=1, width_ratios=[8, 0.5, 2])
    ax = fig.add_subplot(gs[0])
    #a = ax.matshow(dw.get_zygosity().transpose(), cmap=cmap, vmax=2, vmin=-1)
    a = ax.pcolorfast(dw.get_zygosity().transpose(), cmap=cmap, vmax=2, vmin=-1)

    span = 150
    ax.set_ylim(span,0)

    # Make slider (scroll) for the figure (simple slider)
    # slider_pos = 0
    # divider = make_axes_locatable(ax)
    # sax = divider.append_axes('right', size='5%', pad=0.05)
    # s = Slider(ax=sax, label="Pos", valmin=0, valmax=dw.n_samples-span, orientation="vertical")
    # s.on_changed(update)

    # c = fig.colorbar(a, shrink=0.3, pad = 0.2)
    # l = len(cmap.colors)
    # step = (l-1)/l
    # c.set_ticks(np.arange(-1+step/2,-1+4*step,step))
    # c.set_ticklabels(["No data", "Homozygous", "Heterozygous", "Homozygous Mutation"])

    # divider = make_axes_locatable(ax)
    # cax_1 = divider.append_axes('right', size='5%', pad=0.05)
    cax_1 = fig.add_subplot(gs[1])
    cax_1.matshow(dw.get_zygosity().transpose(), cmap=cmap, vmax=2, vmin=-1)
    divider = make_axes_locatable(cax_1)
    cax_2 = divider.append_axes('right', size='20%', pad=0.0)
    slider_pos = 0
    s = Slider(ax=cax_2, label="Pos", valmin=0, valmax=dw.n_variants-span, orientation="vertical")
    s.on_changed(update)
    plt.show()

import matplotlib.pyplot as plt
import numpy as np



    