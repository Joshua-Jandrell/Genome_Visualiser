import os
from config import RESULT_DIR, DATA_FOLDER
from FileRead import run_al_speedtests, run_bcftools_speedtests, run_hybrid_speedtests

N_SAMPLES = 10
SMALL_FILE = "afr-small"
MED_FILE = "med"
LARGE_FILE = "afr"
SUFFIX = ".vcf.gz"
CASE_SUFFIX = ".case.tsv"
SAVE_DIR = os.path.join(RESULT_DIR,"ReadTimes")

def map_chr(file:str):
    if file == MED_FILE:
        return 1
    else:
        return 9


if __name__ == "__main__":
    os.makedirs(SAVE_DIR, exist_ok=True)
    for test_file in [SMALL_FILE, MED_FILE, LARGE_FILE]:
        n_iters = N_SAMPLES

        chr = map_chr(test_file)
        
        data_path = os.path.join(DATA_FOLDER,test_file+SUFFIX)
        case_path = os.path.join(DATA_FOLDER,test_file+CASE_SUFFIX)
        # run_al_speedtests(data_path, case_path,
        #                 os.path.join(SAVE_DIR,test_file+"_al_times.csv"),
        #                 chr=chr, start=10000, stop=11000,
        #                 min_qual=25, max_qual=100,
        #                 n_iters=n_iters)
        # run_bcftools_speedtests(data_path, case_path,
        #                 os.path.join(SAVE_DIR,test_file+"_bcftools_times.csv"),
        #                 chr=chr, start=10000, stop=11000,
        #                 min_qual=25, max_qual=100,
        #                 n_iters=n_iters)
        run_hybrid_speedtests(data_path, case_path,
                        os.path.join(SAVE_DIR,test_file+"_hybrid_times.csv"),
                        chr=chr, start=10000, stop=11000,
                        min_qual=25, max_qual=100,
                        n_iters=n_iters)
        
    
    