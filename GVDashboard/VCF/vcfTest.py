# Simple script that contains tools for testing vcf file reading and writing 

import allel as al # Used for VCF file manipulation
import os

TEST_FILE = os.path.realpath("./Data/afr-small.vcf") # Path to the vcf file used for testing

def getData()->dict:
    return al.read_vcf(TEST_FILE)

if __name__ == "__main__":
    data = al.read_vcf(TEST_FILE)
    print(data.keys())

    #print(data['calldata/GT'][0:10,0:20])

    # print(len(max(data['variants/REF'], key=len)))
    # print((max(data['variants/REF'], key=len)))
    # print(len(data['variants/REF']))
    # print(len(data['samples']))