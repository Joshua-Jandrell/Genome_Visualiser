"""
Used to filter vcf files after reding it in via scikit allele
"""

import allel as al
import pandas as pd

def readFile(path:str, chrom:int, start:int, stop:int, tabix='tabix')->tuple[dict, pd.DataFrame]:
    """
    Reads in a region of a vcf file using scikit allele.\n
    Note: reading by region is required because files may be very large.
    """
    vcf = al.read_vcf(path,region=f"{chrom}:{start}-{stop}", tabix=tabix)
    df = al.vcf_to_dataframe(path,region=f"{chrom}:{start}-{stop}")
    return vcf, df

def select_by_qual(genome_data:al.GenotypeArray, df: pd.DataFrame, min=0, max=100)-> tuple[al.GenotypeArray, pd.DataFrame]:
    df = df[df["QUAL"].between(min, max, inclusive = 'both')]
    genome_data = genome_data[df.index,:]
    return genome_data, df

def select_case_ctrl(genome_data:al.GenotypeArray, samples_list:list[str], cases:list[str])->tuple[list[str], al.GenotypeArray, list[str], al.GenotypeArray]:
    """
    split a genotype data array into cases and controls.
    """
    case_mask = [s in cases for s in samples_list]
    case_data = genome_data[:, case_mask]
    ctrl_list = samples_list[:,not case_mask]
    ctrl_data = genome_data[:, not case_mask]
    return cases, case_data, ctrl_list, ctrl_data