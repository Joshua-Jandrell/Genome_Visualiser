"""Script used to verify that plots are generated correctly"""
import os

import numpy as np

from  makeRandomData import get_random_zygoisty
from plotSetup import get_plot_figure
from plotMethods import *

from config import RESULT_DIR

SAVE_DIR = os.path.join(RESULT_DIR,"Plots","ZygsityPlottingVerification")

def make_verification_images():
    """Generate simple 20 by 10 images to verify that plots are generated correctly."""

    # Make results directory if required 
    os.makedirs(SAVE_DIR, exist_ok=True)

    n_v = 20 # 20 variants
    n_s = 10 # 10 samples 
    blocksize=10 # 10 pixels per block 
    data = get_random_zygoisty(n_variants=n_v, n_samples=n_s)
    
    for i, plot_method in enumerate(ZYGO_PLOT_METHODS):
        fig, _ = get_plot_figure(n_s*blocksize, n_v*blocksize,dpi=100)
        plot_method(data,fig)
        fig.savefig(os.path.join(SAVE_DIR,f"{ZYGO_PLOT_METHOD_NAMES[i]}.png"))

    # Save the random data so that it can be used to verify plots
    np.savetxt(os.path.join(SAVE_DIR, "data.txt"), data, fmt="%d")
    
if __name__ == "__main__":
    make_verification_images()