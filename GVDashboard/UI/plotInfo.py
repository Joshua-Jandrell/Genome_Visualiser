# This script contains classes for managing and updating vcf data plots 
import numpy as np

from allel import GenotypeArray as GTArr

from matplotlib.figure import Figure as Figure
from matplotlib.axes import Axes as Axes
from matplotlib import colors
from matplotlib.gridspec import GridSpec as GridSpec

# Constants used for indexing VCF ductionary
SAMPLES = 'samples'
DATA = 'calldata/GT'
ID = 'variants/ID'
REF = 'variants/REF'
ALT = 'variants/ALT'
POS = 'variants/POS'
QUAL = 'variants/QUAL'

# Used to get nucleotide number
NUCLEOTIDE_DICT = {
    "A":1,
    "C":2,
    "G":3,
    "T":4
}

# Conatins vcf query data and returns it in various formats
class VcfDataWrapper:
    def __init__(self, vcf_data:dict) -> None:

        # Tmp data size constriants
        # TODO REMOVE THESE
        max_vars = 50
        max_samples = 30

        vcf_data[SAMPLES] = vcf_data[SAMPLES][:max_samples]
        vcf_data[DATA] = vcf_data[DATA][:max_vars,:max_samples,]
        vcf_data[REF] = vcf_data[REF][:max_vars]
        vcf_data[ALT] = vcf_data[ALT][:max_vars]
        vcf_data[ID] = vcf_data[ID][:max_vars]
        
        # ------------------------
        self.data = vcf_data
        self.gt_data = GTArr(self.data[DATA])
        self.n_samples = len(vcf_data[SAMPLES])
        self.n_variants = len(vcf_data[ID])

        # clear pre-constructed arrays
        self._zygos = None
        self._refs = None
        self._alts = None

    # Returns a matrix of zygosities for each sample variant.
    # 0 = no mutation, 1 = heterozygous, 2 = homozygous mutation, -1 = no-data
    def get_zygosity(self):
        if self._zygos is None: # zygosity not pre-computed
            gt_data = self.gt_data
            self._zygos = gt_data.is_hom_alt()*2 + gt_data.is_het()*1 + gt_data.is_missing()*(-1)
        return self._zygos.transpose()[::-1,:] # Flip order so that firs entry is on the top
    
    # Returns a list indicating the nucleotide type of ref sequences
    # 0 = multi-nucleotide, -1 is no-data
    def get_ref(self):
        if self._refs is None:
            self._refs = alleles_to_numbs(self.data[REF])
        return self._refs

    def get_alt(self):
        if self._alts is None:
            self._alts = np.array([alleles_to_numbs(alts) for alts in self.data[ALT]])
            filter_mask = np.array([np.max(self._alts,axis=0) >= 0][0]) # filter out empty columns
            self._alts = self._alts[:,filter_mask].transpose()[::-1,:] # Put samples on the rows in descending order
        return self._alts

# Converts and allele character/string to an intagetr
# 0 = multi-nucleotide, -1 = n0-data
def allele_to_numb(a:str):
    if len(a) > 1:
        return 0
    elif NUCLEOTIDE_DICT.keys().__contains__(a):
        return NUCLEOTIDE_DICT[a]
    else:
        return -1
# Converts an array of alleles to numbers
def alleles_to_numbs(alleles:np.array):
    return [allele_to_numb(a) for a in alleles]


# ------------------------------------------------------

# Colors
MUT_COLORS = colors.ListedColormap(["#00000000","#002164", "g", "y"])
ALLELE_COLORS = colors.ListedColormap(["#00000000","grey", "#29E838", "#E829D8", "#E89829", "#2979E8"])

# Boundries
VAR_MAX = 4
VAR_MIN = -1

# This class is responsible for generating vcf plots based on vcf query data
class PlotInfo:
    REF_LABEL = "Ref."
    ALT_LABEL = "Alt."
    def __init__(self,plot_ref:bool=True, plot_alt:bool=True, plot_labels:bool=True):
        self.plot_ref = plot_ref # If set to true the ref. alleles will be plotted
        self.plot_alt = plot_alt # If set true the alt. alleles will be plotted
        self.plot_labels = plot_labels

        self.mut_cols = MUT_COLORS
        self.allele_cols = ALLELE_COLORS
    
    # Plots the vcf query data stored in the given dictionary
    def plot_data(self,vcf_data:dict)->Figure:
        self.set_data(vcf_data)
        return self.make_plot()

    # Sets the plot data
    def set_data(self, vcf_data:VcfDataWrapper):
        self._data = vcf_data

    
    # Generates a mathplotlib plot 
    def make_plot(self)->Figure:

        # Determine number of sub_plots and their weights
        height_ratios = []
        n_subplots = 1

        if(self.plot_ref):
            height_ratios.append(1)
            n_subplots += 1
        if(self.plot_alt):
            height_ratios.append(self._data.get_alt().shape[0])
            n_subplots +=1 

        height_ratios.append(self._data.n_samples)

        gs = GridSpec(n_subplots, 1, height_ratios=height_ratios)

        # Create figure
        self.fig = Figure(figsize = (5, 5), dpi = 100)

        # Create main plot
        n_subplots -= 1
        self.main = self.fig.add_subplot(gs[n_subplots])

        # Create optional subplots
        if(self.plot_ref):
            n_subplots -= 1
            self.ref = self.fig.add_subplot(gs[n_subplots], sharex=self.main)
            self.make_ref_plot(self.ref)
        else:
            self.ref = None

        if(self.plot_alt):
            n_subplots -= 1
            self.alt = self.fig.add_subplot(gs[n_subplots], sharex=self.main)
            self.make_alt_plot(self.alt)
        else:
            self.alt = None
        

        self.make_zygosity_polt(self.main)
        
        # Remove spacing between plots
        self.fig.subplots_adjust(hspace=0, wspace=0)
        return self.fig
    
    # updates the plotting settings
    def configure(self,plot_ref:bool=None, plot_alt:bool=None, plot_labels:bool=None):
        if plot_ref is not None:
            self.plot_ref = plot_ref
        if plot_alt is not None:
            self.plot_alt = plot_alt
        if plot_labels is not None:
            self.plot_labels = plot_labels


        
    # Generates the data for a ref/alt variant type plot
    def make_ref_plot(self,ref_ax:Axes):
        self.make_allele_plot(ref_ax, np.matrix(self._data.get_ref()),self.REF_LABEL, self._data.data[REF])

    def make_alt_plot(self,ref_ax:Axes):
        self.make_allele_plot(ref_ax, np.matrix(self._data.get_alt()),self.ALT_LABEL,self._data.data[ALT])

    def make_allele_plot(self, axis:Axes, data:np.matrix, label:str, data_labels):
        axis.pcolor(data,linewidth=1,edgecolors="k",cmap=self.allele_cols, vmin=VAR_MIN, vmax=VAR_MAX)
        # Remove tick labels
        axis.set_xticks([])
        axis.set_yticks([])
        # Label y-axis
        axis.set_ylabel(label, rotation=0, va="center", ha="right")

        # Add annotations
        if self.plot_labels:
            for y in range(data.shape[0]):
                for x in range(data.shape[1]):
                    axis.annotate(f"{data_labels[x][y]}", 
                                  xy=(x+0.5,y+0.5),
                                  horizontalalignment='center',
                                  verticalalignment='center', 
                                  fontsize=8)

    def make_zygosity_polt(self, axis:Axes):
        axis.pcolor(np.matrix(self._data.get_zygosity()), linewidth=1,edgecolors="k", cmap=self.mut_cols, vmax=2, vmin=-1)
