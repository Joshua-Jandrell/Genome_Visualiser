# This script contains classes for managing and updating vcf data plots 
from typing import Literal
import numpy as np
import allel as al
from allel import GenotypeArray as GTArr
from pandas import DataFrame

from enum import IntEnum

class SortMode(IntEnum):
    BY_POSITION=0,
    BY_QUALITY=1,
    BY_POPULATION=2,
     
    
# Constants used to index a VCF dictionary
CHROM = 'variants/CHROM'
SAMPLES = 'samples'      ##'Pop-tag+numbers' <<< (what are the numbers?)
DATA = 'calldata/GT'    #######Should rename, because this gets genotype pairs/matrix, yeah???   GTDATA  ??
ID = 'variants/ID'
REF = 'variants/REF'
ALT = 'variants/ALT'
POS = 'variants/POS'
QUAL = 'variants/QUAL'

CASES = 'samples/cases'
CTRLS = 'samples/ctrls'


S_KEYS = [SAMPLES, CASES, CTRLS]
"""Data dict fields which run along the s direction."""

V_KEYS = [CHROM, ID, REF, ALT, POS, QUAL]
"""Data dict views which align with variant."""

DW_S_KEYS = [SAMPLES, CASES, CTRLS]
DW_V_KEYS = [ALT]
DW_DF_KEYS = [CHROM, ID, REF, POS, QUAL]
 


# Used to get nucleotide number
NUCLEOTIDE_DICT = {
    "A":1,
    "C":2,
    "G":3,
    "T":4
}

