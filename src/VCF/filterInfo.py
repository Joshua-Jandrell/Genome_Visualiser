# Contains classes and data that can be used to filter, query and manage datasets
import random, os
import pandas as pd
from typing import Any, Literal, Callable
from VCF.dataWrapper import VcfDataWrapper as DataWrapper
from Util.event import Event

from .dataLoad import peek_vcf_data, read_vcf_df, read_vcf_data
from .FileRead.bcftoolSys import make_dataset_file, convert
from .FileRead.caseCtrl import read_case_ctrl



DEFAULT_VARIANTS = 25000
DEFAULT_DISPLAY = 500
REGION_CMD = '-r'
INCLUDE_CMD = '-i'

class FilterError(ValueError):
    pass


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
        query_str += (" -r " + ",".join([s for s in [chr_prefix+filt.get_query_str('-r') for filt in filters] if s not in ["", chr_prefix]]))
    if INCLUDE_CMD in cmds:
        query_str += (" -i \"" + " && ".join([chr_prefix+filt.get_query_str('-i') for filt in filters]) +"\" ")

    return query_str



# Class used to store and apply various vcf filters
class DataSetInfo:
    POS_RANGE = 20000
    APPEND = "_subset"
    names = [] # List of all dataset names to help avoid tow datasets having the same name
    _files = []
    __FILE_EXTENSION = ".vcf.gz"
    data_wrappers = {} # stores a list of pre-computed data wrappers 

    @classmethod
    def __make_valid_save_file_name(cls, dir):
        """
        Crates a unique save file name for the given data set
        """
        save_file = os.path.join(os.path.relpath(dir),'.' +  str(random.randint(0,999999999)))+cls.__FILE_EXTENSION
        if save_file in cls._files: return cls.__make_valid_save_file_name()
        else:
            cls._files.append(save_file)
            return save_file
        
    @classmethod 
    def __clear_save_file_name(cls, name):
        """
        clears the given save file name.
        """
        if name in cls._files:
            cls._files.remove(name)

    def add_name(name:str):
        DataSetInfo.names.append(name)
    def clear_name(name:str):
        DataSetInfo.names.remove(name)
  
    def is_free_name(name:str)->bool:
        return name not in DataSetInfo.names


    def __init__(self,source_path:str|None = None,name:str|None = None, case_path:str|None="", ctrl_path:str|None="") -> None:
        
        self._update_event = Event()
        """
        Event called whenever dataset parameters are updated.\n
        """

        # Flags used to see which fields must be updated 
        self.__reload_flag = False
        """Set to true if sample save file should be re-loaded"""
        self.__save_flag = False
        
        
        self.filters:list[DataFilter_base] = []
        # Add make required filters
        # NOTE this must be done before configuration
        self.__range_filter = RegionFiler()
        self.__quality_filter = QualityFilter()



        self.__save_path = None
        self.__name = None # Must set name to None here so that set name can use this variable 

        # Initial variables (MUST be set later using configure)
        self.source_path = None
        self.chr = None
        self.chr_prefix=""
        self.abs_start = 1
        self.abs_end = None
        self.abs_end = False

        self._case_path = None

        self.__destroyed = False

        # If a path was given, use this to name the dataset 
        self.dw = None

        self.set_source_path(source_path)

        if name is None:
            if source_path is not None:
                name = os.path.basename(source_path)
            else:
                name = "New Dataset"
        self.__set__name(name)
        self.configure(source_path, name=name, case_path = case_path)
        self.get_dataset_name()
        #print(f"Make {self.__name}")

        # Add required filters to filter stack
        self.add_filter(self.__range_filter)
        self.add_filter(self.__quality_filter)


    def __del__(self):
        #print(f"killed {self.__name}")
        self.destroy()

    def add_listener(self, command:Callable[["DataSetInfo", Literal['source', 'variants', 'samples', 'delete']],Any]):
        self._update_event.add_listener(command=command)

    def remove_listener(self, command:Callable[["DataSetInfo", Literal['source', 'variants', 'samples', 'delete']],Any]):
        self._update_event.remove_listener(command)

    def configure(self,
                  source_path:str|None = None,
                  filters:DataFilter_base|None = None,
                  name:str|None = None,
                  case_path:str|None = None,
                  ):
        if source_path is not None and self.source_path != source_path:
            self.set_source_path(source_path)
        if filters is not None: self.filters = filters
        if name is not None: self.__set__name(name)
        if case_path is not None: self.set_case_path(case_path)

    def destroy(self):
        """
        Called to delete all dataset files and remove all records of dataset.\n
        If a reference to this dataset still exists the dataset will return None instead of a datawrapper.
        """
        if self.__destroyed: return
        
        DataSetInfo.clear_name(self.__name)
        if self.__save_path is not None:
            DataSetInfo.__clear_save_file_name(self.__save_path)
        self.__clear_save()
        self._update_event.remove_all()
        self.__destroyed = True

    def set_source_path(self,source_path:str|None):
        if source_path == self.source_path: return

        # Clear any old save files
        self.__clear_save()

        self.source_path = source_path
        if self.source_path is None: return

        # Peak into dataset to see if full file can be loader reasonably
        self.__peek_data()

        # Make a save path if it will be required
        if not self.at_end:
            # Peaking did not reveal the full file, that dataset is big and should thus be stored in memory
            self.__save_path = self.__make_valid_save_file_name(os.path.dirname(source_path))

        self._update_event.invoke(self, 'source')

    def __clear_save(self):
        """
        Remove the save file if it exists.
        """
        if self.__save_path is None: return
        if os.path.isfile(self.__save_path):
            os.remove(self.__save_path)
            self.__save_flag = False
        self.__save_path = None

    def add_filter(self,filter:DataFilter_base):
        self.filters.append(filter)

        
        self._update_event.invoke(self, 'variants')

    def is_valid(self):
        """Returns true if the given dataset is valid and can be created
        """
        return self.source_path is not None # Assume that file type validation has already been done

    def get_source_path(self)->str|None:
        return self.source_path

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

    def __peek_data(self):
        """
        Called only when a new source file is set.\n
        This function loads in default range value by peaking at the dataset loaded and finding its chromosome and first value.
        """
        peek_info = peek_vcf_data(self.source_path, DEFAULT_VARIANTS, target_pt=DEFAULT_DISPLAY)
        self.chr_prefix = peek_info['CHROM/prefix']

        chr = peek_info['CHROM/number']
        self.abs_start = min_pos = peek_info['POS/first']
        max_pos = peek_info['POS/target']
        if peek_info['POS/at_end']:
            self.abs_end = max_pos

        self.at_end = peek_info['POS/at_end']

        self.set_range(chromosome=chr, min=min_pos, max=max_pos)

    def __should_make_save_file(self)->bool:
        """
        Returns true if the dataset should use an external save file to store pre-filtered data, \n
        or if the existing save file should be remade.
        """
        return not self.at_end and (not self.__save_flag or self.__reload_flag)
    
    def __should_reload_data(self)->bool:
        """
        Returns true is the given dataset should be reloaded from file into memory.\\
        This is generally required if the filter parameters have been updated.
        """
        return self.dw is None or self.__reload_flag

    
    def get_data(self)->DataWrapper|None:
        """Returns a `VcfDataWrapper` containing the data managed by this dataset (with all filtering applied)"""
        if self.__destroyed:
            raise Exception("Trying to get data from destroyed da")

        data_path = self.__save_path
        if data_path is None: data_path = self.source_path
        
        # Pre-load vcf data using bcftools if required 
        if self.__should_make_save_file():
            query_str = get_filter_query_str(self.filters,['-r'], chr_prefix=self.chr_prefix)
            data_path = make_dataset_file(self.source_path,
                                                   os.path.join(os.path.dirname(self.source_path),self.__save_path),
                                                   query_str=query_str,
                                                   output_type=self.__FILE_EXTENSION)
            assert(data_path == self.__save_path)
            self.__save_flag = True


        if self.__should_reload_data():
            # Load datawrapper
            data = read_vcf_data(data_path)
            if data is None:
                return None

            # Get cases and controls 
            cases, ctrls = read_case_ctrl(self._case_path)

            chr = f"{self.chr_prefix}{self.__range_filter.chromosome}"
            self.dw = DataWrapper(data, chr, cases=cases, ctrls=ctrls)

            self.__reload_flag = False

            for filt in self.filters:
                filt.apply_to_wrapper(self.dw)
                

        return self.dw
    
    # Range Filter parameters 
    def set_range(self, chromosome:int|None = None, min:int|None = None, max:int|None = None):
        requires_reload = self.__range_filter.min is None or self.__range_filter.max is None
        if not requires_reload and min is not None:
            requires_reload =  self.__range_filter.min > min
        if not requires_reload and max is not None:
             requires_reload = self.__range_filter.max < max
        if not requires_reload and chromosome is not None:
            requires_reload = self.__range_filter.chromosome != chromosome

        if requires_reload:
            self.__reload_flag = True

        # Set region reload flag if on a new chromosome
        self.__save_flag = self.__range_filter.chromosome == chromosome
        
        self.__range_filter.configure(chromosome=chromosome, min=min, max=max)

        if self.dw is not None:
            self.__range_filter.apply_to_wrapper(self.dw)

        self._update_event.invoke(self, 'variants')

    def get_range(self)->tuple[int, int]:
        """
        Get the position range of the dataset in the form (min, max)
        """
        return self.__range_filter.min, self.__range_filter.max
        
    def get_chromosome(self)->int:
        return self.__range_filter.chromosome
    
    # Quality filter parameters 
    def set_quality(self, min:float|None=None, max:float|None=None):
        if (min is not None and min < self.__quality_filter.min) or (max is not None and max > self.__quality_filter.max):
            self.__reload_flag = True

        self.__quality_filter.set_range(min,max)

        if self.dw is not None:
            self.__quality_filter.apply_to_wrapper(self.dw)

        self._update_event.invoke(self, 'variants')

    def get_quality(self)->tuple[float, float]:
        """
        Get the quality range of the dataset
        """
        return self.__quality_filter.get_range()
    
    def set_case_path(self,case_path:str):
        self._case_path = case_path
        if self.dw is not None:
            cases, ctrls = read_case_ctrl(case_path)
            self.dw.set_case_ctrl(cases, ctrls)

        self._update_event.invoke(self, 'samples')
    def get_case_path(self)->str|None:
        return self._case_path

    
        

# ===================================================================
# Class used to filter based b