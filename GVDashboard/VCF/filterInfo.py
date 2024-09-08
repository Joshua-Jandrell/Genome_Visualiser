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
    names = [] # List of all dataset names to help avoid tow datasets having the same name

    def add_name(name:str):
        DataSetInfo.names.append(name)
    def clear_name(name:str):
        DataSetInfo.names.remove(name)
    def is_free_name(name:str)->bool:
        return name not in DataSetInfo.names


    def __init__(self,source_path:str|None = None,save_path:str|None = None,name:str="New Dataset") -> None:
        self.filters = []
        self.source_path = source_path
        self.save_path = save_path
        self.__name = None # Must set name to None here so that set name can use this variable 
        self.__set__name(name)
        self.configure(source_path, save_path, name=name)
        self.get_save_path()
        self.get_dataset_name()
        print(f"Make {self.__name}")

    def __del__(self):
        print(f"killed {self.__name}")
        DataSetInfo.clear_name(self.__name)
        

    def configure(self,source_path:str|None = None, save_path:str|None = None, filters:DataFilter_base|None = None, name:str|None = None):
        if source_path is not None: self.source_path = source_path
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
        self.__name = name # set name
    
    def get_data_wrapper()->DataWrapper:
        """Returns a `VcfDataWrapper` containing the data managed by this dataset (with all filtering applied)"""
        

# ===================================================================
# Class used to filter based b