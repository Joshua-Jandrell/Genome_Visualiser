# Placeholder script that generates random dummy plots for demonstrative purposes

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.colors import LogNorm
from matplotlib.figure import Figure as Figure

def make_plot()->Figure:
    # # Fixing random state for reproducibility
    # np.random.seed(19680801)

    Z = np.random.rand(20, 100)

    # fig, (ax0, ax1) = plt.subplots(2, 1)

    # c = ax0.pcolor(Z)
    # ax0.set_title('default: no edges')

    # c = ax1.pcolor(Z, edgecolors='k', linewidths=1)
    # ax1.set_title('thick edges')

    # fig.tight_layout()
    # return fig
    	# the figure that will contain the plot 
    fig = Figure(figsize = (5, 5), 
				dpi = 100) 

	# list of squares 
    y = [i**2 for i in range(101)] 

	# adding the subplot 
    plot1 = fig.add_subplot(111) 

	# plotting the graph 
    plot1.set_title("Cool plot")
    plot1.pcolor(Z, edgecolors='k', linewidths=0)
    return fig