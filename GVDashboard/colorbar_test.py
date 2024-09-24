import matplotlib as mpl
import matplotlib.cm as clrmp
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as colors

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.widgets import Slider
import allel as al
from VCF.dataFetcher import DataFetcher, DataWrapper

from VCF.dataWrapper import VcfDataWrapper as Wrapper
#from VCF.vcfTest import *

from VCF.vcfTest import getData
from VCF.vcfTest import TEST_FILE

MUTATION_FREQ_SPECTRUM = ['#81C4E7','#CEFFFF','#C6F7D6', '#A2F49B', '#BBE453', '#D5CE04', '#E7B503', '#F6790B', '#F94902', '#E40515']

def update(val):
    ax.set_ylim(dw.get_n_variants()-val, dw.get_n_variants()-val-span)
    
if __name__ == "__main__":
    dw = DataFetcher.load_data("./Data/med.vcf")
    assert(isinstance(dw,DataWrapper))
    
    
    fig, ax = plt.subplots(figsize=(10,5))
    cmap = colors.ListedColormap(["#00000000","#002164", "g", "y"])
    #ax.pcolormesh(dw.get_zygosity(), cmap=cmap, vmax=2, vmin=-1)
    # gs = GridSpec(ncols=3, nrows=1, width_ratios=[8, 0.5, 2])
    gs = GridSpec(ncols=1, nrows=1)
    ax = fig.add_subplot(gs[0])
    #####a = ax.matshow(dw.get_zygosity().transpose(), cmap=cmap, vmax=2, vmin=-1)
    #a = ax.pcolorfast(dw.get_zygosity(), cmap=cmap, vmax=2, vmin=-1)
    
    all_prob_mat = np.matrix(dw.get_mutation_probability())

    #self.colors = colors.ListedColormap(MUTATION_FREQ_SPECTRUM)
    ax.pcolorfast(all_prob_mat, cmap=colors.ListedColormap(MUTATION_FREQ_SPECTRUM), vmin=0, vmax=100)
    span = 10
    ax.set_ylim(span,0)
    
    plt.show()
    
    ### Testing the colormap for mutation-freq:
    # fig, ax = plt.subplots(figsize=(1, 10), layout='constrained')
    # MUTATION_FREQ_SPECTRUM = ['#81C4E7','#CEFFFF','#C6F7D6', '#A2F49B', '#BBE453', '#D5CE04', '#E7B503', '#F6790B', '#F94902', '#E40515']
    # cmap = colors.ListedColormap(MUTATION_FREQ_SPECTRUM, 10)
    # #ax.imshow(cmap=colors)
    # #cmap = mpl.cm.viridis
    # # bounds = ['10%','20%','30%','40%','50%','60%','70%', '80%','90%', '100%']
    # bounds = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # norm = colors.BoundaryNorm(bounds, cmap.N) #, extend='both')
    # fig.colorbar(clrmp.ScalarMappable(norm=colors.Normalize(0, 1), cmap=cmap),cax=ax, orientation='vertical', label="Zygosity Frequency key")
    

    fig, ax = plt.subplots(figsize=(0.3,3), layout='constrained')
    # Define the color spectrum
    MUTATION_FREQ_SPECTRUM = ['#81C4E7','#CEFFFF','#C6F7D6', '#A2F49B', '#BBE453', '#D5CE04', '#E7B503', '#F6790B', '#F94902', '#E40515']
    # Create a continuous colormap
    cmap = colors.LinearSegmentedColormap.from_list('custom_cmap', MUTATION_FREQ_SPECTRUM)
    # Normalize the color scale
    norm = colors.Normalize(vmin=0, vmax=100)
    # Create the colorbar
    cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='vertical', label="Zygosity Frequency key")
    # Set custom ticks and labels
    ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels([f'{tick}%' for tick in ticks])
    plt.show()


    # data = getData()
    # w = Wrapper(data)
    print("this is dw.get_n_variants:\n", dw.get_n_variants())
    print("this is dw.get_zygosity:\n", dw.get_zygosity())
    print("this is dw.get_n_samples:\n", dw.get_n_samples())
    
    print("this is pos-size:\n", dw.get_pos().size)
        

    zygo_is_homo = dw.gt_data.is_hom_alt()
    print("This is zygo_is_homo:\n", zygo_is_homo)
    zygo_is_hetero = dw.gt_data.is_het()
    print("This is zygo_is_hetreo:\n", zygo_is_hetero)

    # Frequency of homzygos per position
    z_homo = zygo_is_homo.sum(axis=1)/dw.get_n_samples()
    z_het = zygo_is_hetero.sum(axis=1)/dw.get_n_samples()
    z_total_probability = (z_homo + z_het)*100
    print("this is freq of homozygos:\n",z_homo)
    print("this is freq of heterozygos:\n",z_het)
    print("this is total mutation probability:\n",z_total_probability[:5])
    

    # Frequency of any mutation (note diferance between columns and rows: will fix this in the future)
    zygo = dw.get_zygosity()
    mutation_matrix = np.matrix(zygo)
    
    zygo[zygo<0] = 0 # make zygosity counts strictly positive for sum (ignore missing data)
    z = zygo.sum(axis=0)*100/(dw.get_n_samples()*2) # 2 times no. variants assuming diploidicity 

    
    
    
    
    ###########################
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
    ######################
    # # cax_1 = fig.add_subplot(gs[1])
    # # cax_1.matshow(dw.get_zygosity(), cmap=cmap, vmax=2, vmin=-1)
    # # divider = make_axes_locatable(cax_1)
    # # cax_2 = divider.append_axes('right', size='20%', pad=0.0)
    # # slider_pos = 0
    # # s = Slider(ax=cax_2, label="Pos", valmin=0, valmax=dw.get_n_variants()-span, orientation="vertical")
    # # s.on_changed(update)
    # # plt.show()



    