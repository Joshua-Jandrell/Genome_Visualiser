#  Filter and Read Bechnmarking: Bcftools vs Scikit-allel:

This disrectory contains files used to test the time taken to read and filter `.vcf` files using different approches.

Each approch usese [bcftools](https://github.com/samtools/bcftools) and/or [scikit-allel](https://github.com/cggh/scikit-allel) to filter genomic datasets stored in `.vcf.gz` files and read their contents into a Python data structre. 

## Run tests
The tests can be run (from the repo root) with the following command:

``` bash
python Benchmarking/FileRead/timeFileReading.py 
```

> [!IMPORTANT]
> These tests require a build bcftools to run.
> Either [build a local version](../../README.md#local-build) of bcftools or update the `bcftools` field in [`data_config.toml`](data_config.toml) to refferacne and exiting install of bcftools.

> [!NOTE]
> These tests must be run with the `.venv` (containing sckikit-allel) activated.

> [!NOTE]
> When running these tests data files will be downloaded and saved to the `./Data` direcotry.

## Methadology
The times taken to perform filtering and reading operation are recorded using three different apporches: [bcftools filtering](#bcftools-filtering), [scikit-allel filtering](#scikit-allel-filtering), and [hybrid filtering](#hybrid-filtering). 

Each filtering apporch ([detailed below](#Filtering-approaches)) is broken into several sub-operations (detailed below) that are timed individually to idneify bottelnecks. Every sub-operation is repeated 10 times and averaged to impove reliabaility.

In general, each filtering approch reads a genomic dataste (stored in a `.vcf.gz.` file) and selects variants in the region of `10000-11000` (on the first chromosome listed) while exclauding variants with a quaility less than `25`.
The dataset is split into two subsets: one for case samples (listed in a seperate `.tsv` file) and one for control sampless (all othe samples not listed in the `.tsv`).
Each subset is represented by a seperate Python dictinary (`dict`).


### Test data
Three publically-avaible genomic datasets: `afr.vcf.gz` (150 MB), `afr-small.vcf.gz` (98 KB), and `med.vcf.gz` (730 KB) are used during speed tests.
Each dataset is accompanied by a randomly-generated case `.tsv` file with the namining convenation: `<dataset-name>.case.tsv`.

Although case (`.tsv`) files are randomly generated; the same case file is used for all three apporches to ensure that results are comprable.

> [!TIP]
> All files used for testing will be automatically downlaoded when either `Benchmarking/FileRead/timeFileReading.py ` or `Benchmarking/FileRead/verifyFileRead.py` is run.
> Files can also be downlaoded with the command: `python Benchmarking/FileRead/fetchData.py`.

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
