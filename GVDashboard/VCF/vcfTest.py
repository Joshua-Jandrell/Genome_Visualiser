# Simple script that contains tools for testing vcf file reading and writing 

import allel as al # Used for VCF file manipulation
import os

TEST_FILE = os.path.realpath("./Data/afr-small.vcf") # Path to the vcf file used for testing

def getData()->dict:
    return al.read_vcf(TEST_FILE)


if __name__ == "__main__":
    data = getData()
    df = al.vcf_to_dataframe(TEST_FILE)
    print(data.keys())
    bool_search = (df["QUAL"].between(30, 35, inclusive = 'both')) & (df["POS"]<15000)
    new_df = df[bool_search]
    new_df = new_df.sort_values(by=["QUAL"], ascending=True)
    print(new_df)
    print(new_df.index)

    
    # Use the dataframe index to access rows (or columns) for the genotype array
    print(al.GenotypeArray(data['calldata/GT'])[new_df.index,:])

    # print(len(max(data['variants/REF'], key=len)))
    # print((max(data['variants/REF'], key=len)))
    # print(len(data['variants/REF']))
    print(data['samples'])