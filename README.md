# Genome Visualiser

## Quick Build and Run
To build the genome visualizer app use the command:
```bash
bash build.sh
```
> [!NOTE]
> This command will automatically install all required Python libraries to `.venv/` and a bcftools build to `src/assets/bin/`.

After the build is completed the app executable can be run using:
```bash
dist/app/Genome\ Visualizer.exe 
```
To run un-packaged Python scripts activate `.venv` and run the command:
```bash
python src/app.py
```
> [!TIP]
> If you have run `build.sh` the `.venv/` directory will have been created and can be activated using:
> ```bash 
> source .venv/bin/activate # On Linux/MacOS/Unix
> ```
> or 
> ```bash
> source .venv/Script/activate # On Windows
> ```
> If `build.sh` has not been run, follow the [setup instructions](#make-the-virtual-environment) to create a new venv.

## **Features**
`Version 2.0` of the Genome Visualiser Application supports basic functionality for visualising `.vcf`, `.vcf.gz` and `.bcf` files. Version 2.0 is best suited for Usability Testing, allowing developers to understand which features of the visualiser need to be further developed and improved in future App releases.

## `Version 2.0` Features:
- [x] User specified data subset management
- [x] Input validation for acceptable VCF file formats
- [x] Supports `.bcf` file visualisation, provided bcftools has installed sucessfully
- [x] Desktop installation with `PyInstaller`
- [x] Scripts to automatically build [bcftools](https://www.htslib.org/download/)

### _Visualization_:
- [x] Reference and alternate allele sequences (nucleotide-encoded)
- [x] Variant-Zygosity colourmap 
- [x] Variant-frequency count and density histograms
- [x] Variant probability heatmap
- [x] Comparion of variant proportions between case and control samples
- [x] Case and control samples colourmap
- [x] Exploratory view of allele position as a heatmap

**Dataset subset selection using any combination of the following**:
- [x] Inputting the range of genome positions to be visualised
- [x] Inputting a range of min and max sample quality values
- [x] Selecting a `.csv`, `.txt` and `.tsv` file to tag samples as either a case or a control sample

### `Version 2.0 no longer supports:`
* Sorting - by default the variants are sorted by position (lowest to highest).


## Requirements
The app requires the following to be already setup in order to be configured:
- [Python](https://www.python.org/downloads/) v3.12.2+
- [pip](https://pypi.org/project/pip/) v24.0+
- gcc compiler with [GNU make](https://www.gnu.org/software/make/) OR [bcftools](https://www.htslib.org/download/) v1.20+ pre-installed on system.
- Python [virtual environment](https://docs.python.org/3/library/venv.html) (venv) and bcftools installed and configured according to the [setup instructions](#Setup).
- All pre-requisites for the (automatically installed) python libraries listed in [`requirements.txt`](requirements.txt). 

> [!TIP]
> If using Windows [MSYS](https://www.msys2.org/), a Windows native (non-posix) version of **GNU make** may be installed with the command `mingw32-make`.
> This can be used on Windows systems if the regular `make` command does not work.

> [!IMPORTANT]
> On some Unix/Unix-like systems (Linux, MacOS) Python v3+ must be accessed using `python3` instead of `python`. 
> In this case, please use `python` instead of `python3` for all commands listed below to ensure that scripts are executed with Python v3.--- .


## **Setup**
The application must be run in an active [virtual environment](https://docs.python.org/3/library/venv.html) (venv) with the required libraries installed. A build of [bcftools](https://www.htslib.org/download/) must also be configured.

### Make the Virtual Environment
To create a [venv](https://docs.python.org/3/library/venv.html) in the `.venv/` directory:
* Activate it and then,
* Install all required python libraries using one of the following sets of bash commands (which are operating system dependant) :
#### Build for _Linux/MacOS_ and other Unix-like systems:
```bash
python3 -m venv .venv                 # Create venv in .venv/ directory.
source .venv/bin/activate          # Activate venv.
pip install -r requirements.txt    # Install requirements.
```
#### Build for _Windows_:
```bash
python -m venv .venv                 # Create venv in .venv/ directory.
source .venv/Scripts/activate     # Activate venv.
pip install -r requirements.txt   # Install requirements.
```

### Install Bcftools 
A build of bcftools to search and index files. This can either be a [local build](#Local-build) or a [pre-existing install](#Existing-build) configured as an environmental path variable. If you intend to build and package the app as an executable a local build is strongly recommended.

#### Local build
A local build of bcftools can be automatically compiled and installed in the `src/assets/bin/` directory with:
```bash
python build_bcftools.py          # Replace python with python3 if required.
```
> [!TIP]
> If this above method fails, the bcftools source code can be downloaded [here](https://www.htslib.org/download/) and manually compiled.
> The executable must be copied to `src/assets/bin/` after compilation.
> 
#### Existing build
To use a pre-existing install of bcftools set `local = false` in [`config.toml`](config.toml).

> [!WARNING]
> This will only work if bcftools is accessible as an environmental variable.
  > To check if it is, use the command:
> ```bash
> bcftools --version
> ```

> [!CAUTION]
> If you wish to build and distribute the app as an executable: a [local build](#Local-build) must be used.

## Running the App
To run the app user the command:
```bash
python src/app.py         # Replace python with python3 if required.
```

## Example Data for Visualisation
If you do not have access to `.vcf.gz` files to use or test the app's visualisation with, you can download some publicly available data which will load 3 `.vcf.gz` files into the `Data` directory along with 6 case/control files (3 case/control files that were used to obtain the results the [`Benchmarking/`](Benchmarking) tests and 3 randomly generated case/control files for experimentation). To download this public data use the following command:
 ```bash

bash get_data.sh

```

### Cases & Controls file format
Case files can be used to specify which samples are cases (represent the sub-population/individuals who are being researched for the presence of a variant or physical trait) and which are controls (sample who have the specific  variant or trait that being researched).It can be useful to split and sort samples into cases and controls for comparative visualisation.
> Case files can be `.txt`, `.tsv`, or `.csv` files which define if a sample is a case or a control.

### General Cases/Controls file format
A cases/control file should contain two columns: one is a list of all samples in the `.vcf` dataset, the other is a list of Boolean values [`True` or `False`] where `True` indicates that the corresponding sample is a **case**.
For example,
A case file for a dataset with 4 samples: `s_1`, `s_2`,  `s_3`, and `s_4`;  looks as follows in tsv format:
```tsv

s_1        False

s_2        True

s_3        False

s_4        True

```

In the above example file, `s_2` is a case while `s_1` and `s_3` are controls.

### Alternative Cases/Controls file format
Sometimes it is easier to list only the case samples. This can be done by providing a single column which lists only the cases samples:
```tsv

s_2

s_3

```

The above case file shows that `s_2` and `s_3` are cases while all other samples are controls.

## Packaging the App
To package the app as an executable use the command:
```bash
pyinstaller app.spec 
```

## App Optimisation Tests 
The [`Benchmarking/`](Benchmarking) folder contains scripts used for tests. For more  details regarding testing, see the testing [`README`](Benchmarking/README.md).

## Running Unit Tests 
To download all required testing files and run unit tests use the command
```bash

run_tests.sh

```

If the above data has already been downloaded, you can instead use the command:
```bash

python -m unittest discomver test/

```