# Conatins vcf query data and returns it in various formats
class VcfDataWrapper:
    def __init__(self, vcf_data:dict, df:DataFrame, cases:list[str]=[], ctrls:list[str]=[]) -> None:

        # TPDOD Construct a pandas datafram form dict data 

        self._data = {key:vcf_data[key] for key in DW_S_KEYS+DW_V_KEYS+[DATA] if key in vcf_data.keys()}
        self.set_case_ctrl(cases=cases, ctrls=ctrls)

        # Make pandas data frame
        df_dict = {key.strip('variants/'):vcf_data[key] for key in DW_DF_KEYS if key in vcf_data.keys() and key != ALT}
        self._df = DataFrame(df_dict)
            
              

        self.first_pos, self.last_pos = self.get_file_pos_range()
        self._pop_tag = None
        
        self.mutation_prob = None
        # Default range of quality scores in a .vcf file:
        self.first_qual=0
        self.last_qual=100        
        #Default setting: don't sort by quality
        self.sort_mode:SortMode = SortMode.BY_POSITION

        self._df_filtered = False
        self._dict_filtered = False       

    # Returns a matrix of zygosities for each sample variant.
    # 0 = no mutation, 1 = heterozygous, 2 = homozygous mutation, -1 = no-data

    def slice_v(self, mask:list[bool], data:dict|None = None, in_place:bool = True)->dict:
        """Slice all data that aligns with variants according to the given bool mask."""
        if data is None:
            data = self._data

        # if len(mask) != len(data[POS]):
        #     raise ValueError("Data mask does not match length of variants")
        
        if in_place:
            new_data = data
        else:
            new_data={}
        for key in V_KEYS:
            if key in data.keys():
                new_data[key] = data[key][mask]

        # Special case for callset data 
        new_data[DATA] = data[DATA][mask,:]

        return new_data

    def slice_s(self, mask:list[bool], data:dict|None = None, in_place:bool = True)->dict:
        """Slice all data that aligns with samples according to the given bool mask."""
        if data is None:
            data = self._data
        # if len(mask) != len(data[SAMPLES]):
        #     raise ValueError("Data mask does not match length of samples")
        if in_place:
            data = new_data
        else:
            new_data = {}
        for key in S_KEYS:
            if key in data.keys():
                new_data[key] = data[key][mask]
        # Special case for callset data 
        new_data[DATA] = self._data[DATA][mask,:]

        return new_data
        
    def get_zygosity(self, split=True):
        """Returns an _`int`_ matrix of zygosities for each sample variant.\\
        0 = no mutation\\
        1 = heterozygous mutation\\
        2 = homozygous mutation\\
        -1 = no-data\\
        NOTE If `split` is set to `True` 
        """
        gt_data = self.__get_filtered_genotype_array()
        self._zygos = gt_data.is_hom_alt()*2 + gt_data.is_het()*1 + gt_data.is_missing()*(-1)
        return self._zygos   #.transpose()[::-1,:] # Flip order so that first entry is on the top
    
    def get_mutation_probability(self):
        """ Returns an array of probabilities (0 - 100 %) for any mutation (homo or hetero) occuring in a position, based on the queried data displayed.\\        
        """
        gt_data = self.__get_filtered_genotype_array()
        # Frequency of homzygos per position
        zygo_total_probability = (((gt_data.is_hom_alt()*2).sum(axis=1)
                                +(gt_data.is_het()*1).sum(axis=1))/(self.get_n_samples()*2))*100
        return zygo_total_probability
    
    def get_homozygous_probability(self, split:bool = False, format:Literal['percentage', 'fraction']='percentage'):
        """ Returns an array of probabilities (0 - 100 %) for a homozygous mutation occuring in a position, based on the queried data displayed.
        """
        mult = 1
        if format == 'percentage':
            mult = 100

        gt_data = self.__get_filtered_genotype_array()

        if split:
            n_cases = self.get_n_cases()
            n_ctrls = n_cases - self.get_n_variants()
            ctrl_data = gt_data[:,:n_ctrls]
            case_data = gt_data[:,n_ctrls:]
            return [(((ctrl_data.is_hom_alt()*1).sum(axis=1))/(self.get_n_samples()))*mult,
                    (((case_data.is_hom_alt()*1).sum(axis=1))/(self.get_n_samples()))*mult]

        # Frequency of homzygos per position
        zygo_homo_probability = (((gt_data.is_hom_alt()*1).sum(axis=1))/(self.get_n_samples()))*mult
        return zygo_homo_probability
    
    def get_heterozygous_probability(self, split:bool = False, format:Literal['percentage', 'fraction']='percentage'):
        """ 
        Returns an array of probabilities (0 - 100 %) for a heterozygous mutation occuring in a position, based on the queried data displayed.\\
        If `split` is set to true then a 2D list of cases and control will be returned 
        """
        mult = 1
        if format == 'percentage':
            mult = 100
        gt_data = self.__get_filtered_genotype_array()
        if split:
            n_cases = self.get_n_cases()
            n_ctrls = n_cases - self.get_n_variants()
            ctrl_data = gt_data[:,:n_ctrls]
            case_data = gt_data[:,n_ctrls:]
            return [(((ctrl_data.is_het()*1).sum(axis=1))/(self.get_n_samples()))*mult,
                    (((case_data.is_het()*1).sum(axis=1))/(self.get_n_samples()))*mult]

        # Frequency of homzygos per position
        zygo_hetero_probability = (((gt_data.is_het()*1).sum(axis=1))/(self.get_n_samples()))*mult
        return zygo_hetero_probability
    
    def _split_mat_by_cases(self,arr:np.matrix)->tuple[np.matrix, np.matrix]:
        """Split the given data into control data and case data."""
        n_ctrls = self.get_n_ctrls()
        ctrl_data = arr[:,:n_ctrls]
        case_data = arr[:,n_ctrls:]
        return ctrl_data, case_data

    # Returns a list indicating the nucleotide type of ref sequences
    # 0 = multi-nucleotide, -1 is no-data
    def get_n_samples(self):
        return len(self.get_samples())
    def get_n_variants(self):
        return len(self.get_pos())
    def get_n_alts(self):
        return self.get_alts().shape[1]
    def get_samples(self):
        return self.__get_filtered_samples()
    
    def get_chromosome(self):
        return self.__get_filtered_df()["CHROM"].to_numpy()
    
    def get_n_cases(self):
        return sum(self.__get_filtered_data()[CASES])
    def get_n_ctrls(self):
        return sum(self.__get_filtered_data()[CTRLS])
    
    def get_ref_ints(self):
        """Returns a `list` indicating the nucleotide type of the reference (`REF`) sequence.\\
        0 = multiple-nucleotides\\
        -1 = no-data
        """
        return alleles_to_numbs(self.get_ref())
        #return self._refs
    
    def get_ref(self):
        df = self.__get_filtered_df()
        return df["REF"].to_numpy()
    
    def get_alts(self):
        alts =  self.__get_filtered_data()[ALT]
        mask = [any(col != "") for col in alts.T]
        return alts[:,mask]
    
    def get_alt_int(self):
        _alts = np.array([alleles_to_numbs(alts) for alts in self.get_alts()])
        return _alts

    def get_pos(self):
        """Returns an array of chromosome positions, for plotting."""
        df = self.__get_filtered_df()
        return df["POS"].to_numpy()
    
    def get_file_pos_range(self):
        """Returns (min, max) possible range of genome sequence positons."""
        self._df = self._df.sort_values(by=["POS"], ascending=True)   ### All the 'by=...' stuff needs: ""
        
        min_pos = self._df["POS"].iloc[0]
        max_pos = self._df["POS"].iloc[-1]
        return(min_pos, max_pos)
    
    def set_pos_range(self, min_pos:int, max_pos:int):
        """Sets the range of nucleotide positions on the reference genome the user wants to view."""
        self.first_pos = min_pos
        self.last_pos = max_pos
        self._dict_filtered = False
        self._df_filtered = False
    
    def set_qual_range(self, min_qual:int, max_qual:int):
        """Sets the range of nucleotide positions on the reference genome the user wants to view."""
        self.first_qual = min_qual
        self.last_qual = max_qual
        self._dict_filtered = False
        self._df_filtered = False
        
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
        population_tag_samples = [self._pop_tag in eg for eg in self._data[SAMPLES]]
        
        # Get zygosity that only has the "population-tag" from the vcf dataframe:
        zygosity = al.GenotypeArray(self._data[DATA])[self._df.index,:]
        population_zygos = zygosity[:,population_tag_samples]
        self._zygos = population_zygos
        population_samples = self._data[SAMPLES][population_tag_samples]         ###this should be given to... is this used???
        
        return self._zygos
    
    def get_cases(self):
        return self.__get_filtered_data()[CASES]
    
    def get_ctrls(self):
        return self.__get_filtered_data()[CTRLS]
    
    def set_case_ctrl(self, cases:list[str], ctrls:list[str]=[]):
        """
        Set the case and control samples for the dataset
        """

        # ensure that there is not data in both cases and controls
        cases = [c for c in cases if c not in ctrls]

        # Make case and control arrays
        if len(cases) > 0:
            self._data[CASES] = np.array([s in cases for s in self._data[SAMPLES]])
            if len(ctrls) == 0:
                self._data[CTRLS] = np.array([not c for c in self._data[CASES]])
        
        if len(ctrls) > 0:
            self._data[CASES] = np.array([s in ctrls for s in self._data[SAMPLES]])
            if len(cases) == 0:
                self._data[CASES] = np.array([not c for c in self._data[CTRLS]])

        if len(cases) == 0 and len(ctrls) == 0:
            self._data[CASES] = np.array([True for s in self._data[SAMPLES]])
            self._data[CTRLS] = np.array([False for s in self._data[SAMPLES]])

        self._dict_filtered = False


    def __get_filtered_df(self)->DataFrame:
        """Applies all filters and returns a dataframe containing only the desired values."""


        if self._df_filtered:
            return self._df
        
        new_df = self._df
        
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
        elif self.sort_mode is SortMode.BY_POSITION:
            new_df = sort_position(new_df)
            
        #sort alphabetically by population
        if self.sort_mode is SortMode.BY_POPULATION:
            new_df = sort_popualtion(new_df)

        self._df = new_df
        self._df_filtered = True
    
        return new_df
    
    def __get_filtered_data(self)->dict:
        if self._dict_filtered:
            return self._data
        
        df = self.__get_filtered_df()
        
        self._data = self.slice_v(df.index, self._data, in_place=True)
        self._data = self.__sort_by_case_ctrl(data=self._data, in_place=True)
        self._dict_filtered = True
        return self._data

    def __get_filtered_genotype_array(self, split:bool = False)->GTArr|list[GTArr]:
        """Find the filtered genotype array."""
        data = self.__get_filtered_data()
        if split:
            n_ctrls = self.get_n_ctrls()
            return [GTArr(data[:,:n_ctrls]), GTArr(data[:,n_ctrls:])]
        return GTArr((data[DATA]))

    def __get_filtered_samples(self):
        """Find the filtered pos."""
        df = self.__get_filtered_df()
        return self._data[SAMPLES]

    
    def set_sort_by_position(self):
        self.sort_mode == SortMode.BY_POSITION
    
    def set_sort_by_qual(self):
        self.sort_mode == SortMode.BY_QUALITY

    def set_sort_by_population(self):
        self.sort_mode == SortMode.BY_POPULATION

    def set_sort_mode(self, mode_int:int):
        sort_mode = SortMode(mode_int)
        self.sort_mode = sort_mode
    
    def __sort_by_case_ctrl(self, data:dict|None = None, in_place:bool = True)->dict:
        if data is None:
            data = self._data
        if in_place:
            new_data = data
        else:
            new_data = {}
        
        _cases = np.array(data[CASES])
        for key in S_KEYS:
            new_data[key] = np.concat((data[key][data[CTRLS]], data[key][_cases[:]]),axis=0)

        new_data[DATA] = np.concat((data[DATA][:,data[CTRLS]], data[DATA][:,data[CASES]]),axis=1)
        return new_data

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
    return df[df["POS"].between(first, last, inclusive = 'both')]

def select_by_qual(df: DataFrame, first, last)-> DataFrame:
    return df[df["QUAL"].between(first, last, inclusive = 'both')]

def sort_position(df:DataFrame):
    return df.sort_values(by=["POS"], ascending=True)

def sort_qual(df:DataFrame):
    return df.sort_values(by=["QUAL"], ascending=False)

def sort_popualtion(df:DataFrame):
    return df.sort_values(by=['samples'], ascending=True)
