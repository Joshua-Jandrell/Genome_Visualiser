# Contains classes and data that can be used to filter, query and manage datasets
import random, os
from os import path
from typing import Literal
from VCF.dataWrapper import VcfDataWrapper as DataWrapper
from .dataLoad import peek_vcf_data, read_vcf_df, read_vcf_data
from .bcftoolSys import make_dataset_file, convert

DEFAULT_VARIANTS = 5000
REGION_CMD = '-r'
INCLUDE_CMD = '-i'
# Class used to define how bcf filters should be applied
# Acts as a base class for more advanced data filters
class DataFilter_base():
    def __init__(self) -> None:
        pass

    def get_query_str(self, opt:str)->str:
        """
        Get string used to construct a bcftools query statement.\n.
        The `opt` string is the bcftools query option that this filter will be appended to.
        NOTE This function should be overridden by descendants
        """
        return ""
    def apply_to_wrapper(self,dw:DataWrapper):
        """
        Used to configure the values of a datawrapper.\n
        NOTE This function should be overridden by descendants
        """
        return dw
    
class ParamRangeFilter(DataFilter_base):
    """
    Filter used to set the range of a given column parameter.
    """
    def __init__(self, column:str, min:float|int, max:float|int) -> None:
        super().__init__()
        assert(min <= max)
        self.column_name = column
        self.min = min
        self.max = max
    def set_range(self, min:float|int|None=None, max:float|int|None=None):
        if min is not None: self.min = min
        if max is not None: self.max = max
    def get_range(self):
        return self.min, self.max
    def get_query_str(self, opt: str) -> str:
        if opt == INCLUDE_CMD:
            return f"{self.column_name}<={self.max} && {self.column_name}>={self.min}"
        return super().get_query_str(opt)
    
    
class RegionFiler(DataFilter_base):
    def __init__(self, chromosome:int=1, min:int=0, max:int=10000) -> None:
        super().__init__()
        self.chromosome=chromosome
        self.min = min
        self.max = max

    def configure(self, chromosome:int|None = None, min:int|None = None, max:int|None = None):
        if chromosome is not None:
            self.chromosome = chromosome
        if min is not None:
            self.min = min
        if max is not None:
            self.max = max

    def get_query_str(self, opt:str) -> str:
        if opt == REGION_CMD: return f"{self.chromosome}:{self.min}-{self.max}"
        return super().get_query_str(opt)
    def apply_to_wrapper(self, dw: DataWrapper):
        dw.set_pos_range(min_pos=self.min, max_pos=self.max)
    
class QualityFilter(ParamRangeFilter):
    def __init__(self, min:float=0, max:float=100):
        super().__init__(column='QUAL', min=min, max=max)
    def apply_to_wrapper(self,dw: DataWrapper):
        dw.set_qual_range(min_qual=self.min, max_qual=self.max)

def get_filter_query_str(filters:list[DataFilter_base],cmds:list[str], chr_prefix = "")->str:
    """
    Construct a bcftools style query string for the list of specified filters.
    """
    # Check for regional filtering
    query_str = ""
    if REGION_CMD in cmds:
        query_str += (" -r " + ",".join([s for s in [chr_prefix+filt.get_query_str('-r') for filt in filters] if s != '']))
    if INCLUDE_CMD in cmds:
        query_str += (" -i \"" + " && ".join([chr_prefix+filt.get_query_str('-i') for filt in filters]) +"\" ")

    return query_str



