# This script contains classes for managing and updating vcf data plots 
import numpy as np

from allel import GenotypeArray as GTArr

# Constants used to index a VCF dictionary
CHROM = 'variants/CHROM'
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
        max_vars = 5000
        max_samples = 300

        vcf_data[SAMPLES] = vcf_data[SAMPLES][:max_samples]
        vcf_data[DATA] = vcf_data[DATA][:max_vars,:max_samples,]
        vcf_data[REF] = vcf_data[REF][:max_vars]
        vcf_data[ALT] = vcf_data[ALT][:max_vars]
        vcf_data[ID] = vcf_data[ID][:max_vars]
        vcf_data[POS] = vcf_data[POS][:max_vars]
        
        # ------------------------
        self.data = vcf_data
        self.gt_data = GTArr(self.data[DATA])
        self.n_samples = len(vcf_data[SAMPLES])
        self.n_variants = len(vcf_data[ID])

        # clear pre-constructed arrays
        self._zygos = None
        self._refs = None
        self._alts = None
        self._pos = None

    # Returns a matrix of zygosities for each sample variant.
    # 0 = no mutation, 1 = heterozygous, 2 = homozygous mutation, -1 = no-data
    def get_zygosity(self):
        """Returns an _`int`_ matrix of zygosities for each sample variant.\\
        0 = no mutation\\
        1 = heterozygous mutation\\
        2 = homozygous mutation\\
        -1 = no-data
        """
        if self._zygos is None: # zygosity not pre-computed
            gt_data = self.gt_data
            self._zygos = gt_data.is_hom_alt()*2 + gt_data.is_het()*1 + gt_data.is_missing()*(-1)
        return self._zygos.transpose()[::-1,:] # Flip order so that first entry is on the top
    
    # Returns a list indicating the nucleotide type of ref sequences
    # 0 = multi-nucleotide, -1 is no-data
    def get_ref(self):
        """Returns a `list` indicating the nucleotide type of the reference (`REF`) sequence.\\
        0 = multiple-nucleotides\\
        -1 = no-data
        """
        if self._refs is None:
            self._refs = alleles_to_numbs(self.data[REF])
        return self._refs

    def get_alt(self):
        if self._alts is None:
            self._alts = np.array([alleles_to_numbs(alts) for alts in self.data[ALT]])
            filter_mask = np.array([np.max(self._alts,axis=0) >= 0][0]) # filter out empty columns
            self._alts = self._alts[:,filter_mask].transpose()[::-1,:] # Put samples on the rows in descending order
        return self._alts
    
    def get_pos(self):
        """Returns an array of chromosome positions in acsending order.
        """
        if self._pos is None:
            self._pos = np.array(self.data[POS]) 
            self._pos = self._pos.sort_values(by=[POS], ascending=True)
        return self._pos

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
