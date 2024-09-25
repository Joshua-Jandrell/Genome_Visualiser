"""
Used to filter vcf files after reding it in via scikit allele
"""
import time, csv, os
import allel as al
import pandas as pd
import numpy as np

OUT_DIR = os.path.realpath('Data')

def read_file(path:str, chrom:int, start:int, stop:int, tabix='tabix')->dict:
    """
    Reads in a region of a vcf file using scikit allele.\n
    Note: reading by region is required because files may be very large.
    """
    return al.read_vcf(path,region=f"{chrom}:{start}-{stop}", tabix=tabix)

def read_df(path:str, chrom:int, start:int, stop:int, tabix='tabix')->pd.DataFrame:
    return al.vcf_to_dataframe(path,region=f"{chrom}:{start}-{stop}", tabix=tabix)

def select_by_qual(genome_data:np.ndarray, df: pd.DataFrame, min=0, max=100)-> tuple[al.GenotypeArray, pd.DataFrame]:
    df = df[df["QUAL"].between(min, max, inclusive = 'both')]
    genome_data = genome_data[df.index,:]
    return genome_data, df

def select_case_ctrl(genome_data:np.ndarray, samples_list:list[str], cases:list[str])->tuple[list[str], al.GenotypeArray, list[str], al.GenotypeArray]:
    """
    split a genotype data array into cases and controls.
    """
    case_mask = [s in cases for s in samples_list]
    case_data = genome_data[:, case_mask]
    ctrl_list = samples_list[not case_mask]
    ctrl_data = genome_data[:, not case_mask]
    return cases, case_data, ctrl_list, ctrl_data

def get_case_list(case_file:str)->list[str]:
    f = open(case_file, mode='r')
    return f.read().split()


def run_al_speedtests(data_file:str, case_file:str, save_file:str = os.path.join(OUT_DIR, "post_times.csv"), n_iters:int = 10, chr=1, start:int=1, stop:int=20000, min_qual:float=80,max_qual:float=100):

    read_times_no_tabix:list[float] = [] # Time taken tor read file without tabix 
    read_times:list[float] = [] # Times taken to read dataset into memory
    df_read_times:list[float] = [] # Times taken to convert data into pandas data frame
    qual_filter_times:list[float] = [] # Times taken to filter data according to quality
    case_file_read_times:list[float] = [] # Time taken to read case control file in to memory
    case_ctrl_times:list[float] = [] # times taken to select case and control datasets
    total_times:list[float] = [] # Total time for filtering.
    for _ in range(n_iters):

        # Time file reading
        _t = time.time()
        data = read_file(data_file, chr, start, stop, tabix=None)
        read_times_no_tabix.append(time.time()-_t)
        _t = time.time()
        data = read_file(data_file, chr, start, stop)
        read_times.append(time.time()-_t)
        
        # time making a data frame
        _t = time.time()
        df= read_df(data_file, chr, start, stop)
        df_read_times.append(time.time()-_t)
        
        # time filtering by quality 
        _t = time.time()
        data['calldata/GT'], df = select_by_qual(data['calldata/GT'], df)
        qual_filter_times.append(time.time()-_t)

        # Time case/control reading 
        _t = time.time()
        cases = get_case_list(case_file=case_file)
        case_file_read_times.append(time.time()-_t)

        # Time case/control selection
        _t = time.time()
        case_list, case_data, ctrl_list, ctrl_data = select_case_ctrl(data['calldata/GT'], data['samples'], cases)
        case_ctrl_times.append(time.time()-_t)

        total_times.append(read_times[_]+df_read_times[_]+qual_filter_times[_]+case_file_read_times[_]+case_ctrl_times[_])
        
    # Write results to csv file
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

if __name__ == "__main__":
    path = os.path.relpath('Data/afr-small.vcf.gz')
    case_path = os.path.relpath('Data/afr-small.case.tsv')
    run_al_speedtests(path,case_path,chr=9,n_iters=1)