"""Script used to set up default test settings and data save paths."""

import os

DATA_FOLDER = os.path.realpath("./Data/")
RESULT_DIR = os.path.realpath("./Results")

#RESULT_FOLDER = os.path()
BLOCK_SIZE = 10

N_CYCLES = 10
"""The number of times each plot is run, taken as an average to improve reliability."""

VAR_COUNTS = [50, 500, 5000, 50000]
"""Variant volume counts used for benchmarking."""

SAMPLE_COUNTS = [10, 100, 1000, 10000]
"""Number of samples to be used in moc data sets when benchmarking."""

DPI_VALS = [50, 100, 150, 200]
"""DPI Values for figures, used to see if this impacts plot time."""