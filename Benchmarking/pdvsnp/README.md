# Pandas vs Numpy benchmarking 

This directory contains code used to test the difference in sorting time when using a numpy (np) array compared to a pandas (pd) dataframe.

These speed tests are intended to help inform how in memory post-filtering should be implemented in the final version of the app.

## Run tests 
The tests can be run (from the repo root) from the `getSortTimes.py` file using the following command:
```bash
python Benchmarking/pdvsnp/getSortTimes.py
```

⚠️ Note: These tests must be run with the `.venv` activated or with numpy and pandas installed.
