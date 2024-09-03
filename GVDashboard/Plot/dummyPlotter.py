# Placeholder script that generates random dummy plots for demonstrative purposes

import matplotlib.pyplot as mpl
import numpy as np

from matplotlib.figure import Figure as Figure
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec

import allel as al

from VCF.vcfTest import getData

# Colors
MUT_COLORS = colors.ListedColormap(["#00000000","#002164", "g", "y"])
ALLELE_COLORS = colors.ListedColormap(["#00000000","grey", "#29E838", "#E829D8", "#E89829", "#2979E8"])

X_TAKE = 5
Y_TAKE = 10

def allele_to_numb(a:str):
    if len(a) > 1:
        return 0
    if a == "A":
        return 1
    elif a == "C":
        return 2
    elif a == "G":
        return 3
    elif a == "T":
        return 4
    else:
        return -1
    


def allele_numbers(allels:np.array):
    return [allele_to_numb(a) for a in allels]

    



def make_plot()->Figure:
    # Get BCF (trial) data 
    data = getData()

    plot_data = al.GenotypeArray(data['calldata/GT'][0:X_TAKE, 0:Y_TAKE])

    ref = data['variants/REF'][0:X_TAKE]
    plot_ref = np.matrix(allele_numbers(ref))

    Z = plot_data.is_hom_alt() * 2 + plot_data.is_het() * 1 + plot_data.is_missing() * (-1)
    Z = Z.transpose()

    #Z = plot_data.to_haplotypes()
    #Z = np.random.random_integers(-1, 2, (20,100))
    rows,cols = Z.shape
    gs = GridSpec(3, 1, height_ratios=[1, 1, rows])
    fig = Figure(figsize = (5, 5), 
				dpi = 100)

	# adding the subplot
    plot0 = fig.add_subplot(gs[0])
    plot1 = fig.add_subplot(gs[1], sharex=plot0)
    plot2 = fig.add_subplot(gs[2], sharex=plot0)

	# plotting the graph 
    plot2.pcolor(Z[::-1,:], linewidths=0, cmap=MUT_COLORS, vmax=2, vmin=-1)


    # Plot the ref graph
    plot0.pcolor(plot_ref,linewidth=1,edgecolors="k",cmap=ALLELE_COLORS, vmin=-1, vmax=4)
    plot0.set_xticks([])
    plot0.set_yticks([])
    plot0.set_ylabel("Ref.", rotation=0, va="center", ha="right")
    # Add text for each allel
    for y in range(plot_ref.shape[0]):
        for x in range(plot_ref.shape[1]):
            plot0.annotate(f"{ref[x]}", xy=(x+0.5,y+0.5), horizontalalignment='center', verticalalignment='center')
            
    # Plot the alternate alleles
    alt = data["variants/ALT"][:X_TAKE,:]
    # Make a matrix of alt values
    plot_alt = np.array([allele_numbers(r) for r in alt])
    filter_mask = np.array([np.max(plot_alt,axis=0) >= 0][0]) # Remove rows where no alt allele is specified
    plot_alt = plot_alt[:,filter_mask].transpose()

    plot1.pcolor(plot_alt,linewidth=1,edgecolors="k",cmap=ALLELE_COLORS, vmin=-1, vmax=4)
    plot1.set_xticks([])
    plot1.set_yticks([])
    plot1.set_ylabel("Alt.", rotation=0, va="center", ha="right")


    # Forat the figure
    fig.subplots_adjust(hspace=0, wspace=0)

    return fig