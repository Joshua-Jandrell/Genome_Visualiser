# This script contains classes for managing and updating vcf data plots 
import numpy as np
import allel as allel
from allel import GenotypeArray as GTArr
from pandas import DataFrame

from enum import Enum

class SortMode(Enum):
    BY_POSITION=0,
    BY_QUALITY=1,
    BY_POPULATION = 2,
     
    
# Constants used to index a VCF dictionary
CHROM = 'variants/CHROM'
SAMPLES = 'samples'      ##'Pop-tag+numbers' <<< (what are the numbers?)
DATA = 'calldata/GT'    #######Should rename, because this gets genotype pairs/matrix, yeah???   GTDATA  ??
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
    def __init__(self, vcf_data:dict, df:DataFrame) -> None:
        
        self.df = df    ####TODO TypeError: VcfDataWrapper.__init__() missing 1 required positional argument: 'df'
        # # Make data into a (pandas?) dataframe ^^^^^ ??????
        # df = al.vcf_to_dataframe(TEST_FILE)  <<<from vcfTest... idk if this helps
        
        
        self.filtered_df = None
       
        # Tmp data size constriants
        # TODO REMOVE THESE
        max_vars = 5000
        max_samples = 300

        vcf_data[SAMPLES] = vcf_data[SAMPLES][:max_samples]   #samples is the number of people
        vcf_data[DATA] = vcf_data[DATA][:max_vars,:max_samples,]
        vcf_data[REF] = vcf_data[REF][:max_vars]
        vcf_data[ALT] = vcf_data[ALT][:max_vars]
        vcf_data[ID] = vcf_data[ID][:max_vars]
        vcf_data[POS] = vcf_data[POS][:max_vars]
        vcf_data[QUAL] = vcf_data[QUAL][:max_vars]
        
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
        
        self.first_pos, self.last_pos = self.get_file_pos_range()
        self._pop_tag = None
        
        # Default range of quality scores in a .vcf file:
        self.first_qual=0
        self.last_qual=100
        
        #Default setting: don't sort by quality
        self.sort_mode = SortMode.BY_POSITION

    # Returns a matrix of zygosities for each sample variant.
    # 0 = no mutation, 1 = heterozygous, 2 = homozygous mutation, -1 = no-data
    def get_zygosity(self):
        """Returns an _`int`_ matrix of zygosities for each sample variant.\\
        0 = no mutation\\
        1 = heterozygous mutation\\
        2 = homozygous mutation\\
        -1 = no-data
        """
        gt_data = self.gt_data
        self._zygos = gt_data.is_hom_alt()*2 + gt_data.is_het()*1 + gt_data.is_missing()*(-1)
        return self._zygos   #.transpose()[::-1,:] # Flip order so that first entry is on the top
    
    # Returns a list indicating the nucleotide type of ref sequences
    # 0 = multi-nucleotide, -1 is no-data
    def get_ref(self):
        """Returns a `list` indicating the nucleotide type of the reference (`REF`) sequence.\\
        0 = multiple-nucleotides\\
        -1 = no-data
        """
        self._refs = alleles_to_numbs(self.data[REF])
        return self._refs

    def get_alt(self):
        self._alts = np.array([alleles_to_numbs(alts) for alts in self.data[ALT]])
        filter_mask = np.array([np.max(self._alts,axis=0) >= 0][0]) # filter out empty columns
        self._alts = self._alts[:,filter_mask].transpose()[::-1,:] # Put samples on the rows in descending order
        return self._alts

    def get_pos(self):
        """Returns an array of chromosome positions, for plotting."""
        df = self.__get_filtered_df()
        return df[POS].to_numpy()
    
    def get_file_pos_range(self):
        """Returns max possible range of genome sequence positons."""
        self.df = self.df.sort_values(by=[POS], ascending=True)
        
        min_pos = self.df[POS].iloc[[0]]
        max_pos = self.df[POS].iloc[[-1]]
        return(min_pos, max_pos)
    
    def set_pos_range(self, min_pos:int, max_pos:int):
        """Sets the range of nucleotide positions on the reference genome the user wants to view."""
        self.first_pos = min_pos
        self.last_pos = max_pos
        self.filtered_df =  None
    
    def set_qual_range(self, min_qual:int, max_qual:int):
        """Sets the range of nucleotide positions on the reference genome the user wants to view."""
        self.first_qual = min_qual
        self.last_qual = max_qual
        self.filtered_df =  None
        
    def set_population_tag(self, pop_target:str):
        """Sets the the tag to look for in the variant samples the user wants to view. """
        self._pop_tag = pop_target
        
    def get_population_zygosity(self):
        """Returns an _`int`_ population matrix of zygosities for the sample variants, based on an input population tag.\\
            0 = no mutation\\
            1 = heterozygous mutation\\
            2 = homozygous mutation\\
            -1 = no-data
            """
        #Find population-tag samples in all 'samples' data:
                #  _pop_tag (== target = "NA")     <<<< set by `set_population_tag()`
        population_tag_samples = [self._pop_tag in eg for eg in self.data[SAMPLES]]    #####Should pop-tag be public or private??
        
        # Get zygosity that only has the "population-tag" from the vcf dataframe:
        zygosity = allel.GenotypeArray(self.data[DATA])[self.df.index,:]
        population_zygos = zygosity[:,population_tag_samples]
        self._zygos = population_zygos
        population_samples = self.data[SAMPLES][population_tag_samples]         ###this should be given to... is this used???
        
        return self._zygos

    def __get_filtered_df(self)->DataFrame:
        """Applies all filters and returns a dataframe containing only the desired values."""
        if isinstance(self.filtered_df, DataFrame): return self.filtered_df
        new_df = self.df
        
        # filter by position range:
        min,max = self.get_file_pos_range()
        if self.first_pos > min or self.last_pos < max:
            new_df = select_by_pos(new_df,self.first_pos, self.last_pos)
            
        #select by quality range:
        if self.first_qual > 0 or self.last_qual < 100:
            new_df = select_by_qual(new_df,self.first_qual, self.last_qual)
        
        #sort by quality
        if self.sort_mode is SortMode.BY_QUALITY:
            new_df = sort_qual(new_df)
            
        #sort alphabetically by population
        if self.sort_mode is SortMode.BY_POPULATION:
            new_df = sort_popualtion(new_df)
    
        return new_df        
    
    def set_sort_by_position(self):
        return self.sort_mode == SortMode.BY_POSITION
    
    def set_sort_by_qual(self):
        return self.sort_mode == SortMode.BY_QUALITY

    def set_sort_by_population(self):
       return self.sort_mode == SortMode.BY_POPULATION
    
    

    # def filter_ref_variant_length(self):  #Scott didn't think this was necessary
    #     return

    # def filter_zygosity_type(self):   #See in zygosityOption
    #     return
    
    # def filter_nucleotide_type(self):
    #     return
   

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

def select_by_pos(df: DataFrame, first, last)-> DataFrame:
    return df[df[POS].between(first, last, inclusive = 'both')]

def select_by_qual(df: DataFrame, first, last)-> DataFrame:
    return df[df[QUAL].between(first, last, inclusive = 'both')]

def sort_qual(df:DataFrame):
    return df.sort_values(by=[QUAL], descending=True)

def sort_popualtion(df:DataFrame):
    return df.sort_values(by=[SAMPLES], ascending=True)