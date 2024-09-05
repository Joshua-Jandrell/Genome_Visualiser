# Simple script that contains tools for testing vcf file reading and writing 

import allel as al # Used for VCF file manipulation
import os

TEST_FILE = os.path.realpath("./Data/med.vcf.gz") # Path to the vcf file used for testing

def getData()->dict:
    return al.read_vcf(TEST_FILE)


if __name__ == "__main__":
    data = getData()
    df = al.vcf_to_dataframe(TEST_FILE)
    print(data.keys())
    bool_search = (df["QUAL"].between(30, 35, inclusive = 'both')) & (df["POS"]<15000)
    new_df = df[bool_search]
    print(new_df)

    print(al.GenotypeArray(data['calldata/GT'])[bool_search,:])

    # print(len(max(data['variants/REF'], key=len)))
    # print((max(data['variants/REF'], key=len)))
    # print(len(data['variants/REF']))
    # print(len(data['samples']))