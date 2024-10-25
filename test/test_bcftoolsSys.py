"""
This script contains unit tests for the bcftools file load and filter system
"""

import unittest, os, subprocess, sys, shutil

# Append src directory to system path to enable imports
try:
    from src.VCF.FileRead.bcftoolSys import *
except:
    sys.path.append('src')
    from src.VCF.FileRead import bcftoolSys


# Useful constant for file paths
AFR_SMALL_PATH = os.path.realpath('Data/afr-small.vcf.gz')

class Test_bcftoolsSetup(unittest.TestCase):

    def test_bcftools_build_exists(self):

        bcftools_path = bcftoolSys.BCFTOOLS_CMD

        # check that file exists
        self.assertTrue(os.path.isfile(bcftools_path))


    def test_bcftools_build_runs(self):
        # check that bcftools version info can be found
        exit_code = subprocess.call(f"{bcftoolSys.BCFTOOLS_CMD} --version", stdout=subprocess.DEVNULL, shell=True)

        self.assertEqual(exit_code, 0)  # An exit code of 0 indicates a successful execution 

    
    def test_bcftools_makes_index(self):
        "Check that bcftools can generate an index file."

        file_path = AFR_SMALL_PATH
        tmp_file_path = file_path+".tmp.vcf.gz"
        shutil.copy(file_path, tmp_file_path)

        index_path = tmp_file_path+".csi"

        bcftoolSys.index(tmp_file_path)
        self.assertTrue(os.path.isfile(index_path))

        os.remove(tmp_file_path)
        os.remove(index_path)

        

    def test_bcftoolSys_can_convert_files(self):
        file_path = AFR_SMALL_PATH

        new_path = bcftoolSys.convert(file_path, 'bcf')

        # New file exists
        self.assertTrue(os.path.isfile(new_path))

        # Bcftools can view new file
        exit_code = subprocess.call(f"{bcftoolSys.BCFTOOLS_CMD} view {new_path}", stdout=subprocess.DEVNULL, shell=True)
        self.assertEqual(exit_code, 0)  # An exit code of 0 indicates a successful execution 

        os.remove(new_path)

    def test_bcftools_can_make_tmp_subset_file(self):
        """Check that the bcftools system makes the subset file in the correct location."""

        file_path = AFR_SMALL_PATH
        new_path = os.path.join(os.path.dirname(AFR_SMALL_PATH),".new.file.for.testing.vcf.gz")

        new_data_path_returned = bcftoolSys.make_dataset_file(file_path, new_data_path=new_path)

        # Check that new path is the path requested
        self.assertEqual(new_path, new_data_path_returned)

        # Check that a file exists in the new path
        self.assertTrue(os.path.isfile(new_path))

        exit_code = subprocess.call(f"{bcftoolSys.BCFTOOLS_CMD} view {new_path}", stdout=subprocess.DEVNULL, shell=True)
        # NOTE: stdout=subprocess.DEVNULL is used to make sure that there is not bcftools output to the console
        self.assertEqual(exit_code, 0)  # An exit code of 0 indicates a successful execution 

        os.remove(new_path)


    # def test_bcftoolSys_compresses_files_for_setup(self):

    #     file_path = AFR_SMALL_PATH
    #     uncompressed = bcftoolSys.convert(file_path, 'vcf')

    #     # New file exists
    #     self.assertTrue(os.path.isfile(new_path))

    #     # Bcftools can view new file
    #     exit_code = subprocess.call(f"{bcftoolSys.BCFTOOLS_CMD} view {new_path}", stdout=subprocess.DEVNULL, shell=True)
    #     self.assertEqual(exit_code, 0)  # An exit code of 0 indicates a successful execution 

    #     os.remove(uncompressed)



if __name__ == "__main__":
    unittest.main()