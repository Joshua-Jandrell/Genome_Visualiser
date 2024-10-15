"""
Combines filtering methods from bcftools and sickie allele to verify that a hybrid approach can be more effective than either option.\\
The steps are as follows:\\
- Index .vcf file (with bcftools).
- Filter indexed file for position and quality (bcftools).
- Read file into memory (scikit allele).
- Read, filter and split according to case/control data.
"""
import time, csv, os
import allel as al

from .bcftoolsFilter import make_index, clear_index, clear_file, OUT_FILE, filter_file
from .postFilter import get_case_list, select_case_ctrl
OUT_DIR = os.path.realpath('Data')

def run_hybrid_speedtests(data_file:str, case_file:str, save_file:str|None = os.path.join(OUT_DIR, "times.csv"), n_iters:int = 10, chr=1, start:int=1, stop:int=20000, min_qual:float=None,max_qual:float=None):
    index_times:list[float] = [] # Time taken to generate a bcftools csi index file
    pos_and_qual_filter_times:list[float] = [] # Time taken to extract to a file based on pos and quality 
    read_times:list[float] =  [] # time taken to read in data from scikit allele
    case_file_read_times:list[float] = [] # Time taken to read case control file in to memory
    case_ctrl_times:list[float] = [] # times taken to select case and control datasets
    total_times:list[float] = [] # Total time for filtering.
    
    case_data = None
    ctrl_data = None

    for _ in range(n_iters):

        # Clear all files
        clear_index(data_file)
        clear_file(OUT_FILE)

        # Time index making
        _t = time.time_ns()
        make_index(data_file)
        index_times.append((time.time_ns()-_t)/(10**9))

        # Time pos and quality filtering
        _t = time.time_ns()
        out_file = filter_file(data_file,chr,start,stop,min_qual,max_qual)
        pos_and_qual_filter_times.append((time.time_ns()-_t)/(10**9))
        assert(OUT_FILE == out_file)

        # Time data reading
        _t = time.time_ns()
        data = al.read_vcf(out_file)
        read_times.append((time.time_ns()-_t)/(10**9))

        # Time case/control reading 
        _t = time.time_ns()
        cases = get_case_list(case_file=case_file)
        case_file_read_times.append((time.time_ns()-_t)/(10**9))

        # Time case/control selection
        _t = time.time_ns()
        case_data, ctrl_data = select_case_ctrl(data, cases)
        case_ctrl_times.append((time.time_ns()-_t)/(10**9))

        total_times.append(index_times[_]+pos_and_qual_filter_times[_]+read_times[_]+case_file_read_times[_]+case_ctrl_times[_])

    # Write results to csv
    if save_file is not None:
        with open(save_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            iter_heads = [f"iter_{n+1}" for n in range(n_iters)]
            writer.writerow(["Operation", "Average"] + iter_heads)
            writer.writerow(["Indexing", sum(index_times)/n_iters] + index_times)
            writer.writerow(["Pos and qual filtering", sum(pos_and_qual_filter_times)/n_iters] + pos_and_qual_filter_times)
            writer.writerow(["Read case and ctrl in to memory", sum(case_file_read_times)/n_iters] + case_file_read_times)
            writer.writerow(["Case-control splitting", sum(case_ctrl_times)/n_iters] + case_ctrl_times)
            writer.writerow(["Read in to memory", sum(read_times)/n_iters] + read_times)
            writer.writerow(["Total", sum(total_times)/n_iters] + total_times)
            f.close()


    # Clear all files
    clear_index(data_file)
    clear_file(OUT_FILE)

    return case_data, ctrl_data 