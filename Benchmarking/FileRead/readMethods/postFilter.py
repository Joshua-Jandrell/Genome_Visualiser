"""
Used to filter vcf files after reding it in via scikit allele
"""
import time, csv, os
import allel as al
import pandas as pd
pd.set_option('future.no_silent_downcasting', True) # Opt in to future pd dataframe replace behavior used by allel
import numpy as np

OUT_DIR = os.path.realpath('Data')

def read_file(path:str, chrom:int, start:int, stop:int, tabix='tabix')->dict:
    """
    Reads in a region of a vcf file using scikit allele.\n
    Note: reading by region is required because files may be very large.
    """
    data = al.read_vcf(path,region=f"{chrom}:{start}-{stop}", tabix=tabix)
    if data is None:
        return al.read_vcf(path,region=f"chr{chrom}:{start}-{stop}", tabix=tabix)
    else: return data

def read_df(path:str, chrom:int, start:int, stop:int, tabix='tabix')->pd.DataFrame:
    df =  al.vcf_to_dataframe(path,region=f"{chrom}:{start}-{stop}", tabix=tabix)
    if df is None:
        return al.vcf_to_dataframe(path,region=f"chr{chrom}:{start}-{stop}", tabix=tabix)
    else: return df


def select_by_qual(genome_data:dict, df: pd.DataFrame, min=0, max=100)-> tuple[al.GenotypeArray, pd.DataFrame]:
    df = df[df["QUAL"].between(min, max, inclusive = 'both')]
    genome_data['calldata/GT'] = genome_data['calldata/GT'][df.index,:]
    for k in ['variants/QUAL', 'variants/CHROM', 'variants/REF', 'variants/ALT', 'variants/POS']:
        genome_data[k] = genome_data[k][df.index]
    return genome_data, df

def select_case_ctrl(data:dict, cases:list[str])->tuple[list[str], al.GenotypeArray, list[str], al.GenotypeArray]:
    """
    split a genotype data array into cases and controls.
    """
    case_mask = [s in cases for s in data['samples']]
    case_data = dict(data)
    ctrl_data = dict(data)
    case_data['calldata/GT'] = case_data['calldata/GT'][:,case_mask]
    case_data['samples'] = case_data['samples'][case_mask]
    invert_mask = [not b for b in case_mask]
    ctrl_data['calldata/GT'] = ctrl_data['calldata/GT'][:,invert_mask]
    ctrl_data['samples'] = ctrl_data['samples'][invert_mask]
    return case_data, ctrl_data

def get_case_list(case_file:str)->list[str]:
    f = open(case_file, mode='r')
    case_list = f.read().split()
    f.close()
    return case_list


def run_al_speedtests(data_file:str, case_file:str, save_file:str|None = os.path.join(OUT_DIR, "post_times.csv"), n_iters:int = 10, chr=1, start:int=1, stop:int=20000, min_qual:float=0,max_qual:float=100):

    read_times_no_tabix:list[float] = [] # Time taken tor read file without tabix 
    read_times:list[float] = [] # Times taken to read dataset into memory
    df_read_times:list[float] = [] # Times taken to convert data into pandas data frame
    qual_filter_times:list[float] = [] # Times taken to filter data according to quality
    case_file_read_times:list[float] = [] # Time taken to read case control file in to memory
    case_ctrl_times:list[float] = [] # times taken to select case and control datasets
    total_times:list[float] = [] # Total time for filtering.

    case_data=None
    ctrl_data=None

    for _ in range(n_iters):

        # Time file reading
        _t = time.time_ns()
        data = read_file(data_file, chr, start, stop, tabix=None)
        read_times_no_tabix.append((time.time_ns()-_t)/(10**9))
        _t = time.time_ns()
        data = read_file(data_file, chr, start, stop)
        read_times.append((time.time_ns()-_t)/(10**9))
        
        # time making a data frame
        _t = time.time_ns()
        df= read_df(data_file, chr, start, stop)
        df_read_times.append((time.time_ns()-_t)/(10**9))
        
        # time filtering by quality 
        _t = time.time_ns()
        data, df = select_by_qual(data, df, min_qual, max_qual)
        qual_filter_times.append((time.time_ns()-_t)/(10**9))

        # Time case/control reading 
        _t = time.time_ns()
        cases = get_case_list(case_file=case_file)
        case_file_read_times.append((time.time_ns()-_t)/(10**9))

        # Time case/control selection
        _t = time.time_ns()
        case_data, ctrl_data = select_case_ctrl(data, cases)
        case_ctrl_times.append((time.time_ns()-_t)/(10**9))

        total_times.append(read_times[_]+df_read_times[_]+qual_filter_times[_]+case_file_read_times[_]+case_ctrl_times[_])
        
    # Write results to csv file
    if save_file is not None:
        with open(save_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            iter_heads = [f"iter_{n+1}" for n in range(n_iters)]
            writer.writerow(["Operation", "Average"] + iter_heads)
            writer.writerow(["Data reading", sum(read_times)/n_iters] + read_times)
            writer.writerow(["Data reading (no tabix)", sum(read_times_no_tabix)/n_iters] + read_times_no_tabix)
            writer.writerow(["DF reading", sum(df_read_times)/n_iters] + df_read_times)
            writer.writerow(["Quality filtering", sum(qual_filter_times)/n_iters] + qual_filter_times)
            writer.writerow(["Case file reading", sum(case_file_read_times)/n_iters] + case_file_read_times)
            writer.writerow(["Case-control splitting", sum(case_ctrl_times)/n_iters] + case_ctrl_times)
            writer.writerow(["Total", sum(total_times)/n_iters] + total_times)
            f.close()

    return case_data, ctrl_data

if __name__ == "__main__":
    path = os.path.relpath('Data/afr-small.vcf.gz')
    case_path = os.path.relpath('Data/afr-small.case.tsv')
    run_al_speedtests(path,case_path,chr=9,n_iters=1)