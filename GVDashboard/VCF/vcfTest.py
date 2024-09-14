# Simple script that contains tools for testing vcf file reading and writing 
import numpy as np
import allel as al # Used for VCF file manipulation
import os
#from pysam import VariantFile

TEST_FILE = os.path.realpath("./Data/afr-small.vcf") # Path to the vcf file used for testing

def getData()->dict:
    return al.read_vcf(TEST_FILE)


if __name__ == "__main__":
    # Get data somehow....  <<< gets .vcf file dictionary keys, from TEST _FILE 
    dict_data = getData()
    
    # Make data into a (pandas?) dataframe
    df = al.vcf_to_dataframe(TEST_FILE)

    # Construct a search query based on dataframe
    bool_search = (df["QUAL"].between(30, 35, inclusive = 'both'))
    # This search can be chained (useful)
    bool_search = bool_search &(df["POS"]<15000)

    # Then get a new dataframe by indexing useing the bool search
    new_df = df[bool_search]

    # Dataframe can also be sorted like this 
    new_df = new_df.sort_values(by=["QUAL"], ascending=True)

   # print(new_df)

    
    # The indexes of a dataframe can be used to access and sored rows of a genotype array (or any numpy array/matrix)
    print("\n Line 35: This is zygosity-pair genotype data ('calldata/GT'): \n", 
          al.GenotypeArray(dict_data['calldata/GT'])[df.index,:])

 #============ Position stuff =================
    # # get column of dataframe
    # print("This is new_df, only \"POS\": \n", new_df["POS"])
    # pos_df= new_df.sort_values(by=["POS"], ascending=True) #["POS"]
    # #df.sort_values(by=['Date'], ascending=False)
    # print("This is sorted new_df, only \"POS\": \n", pos_df["POS"])
    # count = pos_df.size
    # print("This is count: \n", count)
    # first_row = pos_df["POS"].iloc[[0]]
    # print("This is first_row: \n", first_row)
    # last_row = pos_df["POS"].iloc[[-1]] #, ['POS']]
    # print("This is last: \n", last_row) 


 #============ String stuff =================
    # Get only the numbers from a string

    #numb_str = [''.join([s for s in eg if s.isdigit()]) for eg in eg_sample]
    #print("This is numb_str: \n", numb_str)
    
    # #### Might be useful for getting a list of population letters, using a for-loop
    
    # print("This is data['samples']: \n", data['samples'])
    # eg_sample = data['samples'][0:10]
    # eg2_sample = data['samples'][-11:-1]
    # eg_sample = np.concatenate((eg_sample,eg2_sample),axis=0)
    
    # print("This is eg_sample : \n", eg_sample )
    
    # letters = [''.join([s for s in eg if not s.isdigit()]) for eg in eg_sample]
    # print("This is letters: \n", letters)

    
    #============ Population String stuff =================

    print("This is dict_data['samples']: \n", dict_data['samples'])

    #target = "NA"
    {#Find "NA in eg_sample data"
    # only_na = [target in eg for eg in eg_sample]
    # print("This is only_na for eg_samples: \n",only_na)
    }
    
    #Find "NA" in all 'samples' data
    target = "NA"
    target_samples_NA_only = [target in eg for eg in dict_data['samples']]
    print("This is finding target_samples_NA_only in dict_data['samples']: \n", target_samples_NA_only)
    
    # Get zygosity that's only "NA" from vcf data:
    
    gt = al.GenotypeArray(dict_data['calldata/GT'])[df.index,:]
    na_only = gt[:,target_samples_NA_only]
    print("This is zygosity data ('calldata/GT') from genotype_array (gt[:,samples_only_na]), for only NA population: \n",na_only)
    print("Get samples that are only NA", dict_data['samples'][target_samples_NA_only])
    #print("Get zygosity that's df[only_na]\n", df[only_na])
    
    
    

    # Now remove numb_str from the main sring 
    # letters = eg_sample.strip(numb_str)
    # print("This is letters: \n", letters)

    # population_string_list = []
    # population_string_list = population_string_list+[letters,]

    # print("This is population_string_list: \n", population_string_list)
    # # now make sample an intager
    # int(numb_str)
    # print("This is numb_str: \n", numb_str)
    
    # print("Starting conversion")
    # al.vcf_to_csv('./Data/afr-small.vcf', './Data/example.csv', fields='*')
    # print("done")