import matplotlib as mpl
import numpy as np

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
import matplotlib.pyplot as plt
import os
import allel as al

from GVDashboard.VCF.vcfTest import getData
TEST_FILE = os.path.realpath("./Data/afr-small.vcf")
def plot_windowed_variant_density(pos, window_size=500, title=None):

    window_size=500
    data = getData()
    # and make data into dataframe
    df = al.vcf_to_dataframe(TEST_FILE)
    pos = df['POS'][:]
    
    # setup windows 
    bins = np.arange(0, pos.max(), window_size)
    
    # use window midpoints as x coordinate
    x = (bins[1:] + bins[:-1])/2
    
    # compute variant density in each window
    h, _ = np.histogram(pos, bins=bins)
    y = h / window_size
    print("h:\n", h, "Size:", h.shape)
    print("_:\n", _[:-1], "Size:", _[:-1].shape)
    print("x:\n",x, "Size:", x.shape)
    print("y:\n",y,"Size:", y.shape)
    # plot
    fig, ax = plt.subplots(figsize=(12,5))
    # fig = Figure((10,10),dpi=100)
    # ax = fig.add_subplot(111)

    print(ax)
    #ax.plot(x, y)
    
    #ax.bar(x,y, align='edge')
    #ax.bar(_[:-1], h)
    ax.plot(_[:-1], h)

    #ax.bar(x=_[:-1],height=y)
    ax.hist(x=pos, bins=bins)


    ax.set_xlabel('Chromosome position (bp)')
    ax.set_ylabel('Variant density (bp$^{-1}$)')
    if title:
        ax.set_title(title)

    plt.show()

if __name__ == "__main__":
    plot_windowed_variant_density(np.array([1,3,4,5,6,7,10,14,20,21,22,23,32,34]),5)