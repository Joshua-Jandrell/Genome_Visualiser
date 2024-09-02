# Placeholder script that generates random dummy plots for demonstrative purposes

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.figure import Figure as Figure

# Colors
MUT_COLORS = []

def make_plot()->Figure:
    # # Fixing random state for reproducibility
    # np.random.seed(19680801)

    ref = np.random.random_integers(0, 4, (20,1))

    Z = np.random.random_integers(0, 2, (20,100))
    fig = Figure(figsize = (5, 5), 
				dpi = 100) 

	# adding the subplot 
    plot1 = fig.add_subplot(111) 

	# plotting the graph 
    plot1.set_title("Cool plot")
    plot1.pcolor(Z, edgecolors='k', linewidths=0)
    return fig