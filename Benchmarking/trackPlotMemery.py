"""
Track the memory used by various plotting functions.
"""

"""Used find the plotting time of various plotting methods"""
# For time keeping
import os
import csv

import matplotlib as mpl

from Plots import get_random_zygoisty, get_plot_figure
from Plots.plotMethods import * 
from trackTimeMem import monitor_memory
from config import *

SAVE_DIR = os.path.join(RESULT_DIR,"Plots","ZygsityPlotting")

def get_csv_header():
    main_heads = ["plot_type", "n_variants", "n_samples", "n_values", "dpi", "average_mem", "average_peak_mem"]
    for i in range(N_CYCLES):
        main_heads.append(f"memory_{i}")
    for i in range(N_CYCLES):
        main_heads.append(f"peak_memory_{i}")

    return main_heads


def time_zygoisty_plots(output_file:str = "zygosity_plotting_memory.csv"):

    # Make results directory if required 
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Open file and make a csv writer 
    _f = open(os.path.join(SAVE_DIR, output_file), mode='w', newline="")
    _csv = csv.writer(_f)
    _csv.writerow(get_csv_header())

    # Iterate through number variants
    for _v in VAR_COUNTS:
        # Iterate though number of samples
        for _s in SAMPLE_COUNTS:

            # Make data 
            data = get_random_zygoisty()
            
            # Iterate through various DPI values 
            for _dpi in DPI_VALS:

                _n_values = _v * _s

                # Get a matplotlib figure
                fig, ax = get_plot_figure(_s * BLOCK_SIZE, _v * BLOCK_SIZE, dpi=_dpi)
                
                # plot images for all methods 
                for i, method in enumerate(ZYGO_PLOT_METHODS):

                    # skip p color as it is very slow
                    if method == pcolor_plot and (_v > VAR_COUNTS[0] or _s > VAR_COUNTS[0] or _dpi != DPI_VALS[1]):
                        continue

                    # time plotting and write to csv row
                    _row = [ZYGO_PLOT_METHOD_NAMES[i], _v, _s, _n_values, _dpi]
                    _mem, _peak = monitor_memory(fxn=lambda: method(data, fig), n_runs=N_CYCLES)
                    _ave_mem = sum(_mem)/N_CYCLES
                    _ave_peak = sum(_peak)/N_CYCLES
                    _csv.writerow(_row+[_ave_mem, _ave_peak]+_mem+_peak)
    _f.close()

def make_verification_images():
    """
    Function used to generate simple zygosity plots to verify that the plotting system are working
    """
    pass
    data = get_random_zygoisty(50,10)
    fig, ax = get_plot_figure(500,100,100)
    pcolor_plot(data=data, fig=fig)
    #fig.draw()

if __name__ == "__main__":
    time_zygoisty_plots()