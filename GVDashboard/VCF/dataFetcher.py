# This script contains simple classes for data fetching and selection
from os import path
import allel as al
from VCF.dataWrapper import VcfDataWrapper as DataWrapper


class DataFetcher:
    LOADED_DATA = {}

    # Checks if a file can be fetched and returns an error message if ic can't
    def canFetch(data_path:str)->tuple[bool, str]:
        # Check that path exists
        if not path.isfile(data_path):
            return False, "File Not Found"
        
        return True, ""


    def load_data(data_path:str, exclude_fields=None, rename_fields=None)->DataWrapper:

        if data_path not in DataFetcher.LOADED_DATA:
            full_path = path.realpath(data_path)
            DataFetcher.LOADED_DATA[data_path] = DataWrapper(al.read_vcf(full_path,
                                                                         exclude_fields=exclude_fields,
                                                                         rename_fields=rename_fields
                                                                         ))

        return DataFetcher.LOADED_DATA[data_path]