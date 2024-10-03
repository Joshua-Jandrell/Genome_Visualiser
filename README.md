# Genome_Visualiser

## Requirements
- python 3.12.2 or later
- pip 24.0 or later
- bcftools

> [!NOTE]
> On some Linux distributions python 3 must be accessed using `python3` instead of `python`. 
> In the case use `python` instead of `python3` for all commands.


## Setup 
### Virtual Environment
A python [virtual environment](https://docs.python.org/3/library/venv.html) (venv) with all required libraries, listed in [`requirements.txt`](requirements.txt), must be created and activated in order to build or run the application.

To create a new venv in the `~.venv/` directory use the consol command:
```bash
python venv .venv
```
---
After the venv has been created it must be activated.

For MacOS or Linux use:
```bash
source .venv/bin/activate
```
For widows used:
```bash
source .venv/Scripts/activate
```
---
To install all required dependencies to the venv with [pip](https://pypi.org/project/pip/) use the command:
```bash
pip install -r requirements.txt 
```
## Run
To run the visualizer application with python use the command:
```bash
python src/app.py
```
> [!NOTE]
> The Application will only run if a venv has been created and activated.

## Build 
To build an executable application is:
```bash
pyinstaller src/app.py
```




# --- OLD READ ME ---
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


## Requirments
To run the genome visuliser python3 and the required libraries mus be installed. To install these requiremnts in a virtual envrioments (in the directry `.venv`) run the command below:
```bash
bash make_venv.sh
```
❗NOTE: Some required librbaies like scikit-allele have further requirements which must be satesfied.

## Running
In order run the genome visuliser use the command:
```bash
.venv/Scripts/python.exe ./GVDashboard/app.py
```
❗ NOTE there many be issues with reltive script impots, to avoid this please navgate to `./GVDashboard/`.
