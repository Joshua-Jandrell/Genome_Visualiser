# This script contains simple classes for data fetching and selection
from os import path
import allel as al
from VCF.dataWrapper import VcfDataWrapper as DataWrapper


class DataFetcher:

    # Checks if a file can be fetched and returns an error message if ic can't
    def canFetch(data_path:str)->tuple[bool, str]:
        # Check that path exists
        if not path.isfile(data_path):
            return False, "File Not Found"
        
        return True, ""


    def load_data(data_path:str, exclude_fields=None, rename_fields=None)->DataWrapper:

        full_path = path.realpath(data_path)
        data = al.read_vcf(full_path,
                                        exclude_fields=exclude_fields,
                                        rename_fields=rename_fields,
                                        )
        dataframe = al.vcf_to_dataframe(full_path)
        data_wrapper = DataWrapper(data, dataframe)

        return data_wrapper