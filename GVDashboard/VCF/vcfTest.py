# Simple script that contains tools for testing vcf file reading and writing 

import allel as al # Used for VCF file manipulation
import os

TEST_FILE = os.path.realpath("./Data/med.vcf.gz") # Path to the vcf file used for testing

def getData()->dict:
    return al.read_vcf(TEST_FILE)


if __name__ == "__main__":
    # Get data somehow....
    data = getData()
    # and make data into dataframe
    df = al.vcf_to_dataframe(TEST_FILE)

    # Construct a search query based on dataframe
    bool_search = (df["QUAL"].between(30, 35, inclusive = 'both'))
    # this earch can be chained (useful)
    bool_search = bool_search &(df["POS"]<15000)

    # then get a new dataframe by indexing useing the bool search
    new_df = df[bool_search]

    # Dataframe can also be sorted like this 
    new_df = new_df.sort_values(by=["QUAL"], ascending=True)

    print(new_df)

    
    # The idexes of a dataframe can be used to access and sored rows of a genotype array (or any numpy array/matrix)
    print(al.GenotypeArray(data['calldata/GT'])[new_df.index,:])

    # get column of dtaframe
    print(new_df["POS"])

    print(data['samples'])

    eg_sample = data['samples'][0]

    #============ String stuff =================
    # Get only the numbers form a string
    numb_str = ''.join([s for s in eg_sample if s.isdigit()])
    print(numb_str)

    # Now remove numb_str from the main sring 
    leters = eg_sample.strip(numb_str)
    print(leters)

    # now make sample an intager
    int(numb_str)
