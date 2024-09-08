from GVDashboard.VCF.dataWrapper import VcfDataWrapper as Wrapper
from GVDashboard.VCF.vcfTest import *

data = getData()
w = Wrapper(data)
print(w.n_samples)
zygo = w.gt_data.is_hom_alt()


# Frequency of homzygos per allele
z = zygo.sum(axis=1)/w.n_samples * 100
print(z[:20]) # print first 20 entries
print(w.n_variants - len(z))

# Frequency of any mutation (note diferance between columns and rows: will fix this in the future)
zygo = w.get_zygosity()
zygo[zygo<0] = 0 # make zygosity counts strinct positive for sum (ignore missing data)
z = zygo.sum(axis=0)*100/(w.n_samples*2) # 2 times no. variants assuming dipolidicy 

print(z[:20])
print(w.n_variants - len(z))
