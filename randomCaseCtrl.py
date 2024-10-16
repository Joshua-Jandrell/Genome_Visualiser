"""
Generates a random case control file for the given vcf dataset
"""
import sys, os
import allel as al
import random
def makeRandomCaseCtrl(file_path):
    fields, samples, headers, it = al.iter_vcf_chunks(file_path, chunk_length=5000)
    cases = [s for s in samples if random.choice([True, False])]
    return cases

def write_cases(path:str, case_list:list[str]):
    with open(file=path, mode='w') as f:
        f.write("\n".join(case_list))
        f.close()
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usages {sys.argv[0]} <vcf file path>")
        exit()
    cases = makeRandomCaseCtrl(sys.argv[1])
    dir = os.path.dirname(sys.argv[1])
    file = os.path.basename(sys.argv[1]).strip(".gz").strip(".vcf")
    case_file = os.path.join(dir,file+".case.tsv")
    write_cases(case_file, cases)