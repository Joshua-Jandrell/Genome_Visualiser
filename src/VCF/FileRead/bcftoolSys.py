# This script contains simple classes for data fetching and selection
import subprocess, os
from typing import Literal

from _config_ import BCFTOOLS_CMD

#from VCF.dataWrapper import VcfDataWrapper as DataWrapper

def prep_for_bcftools(file_path:str)->str:
    """
    Prepares the given file to be processed with bcftools.\n
    Returns the path to the newly prepared file.
    """
    # Convert not-zipped files to compressed version to be used by bcftools
    if file_path[-3:] != ".gz":
        file_path = convert(file_path, file_path.rsplit('.')[-1]+'.gz')
    # index file
    index(file_path)
    return file_path

    
def get_base_pathname(file_path:str)->str:
    """
    Returns the path of a file without any .vcf, .bcf, .gz or .csi exactions.
    """
    return file_path.strip('.gz').strip('.vcf').strip('.bcf').strip('.csi')

def get_idex_name(file_path)->str:
    return file_path+".csi"

def get_conversion_char(output_type:Literal['bcf.gz', 'vcf', 'vcf.gz', 'bcf.gz'])->str:
    """
    Returns the character required to specify output type in bcf tools
    """
    if output_type == 'bcf.gz': return 'b'
    if output_type == 'bcf': return'u'
    if output_type == 'vcf': return 'v'
    if output_type == 'vcf.gz': return 'z'

def convert(file_path:str, output_type:Literal['bcf', 'bcf.gz', 'vcf', 'vcf.gz']='bcf.gz')->str:
    """
    Converts the given file to a bcf file using bcf tools
    """
    path_name = get_base_pathname(file_path)
    path_name = f"{path_name}.{output_type}"
    if os.path.isfile(path_name): return path_name
    
    convert_c = get_conversion_char(output_type)
    subprocess.call(f"{BCFTOOLS_CMD} convert -O {convert_c} {file_path} -o {path_name}")
    return path_name
               
def index(file_path:str):
    """
    Make an index for the given file using bcftools.
    """
    # Check if index exists
    if os.path.isfile(get_idex_name(file_path)): return
    subprocess.call(f"{BCFTOOLS_CMD} index {file_path}", shell=True)
        

def make_dataset_file(data_path:str, new_data_path:str, query_str:str="", output_type:Literal['bcf', 'bcf.gz', 'vcf', 'vcf.gz']='vcf.gz')->str:
    """
    Create a subset vcf file for data in the given region with the specified filter query. \n
    Returns the `new_data_path` if successful or the `data_path` if unsuccessful (due to bcftools exe not found).\n
    Second argument will be a tabix region string (to be used with scikit alle) if further regional filtering is needed.
    """
    output_type = output_type.strip(".") # remove '.' from output type to avoid double dots
    data_path = prep_for_bcftools(data_path)
    new_data_path = get_base_pathname(new_data_path)+"."+output_type # Ensure that output has correct file extension 
    subprocess.call(f"{BCFTOOLS_CMD} view {query_str.strip(' ')} {data_path} -O {get_conversion_char(output_type)} -o {new_data_path}", shell=True)
    return new_data_path

        


if __name__ == "__main__":
    make_dataset_file(os.path.realpath("Data/med.vcf.gz"), os.path.realpath("Data/med_1.vcf.gz"))