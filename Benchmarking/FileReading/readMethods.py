"""
This script contains several methods for reading in VCF files.\n
These methods all use a combination of scikit-allele and vcf tools
"""
import os
import allel as al

def read_to_memory(file_path):
    """
    Read the vcf file directly into memory using default settings without any filtering.
    """
    data = al.read_vcf(file_path)

def read_to_dataframe(file_path):
    """
    Read the vcf file headers into a pandas dataframe.
    """
    df = al.vcf_to_dataframe(file_path)

def read_to_hdf5(file_path, save_name:str):
    al.vcf_to_hdf5(file_path, f"{save_name}.hdf5", overwrite=True)

def read_to_csv(file_path, save_name:str):
    al.vcf_to_csv(file_path, f"{save_name}.csv", overwrite=True)