# Class used to store and apply various vcf filters
class DataSetInfo:
    POS_RANGE = 20000
    APPEND = "_subset"
    names = [] # List of all dataset names to help avoid tow datasets having the same name
    __files = []
    data_wrappers = {} # stores a list of pre-computed data wrappers 

    @classmethod
    def __make_valid_save_file_name(cls):
        """
        Crates a unique save file name for the given data set
        """
        save_file = '.' +  str(random.randint(0,999999999))
        if save_file in cls.__files: return cls.__make_valid_save_file_name()
        else:
            cls.__files.append(save_file)
            return save_file
        
    @classmethod 
    def __clear_save_file_name(cls, name):
        """
        clears the given save file name.
        """
        cls.__files.remove(name)

    def add_name(name:str):
        DataSetInfo.names.append(name)
    def clear_name(name:str, ):
        DataSetInfo.names.remove(name)
  
    def is_free_name(name:str)->bool:
        return name not in DataSetInfo.names


    def __init__(self,source_path:str|None = None,name:str|None = None, case_path:str|None="", ctrl_path:str|None="") -> None:
        
        # Flags used to see which fields must be updated 
        self.__sample_flag = False
        self.__qaul_flag = False
        self.__region_flag = False
        
        
        self.filters:list[DataFilter_base] = []
        # Add make required filters
        # NOTE this must be done before configuration
        self.__range_filter = RegionFiler()
        self.__quality_filter = QualityFilter()


        self.source_path = source_path
        self._save_name = self.__make_valid_save_file_name()
        self.__save_path__ = None
        self.__name = None # Must set name to None here so that set name can use this variable 

        # Initial region info
        self.chr = None
        self.chr_prefix=""
        self.abs_start = 1
        self.abs_end = None

        # If a path was given, use this to name the dataset 
        self.dw = None
        if name is None:
            if source_path is not None:
                name = path.basename(source_path)
            else:
                name = "New Dataset"
        self.__set__name(name)
        self.configure(source_path, name=name, case_path = case_path, ctrl_path=ctrl_path)
        if self.source_path is not None:
            self.__peak_data()
        self.get_save_path()
        self.get_dataset_name()
        #print(f"Make {self.__name}")

        # Add required filters to filter stack
        self.add_filter(self.__range_filter)
        self.add_filter(self.__quality_filter)


    def __del__(self):
        #print(f"killed {self.__name}")
        DataSetInfo.clear_name(self.__name)
        DataSetInfo.__clear_save_file_name(self._save_name)
        if self.__save_path__ is not None and os.path.isfile(self.__save_path__+".vcf.gz"):
            os.remove(self.__save_path__+".vcf.gz")

    def configure(self,
                  source_path:str|None = None,
                  filters:DataFilter_base|None = None,
                  name:str|None = None,
                  case_path:str|None = None,
                  ctrl_path:str|None = None
                  ):
        if source_path is not None and self.source_path != source_path:
            self.source_path = source_path
            self.__peak_data()
        if filters is not None: self.filters = filters
        if name is not None: self.__set__name(name)
        if case_path is not None: self.set_case(case_path)
        if ctrl_path is not None: self.set_ctrl(ctrl_path=ctrl_path)

    def add_filter(self,filter:DataFilter_base):
        self.filters.append(filter)

    def is_valid(self):
        """Returns true if the given dataset is valid and can be created
        """
        return self.source_path is not None # Assume that file type validation has already been done

    def get_source_path(self)->str|None:
        return self.source_path

    def get_save_path(self):
        if self._save_name is None:
            self._save_name = self.get_dataset_name()
        return self._save_name

    def get_dataset_name(self)->str:
        return self.__name
    
    def __set__name(self, name)->str:
        """Used internally to ensure that two datasets do not have the same name
        """
       
        # Remove old name to avoid confusion
        if self.__name is not None:
            if self.__name == name: return # Trivial case
            DataSetInfo.clear_name(self.__name)

        
        # If name is not available, append a number to name until it becomes available 
        iter = 0
        _name = name
        while not DataSetInfo.is_free_name(_name):
            iter += 1
            _name = name + f' ({iter})'

        DataSetInfo.add_name(_name) # add new name to the list 
        self.__name = _name # set name

    def __peak_data(self):
        """
        Called only when a new source file is set.\n
        This function loads in default range value by peaking at the dataset loaded and finding its chromosome and first value.
        """
        peek_info = peek_vcf_data(self.source_path, DEFAULT_VARIANTS)
        chr = peek_info['CHROM/number']
        self.abs_start = min_pos = peek_info['POS/first']
        max_pos = peek_info['POS/last']
        if peek_info['POS/at_end']:
            self.abs_end = max_pos

        self.__range_filter.configure(chromosome=chr, min=min_pos, max=max_pos)
    
    def get_data(self)->DataWrapper:
        """Returns a `VcfDataWrapper` containing the data managed by this dataset (with all filtering applied)"""
        # Pr-load vcf data using bcftools if required 
        if self.__region_flag or self.__save_path__ is None:
            query_str = get_filter_query_str(self.filters,['-r'])
            self.__save_path__ = make_dataset_file(self.source_path,
                                                   os.path.join(os.path.dirname(self.source_path),self._save_name),
                                                   query_str=query_str)
            
        # Load datawrapper
        data = read_vcf_data(self.__save_path__)
        df = read_vcf_df(self.__save_path__)

        self.dw = DataWrapper(data, df)
        return self.dw
    
    # Range Filter parameters 
    def set_range(self, chromosome:int|None = None, min:int|None = None, max:int|None = None):
        self.__range_filter.configure(chromosome=chromosome, min=min, max=max)
        # Set datawrapper to be None to force data reload
        self.dw = None
    def get_range(self)->tuple[int, int]:
        """
        Get the position range of the dataset in the form (min, max)
        """
        return self.__range_filter.min, self.__range_filter.max
        
    def get_chromosome(self)->int:
        return self.__range_filter.chromosome
    
    # Quality filter parameters 
    def set_quality(self, min:float|None=None, max:float|None=None):
        self.__quality_filter.set_range(min,max)
        self.dw = None
    def get_quality(self)->tuple[float, float]:
        """
        Get the quality range of the dataset
        """
        return self.__quality_filter.get_range()
    
    def set_case(self,case_path:str):
        self._case = case_path
    def set_ctrl(self, ctrl_path:str):
        self._ctrl = ctrl_path

    
        

# ===================================================================
# Class used to filter based b