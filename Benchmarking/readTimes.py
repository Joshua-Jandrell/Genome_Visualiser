import os
from config import *
import allel as al

class TTest():
    def __init__(self):
        pass
    def transform_fields(self,arg):
        print("yay")
        print(arg)
    def transform_chunk(self,arg):
        print("oooh")
        print(arg)

# with open(os.path.join(DATA_FOLDER,"afr.vcf.gz"), mode='r') as vcf:
#     print(vcf.readline())
PATH = 'afr.vcf.gz'

heads = al.read_vcf_headers(os.path.join(DATA_FOLDER,'afr.vcf.gz'))
print(f"There are {len(heads.samples)} samples")
#data = al.read_vcf(os.path.join(DATA_FOLDER,'afr.vcf.gz'), chunk_length=2000, region="9:10000-11000",transformers=TTest())
#fields, samples, headers, it = al.iter_vcf_chunks(os.path.join(DATA_FOLDER,'afr.vcf.gz'), chunk_length=5000)
#print(data)
# print("==========")
# print(it.__next__())

# print("==========1")
# print(it.__next__())

# for i in it:
#     print(i)

#al.vcf_to_hdf5(os.path.join(DATA_FOLDER,'afr.vcf.gz'), os.path.join(DATA_FOLDER,'afr.hdf5'), fields='*', overwrite=True, region="9:100000-200000")
