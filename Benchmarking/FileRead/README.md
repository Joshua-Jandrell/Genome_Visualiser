#  Filtering and Reading Bechnmarking — Bcftools vs Scikit-allel:

This directory contains files used to test the time taken to read and filter `.vcf` files using different approaches.

Each approch uses [bcftools](https://github.com/samtools/bcftools) and/or [scikit-allel](https://github.com/cggh/scikit-allel) to filter genomic datasets stored in `.vcf.gz` files and read their contents into a Python data structure. 

## Run tests
The tests can be run (from the repo root) with the following command:

``` bash
python Benchmarking/FileRead/timeFileReading.py 
```

> [!IMPORTANT]
> These tests require a build of bcftools in order to run.
> Either [build a local version](../../README.md#local-build) of `bcftools`, or update the `bcftools` field in [`data_config.toml`](data_config.toml) to reference an existing installation of bcftools.

> [!NOTE]
> These tests must be run with the `.venv` (containing sckikit-allel) activated.

> [!NOTE]
> When running these tests, data files will be downloaded and saved in the `./Data` directory.

## Methodology
The times taken to perform filtering and reading operation are recorded using three different approaches: [bcftools filtering](#bcftools-filtering), [scikit-allel filtering](#scikit-allel-filtering), and [hybrid filtering](#hybrid-filtering). 

Each filtering approach ([detailed below](#Filtering-approaches)) is divided into several sub-operations that are timed individually to identify bottelnecks.
Each sub-operation is repeated 10 times and averaged to impove the results' reliability.

In general, each filtering approach reads in a genomic dataset (stored in a `.vcf.gz.` file) and selects variants in the region of `10000-11000` (on the first chromosome listed) while exclauding variants with a quality value less than `25`.
The dataset is split into two subsets: one for case samples (listed in a seperate `.tsv` file) and one for control samples (all other samples not listed in the `.tsv`).
Each subset is represented by a separate Python dictionary (`dict`).


### Test data
Three publically-available genomic datasets: `afr.vcf.gz` (150 MB), `med.vcf.gz` (730 KB), and `afr-small.vcf.gz` (98 KB) are used during these speed tests.
Each dataset is accompanied by a randomly-generated case `.tsv` file with the naming convention: `<dataset-name>.case.tsv`.

Although case (`.tsv`) files are randomly generated, the same case file is used for all three approaches to ensure that results are comparable.

> [!TIP]
> All files used for testing will be automatically downloaded when either `Benchmarking/FileRead/timeFileReading.py ` or `Benchmarking/FileRead/verifyFileRead.py` is run.
> Files can also be downloaded with the command: `python Benchmarking/FileRead/fetchData.py`.

### Files generated during testing

In cases where the creation of addtional dataset (`.vcf.gz`) and/or index (`.csi`) files is timed, any exisitng files with the same names are removed before tests are run to ensures consistency and repoducability.
All files created during speed-testing are delected once test have been complected; with the excaption of index files which are useful beyond the speed-tests and re-usable in practice. 

## Filtering approaches

### bcftools filtering
This approch uses bcftools to extract data (filter) and split the dataset into two case/control subset `.vcf.gz` files. The subset files are then read into memeory using scikit-allel.

Two seperate bcftools-based filtering philosophies are investiagted: one-short filtering and filteraing with seperate operations. 
In one-shot filtering a single bcftools command is used to filter (by region and quality) and split (into cases and controls).
When filtering with seperate operations different bcftools operation are used to filter and split.
Both philosophies are investigated to detemine if the advanatge of only needing to call bcftools once (for one-shot filtering) is more benefical than splitting a smaller dataset (seperate operations)
____

### scikit-allel filtering

### Hybrid filtering.

## Verifcation
Unit tests have been created to verify that the file reading and filtering methods tested 

``` bash
python Benchmarking/FileRead/verifyFileRead.py
```
