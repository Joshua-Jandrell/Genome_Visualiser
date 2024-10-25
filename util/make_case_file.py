"""
Randomly make a case file for the given dataset
"""
import sys, os
import allel as al
import random
def _makeRandomCaseCtrl(file_path)->tuple[list[str], list[bool]]:
    """
    Reads in the samples form a give file and randomly assigns them to be either case or control.
    """
    fields, samples, headers, it = al.iter_vcf_chunks(file_path, fields=['POS'], chunk_length=5)
    case_bool = [random.choice([True, False]) for s in samples]
    return samples, case_bool

def _write_cases(path:str, samples:list[str], case_bool:bool):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(file=path, mode='w') as f:
        split_char = "\t"
        if path[-4:] == ".csv": split_char = ","
        for _i, sample in enumerate(samples):
            f.write("".join([sample, split_char, str(case_bool[_i]),'\n']))
        f.close()

def makeRandomCaseFile(vcf_file:str, case_file_path:str|None = None):
    """Generates a radom case file for the given dataset"""

    # Make case path if it does not exist
    if case_file_path is None or "":
        case_file_path = vcf_file+".random.case.csv"

    samples, case_bool = _makeRandomCaseCtrl(vcf_file)
    _write_cases(case_file_path, samples, case_bool)

    

if __name__ == "__main__":
    if len(sys.argv) != 3 :
        print(f"Usages {sys.argv[0]} <vcf-file-path> <case-ctrl-file-path>")
        exit()
    samples, case_bool = _makeRandomCaseCtrl(sys.argv[1])
    _write_cases(sys.argv[2], samples, case_bool)