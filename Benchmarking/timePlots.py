"""Used find the plotting time of various plotting methods"""
# For time keeping
import os
import csv
import time
import tracemalloc

import matplotlib as mpl

from Plots import get_random_zygoisty, get_plot_figure
from Plots.plotMethods import * 
from trackTimeMem import monitor_time
from config import *

BLOCK_SIZE = 10

SAVE_DIR = os.path.join(RESULT_DIR,"Plots","ZygsityPlottingTimes")


N_CYCLES = 1
"""The number of times each plot is run, taken as an average to improve reliability."""

VAR_COUNTS = [50]#, 500, 500, 50000, 500000]
"""Variant volume counts used for benchmarking."""

SAMPLE_COUNTS = [10]#, 100]#, 1000, 10000]
"""Number of samples to be used in moc data sets when benchmarking."""

DPI_VALS = [50, 100, 200]
"""DPI Values for figures, used to see if this impacts plot time."""

def get_csv_header():
    main_heads = ["plot_type", "n_variants", "n_samples", "n_values", "dpi", "average"]
    for i in range(N_CYCLES):
        main_heads.append(f"cycle_{i}")

    return main_heads


def time_zygoisty_plots(output_file:str = "zygosity_plotting_times.csv"):

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
                    _times = monitor_time(fxn=lambda: method(data, fig), n_runs=N_CYCLES)
                    _ave = sum(_times)/N_CYCLES
                    _csv.writerow(_row+[_ave]+_times)
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


# def time_zygosity_plots(n_variants, n_samples):
#     data = get_random_zygoisty(n_variants=n_variants, n_samples=n_samples)
#     fig, ax = get_plot_figure(n_variants*BLOCK_SIZE, n_samples*BLOCK_SIZE)
#     start = time.time()
    
#     end = time.time()-start
#     print(end)

#     # fig.clear()
#     # start = time.time()
#     # ax.imshow(data, cmap=CMAP)
#     # end = time.time()-start
#     # print(end)

#     # fig.clear()
#     # start = time.time()
#     # ax.pcolorfast(data, cmap=CMAP)
#     # end = time.time()-start
#     # print(end)
#     jou = 3

#     for _ in range(10):
#         tracemalloc.start()
#         #fig.clear()
#         fig, ax = get_plot_figure(n_variants*BLOCK_SIZE, n_samples*BLOCK_SIZE)
#         start = time.time()
#         ax.matshow(data, cmap=ZYGOSITY_CMAP)
#         end = time.time()-start
#         print(end)
#         print(tracemalloc.get_traced_memory())

#         tracemalloc.stop()
if __name__ == "__main__":
    time_zygoisty_plots()