# Contains classes and data that can be used to filter, query and manage datasets
from os import path
from VCF.dataWrapper import VcfDataWrapper as DataWrapper
from VCF.dataFetcher import DataFetcher
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
        if opt == "-i":
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
        if opt in ["", " "]: return f"-r chr{self.chromosome}:{self.min}-{self.max}"
        return super().get_query_str(opt)
    def apply_to_wrapper(self, dw: DataWrapper):
        dw.set_pos_range(min_pos=self.min, max_pos=self.max)
    
class QualityFilter(ParamRangeFilter):
    def __init__(self, min:float=0, max:float=100):
        super().__init__(column='QUAL', min=min, max=max)
    def apply_to_wrapper(self,dw: DataWrapper):
        dw.set_qual_range(min_qual=self.min, max_qual=self.max)



# Class used to store and apply various vcf filters
class DataSetInfo:
    POS_RANGE = 20000
    APPEND = "_subset"
    names = [] # List of all dataset names to help avoid tow datasets having the same name
    data_wrappers = {} # stores a list of pre-computed data wrappers 

    def add_name(name:str):
        DataSetInfo.names.append(name)
    def clear_name(name:str):
        DataSetInfo.names.remove(name)
    def is_free_name(name:str)->bool:
        return name not in DataSetInfo.names


    def __init__(self,source_path:str|None = None,save_path:str|None = None,name:str|None = None) -> None:
        self.filters:list[DataFilter_base] = []
        # Add make required filters
        # NOTE this must be done before configuration
        self.__range_filter = RegionFiler()
        self.__quality_filter = QualityFilter()


        self.source_path = source_path
        self.save_path = save_path
        self.__name = None # Must set name to None here so that set name can use this variable 
        # If a path was given, use this to name the dataset 
        self.dw = None
        if name is None:
            if source_path is not None:
                name = path.basename(source_path)
            else:
                name = "New Dataset"
        self.__set__name(name)
        self.configure(source_path, save_path, name=name)
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

    def configure(self,
                  source_path:str|None = None,
                  save_path:str|None = None,
                  filters:DataFilter_base|None = None,
                  name:str|None = None
                  ):
        if source_path is not None and self.source_path != source_path:
            self.source_path = source_path
            self.__peak_data()
        if save_path is not None: self.save_path = save_path
        if filters is not None: self.filters = filters
        if name is not None: self.__set__name(name)

    def add_filter(self,filter:DataFilter_base):
        self.filters.append(filter)

    def is_valid(self):
        """Returns true if the given dataset is valid and can be created
        """
        return self.source_path is not None # Assume that file type validation has already been done

    def get_source_path(self)->str|None:
        return self.source_path
    def get_save_path(self):
        if self.save_path is None:
            self.save_path = self.get_dataset_name()
        return self.save_path

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
        print("NOTE: update data peaking")
        dw = self.get_data_wrapper()
        chromo = int(dw.get_chromosome()[0].strip("chr"))
        min_pos = dw.get_pos()[0]
        max_pos = min_pos + self.POS_RANGE

        self.__range_filter.configure(chromosome=chromo, min=min_pos, max=max_pos)
    
    def get_data_wrapper(self)->DataWrapper:
        """Returns a `VcfDataWrapper` containing the data managed by this dataset (with all filtering applied)"""
        if self.dw is None:
            self.dw = DataFetcher.load_data(self.get_source_path())
            for filter in self.filters:
                filter.apply_to_wrapper(self.dw)
            #print("not using old wrapper?")
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
    
        

# ===================================================================
# Class used to filter based b