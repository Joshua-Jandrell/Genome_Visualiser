import os, time, csv
import pandas as pd
pd.set_option('future.no_silent_downcasting', True) # Opt in to future pd dataframe replace behavior used by allel
import allel as al


OUT_DIR = os.path.realpath('Data')
OUT_FILE = os.path.join(OUT_DIR, 'out.vcf.gz')
CASE_FILE = os.path.join(OUT_DIR, 'out.case.vcf.gz')
CTRL_FILE = os.path.join(OUT_DIR, 'out.ctrl.vcf.gz')

def clear_index(file_path:str):
    clear_file(file_path+'.csi')

def clear_file(file_path:str):
    if os.path.isfile(file_path):
        os.remove(file_path)

def make_index(file_path:str):
    os.system(f"bcftools index {file_path}")

def get_qual_filter(min:float, max:float)->str:
    return f" -i\"QUAL>={min} && QUAL<={max}\""

def get_filter_str(chrom:int, start:int, stop:int, min_qual:float|None=None, max_qual:float|None=None):
    # NOTE chr may or may not be appended in front of chromosome so both queries must be used
    query_str = f"-r chr{chrom}:{start}-{stop},{chrom}:{start}-{stop}"
    if min_qual is not None and max_qual is not None:
        query_str += get_qual_filter(min_qual, max_qual)
    return query_str

def filter_file(data_path:str, chrom:int, start:int, stop:int, min_qual:float|None=None, max_qual:float|None=None)->str:
    query_str = get_filter_str(chrom,start,stop,min_qual, max_qual)
    os.system("bcftools view " + query_str + " " + data_path+ " -o " + OUT_FILE)
    return OUT_FILE

def get_case_ctrl_paths(data_path:str)->tuple[str,str]:
    stripped_path = data_path.strip(".gz").strip(".vcf").strip(".bcf")
    case_file = stripped_path+".case.vcf.gz"
    ctrl_file = stripped_path+".ctrl.vcf.gz"
    return case_file, ctrl_file

def filter_case_oneshot(data_path:str, case_path:str, chrom:int, start:int, stop:int, min_qual:float|None=None, max_qual:float|None=None):
    filter_str = get_filter_str(chrom,start,stop,min_qual,max_qual)
    case_file, ctrl_file = get_case_ctrl_paths(data_path)
    os.system(f"bcftools view {filter_str} -S \"{case_path}\" {data_path} -o {case_file}")
    os.system(f"bcftools view {filter_str} -S \"^{case_path}\" {data_path} -o {ctrl_file}")
    return case_file, ctrl_file

def get_case_ctrl(data_path:str, case_path:str)->tuple[str, str]:
    case_file, ctrl_file = get_case_ctrl_paths(data_path)
    os.system(f"bcftools view -S \"{case_path}\" {data_path} -o {case_file}")
    os.system(f"bcftools view -S\"^{case_path}\" {data_path} -o {ctrl_file}")
    return  case_file, ctrl_file
    

def read_case_ctrl(case_file:str, ctrl_file:str)->tuple[dict, pd.DataFrame, dict, pd.DataFrame]:
    return al.read_vcf(case_file), al.read_vcf(ctrl_file)

def run_bcftools_speedtests(data_file:str, case_file:str, save_file:str|None = os.path.join(OUT_DIR, "times.csv"), n_iters:int = 10, chr=1, start:int=1, stop:int=20000, min_qual:float=None,max_qual:float=None):
    index_times:list[float] = [] # Time taken to generate a bcftools csi index file
    pos_filter_times:list[float] = [] # Time taken to extract to a file based on pos
    pos_and_qual_filter_times:list[float] = [] # Time taken to extract to a file based on pos and quality 
    case_ctrl_times:list[float] = [] # Time take to split (pos and quality extracted) file based on case and control
    oneshot_times:list[float] =  [] # Time taken to filer ad split into case and control in a single command
    read_times:list[float] =  [] # time taken to read in data from scikit allele
    split_total_time:list[float] =  [] # Total time taken where filtering an case/control are split
    oneshot_total_time:list[float] =  [] # Total time taken where filtering and case/control are combined
    
    case_data = None
    ctrl_data = None

    for _ in range(n_iters):
        # Clear all files
        clear_index(data_file)
        clear_file(OUT_FILE)
        case_data_path, ctrl_data_path = get_case_ctrl_paths(data_file)
        clear_file(case_data_path)
        clear_file(ctrl_data_path)

        # Time index making
        _t = time.time()
        make_index(data_file)
        index_times.append(time.time()-_t)

        # Time pos filtering
        _t = time.time()
        out_file = filter_file(data_file,chr,start,stop)
        pos_filter_times.append(time.time()-_t)
        clear_file(out_file)

        # Time pos and quality filtering
        _t = time.time()
        out_file = filter_file(data_file,chr,start,stop,min_qual,max_qual)
        pos_and_qual_filter_times.append(time.time()-_t)

        # Time case and control filtering
        _t = time.time()
        case_data_path, ctrl_data_path = get_case_ctrl(data_path=data_file, case_path=case_file)
        case_ctrl_times.append(time.time()-_t)
        clear_file(case_data_path)
        clear_file(ctrl_data_path)

        # Time one shot extraction
        _t = time.time()
        case_data_path, ctrl_data_path = filter_case_oneshot(data_file,case_file,chr,start,stop,min_qual,max_qual)
        oneshot_times.append(time.time()-_t)

        # Time data reading
        _t = time.time()
        case_data, ctrl_data = read_case_ctrl(case_data_path, ctrl_data_path)
        read_times.append(time.time()-_t)

        # calculate total times
        split_total_time.append(index_times[_]+pos_and_qual_filter_times[_]+case_ctrl_times[_]+read_times[_])
        oneshot_total_time.append(index_times[_]+oneshot_times[_]+read_times[_])

    # Write results to csv
    if save_file is not None:
        with open(save_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            iter_heads = [f"iter_{n+1}" for n in range(n_iters)]
            writer.writerow(["Operation", "Average"] + iter_heads)
            writer.writerow(["Indexing", sum(index_times)/n_iters] + index_times)
            writer.writerow(["Pos filtering", sum(pos_filter_times)/n_iters] + pos_filter_times)
            writer.writerow(["Pos and qual filtering", sum(pos_and_qual_filter_times)/n_iters] + pos_and_qual_filter_times)
            writer.writerow(["Case-control splitting", sum(case_ctrl_times)/n_iters] + case_ctrl_times)
            writer.writerow(["One shot filter and split", sum(oneshot_times)/n_iters] + oneshot_times)
            writer.writerow(["Read case and ctrl in to memory", sum(read_times)/n_iters] + read_times)
            writer.writerow(["Total (separate operations)", sum(split_total_time)/n_iters] + split_total_time)
            writer.writerow(["Total (one shot)", sum(oneshot_total_time)/n_iters] + oneshot_total_time)
            f.close()
    return case_data, ctrl_data 


if __name__ == "__main__":
    path = os.path.relpath('Data/afr-small.vcf.gz')
    case_path = os.path.relpath('Data/afr-small.case.tsv')
    run_bcftools_speedtests(path,case_path,chr=9,n_iters=1)
