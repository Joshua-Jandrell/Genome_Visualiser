#  Filtering and Reading Bechnmarking — Bcftools vs Scikit-allel:

This directory contains files used to test the time taken to read and filter `.vcf` files using different approaches.

Each approch uses [bcftools](https://github.com/samtools/bcftools) and/or [scikit-allel](https://github.com/cggh/scikit-allel) to filter genomic datasets stored in `.vcf.gz` files and read their contents into a Python data structure. 

## Run tests

> [!Warning]
> Running tests will override any exisitng results.

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
All files created during speed-testing are deleted once test have been complected; with the excaption of index files which are useful beyond the speed-tests and re-usable in practice. 

## Filtering approaches

### bcftools filtering
This approach uses bcftools to extract data (filter) and split the dataset into two case/control subset `.vcf.gz` files. The subset files are then read into memory using scikit-allel.

Two separate bcftools-based filtering philosophies are investigated: one-short filtering and faltering with separate operations. 
In one-shot filtering a single bcftools command is used to filter (by region and quality) and split (into cases and controls).
When filtering with separate operations different bcftools operation are used to filter and split.
Both philosophies are investigated to determine if the advantage of only needing to call bcftools once (for one-shot filtering) is more beneficial than the advantage of splitting a smaller dataset (for separate operations).

The time to filter by region (position) only and not quality is recorded to identify the effect that adding multiple filter parameters has on filter times.

> [!NOTE]
> Before a `.vcf` dataset can be queried with bcftools it must be index with a `.csi` file.
> The time taken to index each file is recorded and included from completeness (and so that the maximum possible time can be determined).
> In practice indexing will only ever occur once at most as the index file can be kept with the dataset.

The code used for this method can be found in [`Benchmarking/FileRead/readMethods/bcftoolsFilter.py`](readMethods/bcftoolsFilter.py).
_____________________________________________

### in-mememroy (post) filtering
The approach used only the scikit-allel library (no bcftools).
Data is read directly into memory using the scikit-allel `read_vcf` method which produces a dictionary (`dict`) of [NumPy arrays](https://numpy.org/doc/stable/reference/generated/numpy.array.html).
The chromosome and region must be specified here otherwise the large datasets (like`afr.vcf.gz`) will cause the system to freeze due to high memory requirements (`afr.vcf.gz` is over 6.8 GB when uncompressed).

The scikit-allel `vcf_to_dataframe` method is also used to load certain data from `.vcf` files to [Pandas dataframes](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).

After the file has been loaded into memory, the data frames is used to filter according to quality.

The case `.tsv` file is loaded into memory using the built-in pyton `open()` function. The sample data (stored in Numpy arrays) is split by indexing the data array with a boolean array where `True` indicates case samples and `False` indicates control samples.

The code used for this method can be found in [`Benchmarking/FileRead/readMethods/postFilterpy`](readMethods/postFilter.py).
_____________________________________________

### Hybrid filtering.
The hybrid filter method is intended to leverage on the advantages of both bcftools and in-memory filtering approaches while mitigating their drawbacks.

Becftools is used to filter by region and quality because this approach is much faster than filtering by region with sckikit-allel (especially when a `.csi` index file already exists).
This approach forgoes the need to read the  `.vcf` file in again as a pandas data frame.

The slit into case and control data is done in memory to reduce the number of files written to and read from. When the filtered dataset is small, the in-memory split has a negligible duration (compared to filtering and reading)

## Verification
Unit tests have been created to verify that the file reading and filtering methods tested.

To run these unit tests use the command:

``` bash
python Benchmarking/FileRead/verifyFileRead.py
```

## Results 
After all tests have been run, the read and filter times recorded can be found in [`Results/ReadTimes`](../../Results/ReadTimes/).
All results use the naming convention: `<dataset-name>_<filter-approach>_time.csv` and contain time values recorded in seconds.
