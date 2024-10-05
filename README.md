# Genome Visualiser

## Quick Build and Run
To build the genome visualizer app use the command:
```bash
bash build.sh
```
> [!NOTE]
> This command will automatically set install all required Python librates to `.venv/` and a bcftools build to `src/assets/bin/`.

After the build is completed the app executable can be run using:
```bash
dist/app/Genome\ Visualizer.exe 
```
To run un-packaged Python scripts activate `.venv` and run the command:
```bash
python src/app.py
```
> [!TIP]
> If you have run `build.sh` the `.vevn/` directory will have been created and can be activated using:
> ```bash 
> source .venv/bin/activate # On Linux/MacOS/Unix
> ```
> or 
> ```bash
> source .venv/Script/activate # On Windows
> ```
> If `build.sh` has not been run, follow the [setup instructions](#make-the-virtual-environment) to create a new venv.


## Requirements
The visulsier app requires the following to be configured, run, and packaged:
- [Python](https://www.python.org/downloads/) v3.12.2+
- [pip](https://pypi.org/project/pip/) v24.0+
- gcc compiler with [GNU make](https://www.gnu.org/software/make/) OR [bcftools](https://www.htslib.org/download/) v1.20+ pre-installed on system.
- Pyhon [virtual environment](https://docs.python.org/3/library/venv.html) (venv) and bcftools install configured according to the [setup instructions](#Setup).
- All pre-requisites for the (automatically installed) python libraries listed in [`requirements.txt`](requirements.txt). 

> [!TIP]
> If using Windows [MSYS](https://www.msys2.org/), a Windows native (non-posix) version of GNU make may be installed with the command `mingw32-make`.
> This can be used on Windows systems if the regurlar `make` command does not work.

> [!IMPORTANT]
> On some Unix/Unix-like systems (Linux, MacOS) Python v3+ must be accessed using `python3` instead of `python`. 
> In the case please use `python` instead of `python3` for all commands listed below to ensure that scripts are executed with Python v3.x.


## Setup 
The aplication must be run in an active [virtual environment](https://docs.python.org/3/library/venv.html) (venv) with the required libraies installed. A build of [bcftools](https://www.htslib.org/download/) must also be configured.
### Make the Virtual Environment
To create a [venv](https://docs.python.org/3/library/venv.html) in the `.venv/` directory;  activate it; and install all required python libraries use one of the following sets of (operating system dependant) bash commands:
#### Build for Linux/MacOs and other Unix-like systems:
```bash
python3 -m venv .venv                 # Create venv in .venv/ directory.
source .venv/bin/activate          # Activate venv.
pip install -r requirements.txt    # Install requirments.
```
#### Build for Windows:
```bash
python -m venv .venv                 # Create venv in .venv/ directory.
source .venv/Scripts/activate     # Activate venv.
pip install -r requirements.txt   # Install requirments.
```

### Install Bcftools 
A build of bcftools to search and index files. This can either be a [local build](#Local-build) or a [pre-existing install](#Existing-build) configured as an environmental path variable. If you intend to build and package the app as an executable a local build is strongly recommended.
#### Local build
A local build of bcftools can be automatically compiled and installed in the `src/assets/bin/` directory with:
```bash
python build_bcftools.py          # Replace python with python3 if required.
```
> [!TIP]
> If this above method failes, the bcftools sourc code can be downloded [here](https://www.htslib.org/download/) and manunally compiled.
> The executable must be copied to `src/aseerts/bin/` after compliation.

#### Existing build
To use a pre-existing install of bcftools set `local = false` in [`config.toml`](config.toml).

> [!WARNING]
> This will only work if bcftools ins accesable as an environkental veirbale.
>
> To check this use the command:
> ```bash
> bcftools --version
> ```

> [!CAUTION]
> If you with to build and distribute the app as an executable a [local build](#Local-build) must be used.

## Run the App
To run the app user the command:
```bash
python src/app.py         # Replace python with python3 if required.
```

## Package the App
To package the app as an executable use the command:
```bash
pyinstaller app.spec 
```



## Fetures
`Version 1.0` of the Genome Visualiser Application supports basic functionality for visualising `.vcf` and `.vcf.gz` files. Unfortunately `.bcf` files are not supported for visualisation. Version 1.0 is best suited for initial Usability Testing, alowing developers to understand which features of the visualiser need to be further developed and improved in future App releases.

## `Version 1.0` Features:
- [x] User specified data subset management
- [x] Input validation for acceptable VCF file formats

#### _Visualization_:
- [x] Reference and alternate genome nucleotide-encoded sequences
- [x] Zygosity colormap 
- [x] Mutation count-frequence and density histograms
- [x] An exploratory macro-view of the genome positions as a "heatmap"

**Dataset subset selection using any combination of the following**:
- [x] Inputting the range of genome positions shown 
- [x] Inputting a range of min and max sample quality values

**Sorting the genome dataset by**:
* [Default] Position (lowest to highest)
* Quality (high to lowest)
