# Benchmarking tests
This directory contains the scripts used to conduct several benchmarking tests.

These tests are:
- Tests for `.vcf` dataset [reading and filtering](FileRead/README.md) times in the `FileRead/` directory.
- Tests for data [plotting and rendering](Plots/README.md) in `Plots/`.
- Tests for data [filtering](pdvsnp/README.md) using either a Pandas dataframe or NumPy arrays in `pdvsnp/`.

> [!NOTE]
> All benchmarking tests must be run in an activated virtual environment (`.venv`) with all dependencies installed.
> 
> For details on how to create this `.venv` please see the [`README.md`](../README.md#make-the-virtual-environment) in the repo root.
