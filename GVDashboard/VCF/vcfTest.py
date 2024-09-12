# Simple script that contains tools for testing vcf file reading and writing 

import allel as al # Used for VCF file manipulation
import os
#from pysam import VariantFile

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
    # This search can be chained (useful)
    bool_search = bool_search &(df["POS"]<15000)

    # Then get a new dataframe by indexing useing the bool search
    new_df = df[bool_search]

    # Dataframe can also be sorted like this 
    new_df = new_df.sort_values(by=["QUAL"], ascending=True)

    print(new_df)

    
    # The indexes of a dataframe can be used to access and sored rows of a genotype array (or any numpy array/matrix)
    # print("\n This is 'calldata/GT': \n",al.GenotypeArray(data['calldata/GT'])[new_df.index,:])

    #sort ascending according to index???
    # df = df.sort_index
    # print("This is sorted df: \n", df)
    # get column of dataframe
    print("This is new_df, only \"POS\": \n", new_df["POS"])
    pos_df= new_df.sort_values(by=["POS"], ascending=True) #["POS"]
    #df.sort_values(by=['Date'], ascending=False)
    print("This is sorted new_df, only \"POS\": \n", pos_df["POS"])
    count = pos_df.size
    print("This is count: \n", count)
    first_row = pos_df["POS"].iloc[[0]]
    print("This is first_row: \n", first_row)
    last_row = pos_df["POS"].iloc[[-1]] #, ['POS']]
    print("This is last: \n", last_row)
    
    # for index, pos_df["POS"] in enumerate(pos_df):
    #     print(index, pos_df)
    

    

    print("This is data['samples']: \n", data['samples'])

    eg_sample = data['samples'][0]

    #============ String stuff =================
    # Get only the numbers from a string
    numb_str = ''.join([s for s in eg_sample if s.isdigit()])
    print("This is numb_str: \n", numb_str)

    # Now remove numb_str from the main sring 
    leters = eg_sample.strip(numb_str)
    print("This is leters: \n", leters)

    # now make sample an intager
    int(numb_str)
    print("This is numb_str: \n", numb_str)
    
    # print("Starting conversion")
    # al.vcf_to_csv('./Data/afr-small.vcf', './Data/example.csv', fields='*')
    # print("done")