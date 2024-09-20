import os
from FileReading.readMethods import read_to_memory, read_to_dataframe, read_to_hdf5

from trackTimeMem import monitor_time
from config import *

SAVE_DIR = os.path.join(RESULT_DIR,"ReadOutputs")

if __name__ == "__main__":
    # make required directories 
    os.makedirs(SAVE_DIR, exist_ok=True)

    _times = monitor_time(fxn=lambda: read_to_memory(os.path.join(DATA_FOLDER,"afr-small.vcf")))
    print(_times),
    _times = monitor_time(fxn=lambda: read_to_dataframe(os.path.join(DATA_FOLDER,"afr-small.vcf")))
    print(_times)
    _times = monitor_time(fxn=lambda: read_to_hdf5(os.path.join(DATA_FOLDER,"med.vcf.gz"),
                                                        os.path.join(SAVE_DIR, "to_hdf5")))
    print(_times)