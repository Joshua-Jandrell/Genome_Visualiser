#  Filter and Read Bechnmarking: Bcftools vs Scikit-allel:

This disrectory contains files used to test the time taken to read and filter `.vcf` files using different approches.

Each approch usese [bcftools](https://github.com/samtools/bcftools) and/or [scikit-allel](https://github.com/cggh/scikit-allel) to filter genomic datasets stored in `.vcf.gz` files and read their contents into a Python data structre. 

## Run tests
The tests can be run (from the repo root) with the following command:

``` bash
python Benchmarking/FileRead/timeFileReading.py 
```

> [!NOTE]
> These tests must be run with the `.venv` (containing sckikit-allel) activated.

> [!IMPORTANT]
> These tests require a build bcftools to run.
> Either [build a local version](../README.md#local-build) of bcftools or update the `bcftools` field in [`data_config.toml`](FileRead/data_config.toml) to refferacne and exiting install of bcftools.



``` bash
python Benchmarking/FileRead/verifyFileRead.py
```
