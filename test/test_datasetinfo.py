"""
This script contains unit tests for the bcftools file load and filter system
"""

import unittest, os, subprocess, sys, shutil

# Append src directory to system path to enable imports
try:
    from src.VCF.filterInfo import DataSetInfo
except:
    sys.path.append('src')
    from src.VCF.filterInfo import DataSetInfo


# Useful constant for file paths
MED_PATH = os.path.realpath('Data/med.vcf.gz')

class Test_datasetInfo(unittest.TestCase):

    def test_datsetInfo_make_tmp_file_for_large_set(self):
        """Check that the dataset info object creates a temporary subset file in the correct location."""

        # Make dataset
        dataset:DataSetInfo = DataSetInfo(MED_PATH)

        # call get_data to trigger dataset tmp file creation 
        data = dataset.get_data() # when get data is called a tmp path is made with bcftools

        # the tmp file that the dataset should be saved to
        tmp_file_path = dataset._save_path

        # Check that tmp file exists 
        self.assertTrue(os.path.isfile(tmp_file_path))

        # Check that data was read from tmp file path
        self.assertFalse(data is None)



if __name__ == "__main__":
    unittest.main()