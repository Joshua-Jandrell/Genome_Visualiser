"""
Contains a list of functions ued to 'peek' into vcf datasets to determine their scale and characteristics.
"""
import os
import allel as al, pandas

def peek_vcf_data(file_path:str, variant_count = 10000)->dict:
    """
    'peek' into a vcf file to see the following:\n
    - The number of the first listed chromosome. `['CHROM/number']`
    - How chromosomes are formatted. `['CHROM/prefix']`
    - The position of the first variant. `['POS/first']`
    - The position of the last variant if sampling by the given variant count. `['POS/last']`
    - If the data continues beyond the sample variant count (True if at end). `['POS/at_end']`
    - The number of samples expected. `['samples/count']`
    """
    peek_length = variant_count+1 # Peek one variant more than required to detect data end correctly.
    fields, samples, headers, it = al.iter_vcf_chunks(file_path, fields=['variants/POS', 'variants/CHROM'], chunk_length=peek_length)
    # Get first chunk of data only
    data, count, _, pos  = it.__next__()

    chr_format = "".join([c for c in data['variants/CHROM'][0] if not c.isdigit()])
    chr_n = int(data['variants/CHROM'][0].strip(chr_format))
 
    first_pos = data['variants/POS'][0]
    last_pos = data['variants/POS'][-2] # use second last value to account for extended peek length 

    at_end = pos == 0
    
    # Correct last pos for case where data has not ended and thus
    if at_end: last_pos = data['variants/POS'][-1]


    n_samples = len(samples)


    return {
        'CHROM/number':chr_n,
        'CHROM/prefix':chr_format,
        'POS/first':first_pos,
        'POS/last':last_pos,
        'POS/at_end':at_end,
        'samples/count':n_samples
    }

def read_vcf_data(file_path:str, region_str:str|None = None)->dict:
    if region_str is None:
        return al.read_vcf(file_path)
    else:
        return al.read_vcf(file_path, region=region_str)
    
def read_vcf_df(file_path:str, region_str:str|None = None)->pandas.DataFrame:
    if region_str is None:
        return al.vcf_to_dataframe(file_path)
    else:
        return al.vcf_to_dataframe(file_path, region=region_str)



if __name__ == "__main__":
    p = os.path.realpath("Data/afr-small.vcf.gz")
    d = peek_vcf_data(p,1748)
    print(d['POS/first'])
    print(d['POS/last'])