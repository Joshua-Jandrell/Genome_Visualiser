import matplotlib as mpl
import numpy as np

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
import matplotlib.pyplot as plt
import allel as al

from GVDashboard.VCF.vcfTest import getData
from GVDashboard.VCF.vcfTest import TEST_FILE

def plot_windowed_variant_count(pos, window_size=500, title=None):

    window_size=500  #Ratio recommened:  (500:100000)
    #data = get_pos()
    
    # Make data into dataframe
    df = al.vcf_to_dataframe(TEST_FILE)
    pos = df['POS'][:]
    
    # setup windows 
    bins = np.arange(pos.min(), pos.max(), window_size)
    
    # plot
    fig, ax = plt.subplots(figsize=(12,5))
    
    print("Count plot!",ax)

    ax.hist(x=pos, bins=bins, edgecolor='black', color = '#A2F49B') #DDCC77 <-sand yellow
    ax.set_mouseover(True)
    ax.set_facecolor('#FEFBE9')


    ax.set_xlabel('Chromosome position (bp)')
    ax.set_ylabel('Variant count, bp$^{-1}$')
    if title:
        ax.set_title(title)

    plt.show()

if __name__ == "__main__":
    plot_windowed_variant_count(np.array([1,3,4,5,6,7,10,14,20,21,22,23,32,34]),5)

#========================================================================
#                  DENSITY PLOT BELOW
#========================================================================
def plot_windowed_variant_density(pos, window_size=500, title=None):

    window_size=500   #Ratio recommened:  (500:100000)
    data = getData()
    # Make data into dataframe
    df = al.vcf_to_dataframe(TEST_FILE)
    pos = df['POS'][:]
    
    # setup windows 
    bins = np.arange(pos.min(), pos.max(), window_size)
    
    # compute variant density in each window
    h, _ = np.histogram(pos, bins=bins)
    y = h / window_size

    # plot
    fig2, ax2 = plt.subplots(figsize=(12,5))
    
    # Set the color for each bar
    #colors = ListedColormap(['#AA4499','#882255','#CC6677','#BB5566','#DDCC77','#DDAA33','#9970AB'])

    print("Density plot!",ax2)
    
    ax2.bar(_[:-1], y, width=np.diff(_), align='edge', edgecolor='black', color='#CC6677')
    ax2.set_facecolor('#E8ECFB')
    ax2.set_xlabel('Chromosome position (bp)')
    ax2.set_ylabel('Variant density (count per bp $^{-1}$)')
    if title:
        ax2.set_title(title)

    plt.show()
    
if __name__ == "__main__":
    plot_windowed_variant_density(np.array([1,3,4,5,6,7,10,14,20,21,22,23,32,34]),5)