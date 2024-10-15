# Pandas vs NumPy benchmarking 

This directory contains code used to test the time taken to filter a dataset using a dictionary of NumPy (np) arrays, compared to a Pandas (pd) data frame. These test-times aid in selecting the fastest in-memory dataset-filtering method.

## Run tests 
The tests can be run (from the repo root) with the following command:
```bash
python Benchmarking/pdvsnp/getSortTimes.py
```

> [!NOTE]
> These tests must be run with the `.venv` activated or with NumPy and Pandas installed.

## Methodology 
Tests are run on randomly generate datasets where each data value is a float between `0` and `1`.

Datasets with  rows = `10`, `100`, `1000`, `10000` or `100000` and columns = `5`, `10`, `20` are tested to investigate the scalability of each filtering method.

During testing the dataset is filtered by selecting only rows with values between `0.25` and `0.75` in a single target column (which would contain filter-parameter values). 

To improve reliability, each filter operation is repeated 10 times with the average wall-time recorded.

## Verification 
The np array-based sorting method is verified by asserting that the data it contains after filtering is equivalent to the data stored in the pd data frame.
The pd data frame filtering method is assumed to be reliable because it is implemented entirely in the Pandas library.

## Results
A set of results generated on a computer with 1.7 GHz clock speed and 15.7 GB usable RAM can be found in [`Results/np_vs_pd_times.csv`](../../Results/np_vs_pd_times.csv)

> [!WARNING]
> If the tests are re-run, existing results will be overwritten.


