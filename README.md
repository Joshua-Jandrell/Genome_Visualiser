# Genome_Visualiser

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
