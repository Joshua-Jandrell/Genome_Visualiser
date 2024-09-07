# Contains classes and data that can be used to filter, query and manage datasets
from VCF.dataWrapper import VcfDataWrapper as DataWrapper
# Class used to define how bcf filters should be applied
# Acts as a base class for more advanced data filters
class DataFilter_base():
    def __init__(self) -> None:
        pass
    def get_filter_str(self):
        return ""

# Class used to store and apply various vcf filters
class DataSetInfo:
    APPEND = "_subset"
    sets = []
    def __init__(self,source_path:str|None = None,save_path:str|None = None,name:str=None) -> None:
        self.filters = []
        self.source_path = source_path
        self.save_path = save_path
        self.name = name
        self.configure(source_path, save_path, name=name)
        self.get_save_path()
        self.get_dataset_name()
        print(f"Makde{self.name}")

    def __del__(self):
        print(f"killed {self.name}")
        

    def configure(self,source_path:str|None = None, save_path:str|None = None, filters:DataFilter_base|None = None, name:str|None = None):
        if source_path is not None: self.source_path = source_path
        if save_path is not None: self.save_path = save_path
        if filters is not None: self.filters = filters
        if name is not None: self.name = name

    def add_filter(self,filter:DataFilter_base):
        self.filters.append(filter)

    # Returns true if the given dataset is valid and can be created
    def is_valid(self):
        return self.source_path is not None # Assume that file type validation has already been done

    def get_save_path(self):
        if self.save_path is None:
            self.save_path = self.get_dataset_name()
        return self.save_path

    def get_dataset_name(self)->str:
        if self.name is None:
            # Remove source path and append desired suffix 
            self.name = self.source_path.rsplit('.')[0] + self.APPEND
        return self.name
    
    def get_data_wrapper()->DataWrapper:
        """Returns a `VcfDataWrapper` containing the data managed by this dataset (with all filtering applied)"""
    
class GlobalDatasetManager():
    """Holds a static record of all datasets created. Used to avoid unesesary searching and copying of datasets"""
    _datasets = {str,DataSetInfo} # Holds a list of all existing datasets

    def register(dataset:DataSetInfo):
        """Register a dataset for global access"""
        GlobalDatasetManager._datasets[dataset.gt]

    def deregister(dataset:DataSetInfo):
        """Remove a dataset from global access and delete references to it"""

    def reconfigure(keys:list[str]):
        """Remove all datasets that do not """

    def get_dataset(key:str):
        pass

# ===================================================================
# Class used to filter based b