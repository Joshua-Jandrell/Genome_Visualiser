"""
Script used to verify that file reading occurs correctly
"""
import os, unittest
import allel as al
from FileRead import run_al_speedtests, run_bcftools_speedtests

class TestBcftoolsRead(unittest.TestCase):
    def test_case_samples_selected(self):
        case_data, ctrl_data = run_bcftools_speedtests(data_path, case_file, save_file=None,
                                                                                     chr=1, start=10492, stop=10815,
                                                                                     min_qual=25, max_qual=30,
                                                                                     n_iters=1)
        self.assertTrue(all(case_data['samples']==["NA19321","NA19323"]))
        self.assertTrue(all(ctrl_data['samples']==['NA19319', 'NA19320']))

    def test_pos_range_selected(self):
        case_data, ctrl_data = run_bcftools_speedtests(data_path, case_file, save_file=None,
                                                                                     chr=1, start=10492, stop=10815,
                                                                                     min_qual=None, max_qual=None,
                                                                                     n_iters=1)
        

        self.assertTrue(min(case_data['variants/POS'])==10492)
        self.assertTrue(min(ctrl_data['variants/POS'])==10492)
        self.assertTrue(max(case_data['variants/POS'])==10815)
        self.assertTrue(max(ctrl_data['variants/POS'])==10815)

    def test_filter_by_quality(self):
        case_data, ctrl_data = run_bcftools_speedtests(data_path, case_file, save_file=None,
                                                                                     chr=1, start=10492, stop=10815,
                                                                                     min_qual=25, max_qual=30,
                                                                                     n_iters=1)
        
        self.assertTrue(all(case_data['variants/QUAL'] == ctrl_data['variants/QUAL']))
        self.assertTrue(all(case_data['variants/QUAL'] == [28, 28]))
        
        
class TestAllelRead(unittest.TestCase):
    def test_case_samples_selected_al(self):
        case_data, ctrl_data = run_al_speedtests(data_path, case_file, save_file=None,
                                                chr=1, start=10492, stop=10815,
                                                n_iters=1)
        self.assertTrue(all(case_data['samples']==["NA19321","NA19323"]))
        self.assertTrue(all(ctrl_data['samples']==['NA19319', 'NA19320']))

    def test_pos_range_selected(self):
        case_data, ctrl_data = run_al_speedtests(data_path, case_file, save_file=None,
                                                    chr=1, start=10492, stop=10815,
                                                    n_iters=1)
        

        self.assertTrue(min(case_data['variants/POS'])==10492)
        self.assertTrue(min(ctrl_data['variants/POS'])==10492)
        self.assertTrue(max(case_data['variants/POS'])==10815)
        self.assertTrue(max(ctrl_data['variants/POS'])==10815)

    def test_filter_by_quality(self):
        case_data, ctrl_data = run_al_speedtests(data_path, case_file, save_file=None,
                                                    chr=1, start=10492, stop=10815,
                                                    min_qual=25, max_qual=30,
                                                    n_iters=1)
        
        self.assertTrue(all(case_data['variants/QUAL'] == ctrl_data['variants/QUAL']))
        self.assertTrue(all(case_data['variants/QUAL'] == [28, 28]))

if __name__ == "__main__":
    data_path = os.path.relpath('Data/med.vcf.gz')
    case_file = 'Data/med_tmp.case.tsv'

    # Make useful file for testing
    with open(case_file, mode="w") as f:
        f.write("NA19321\nNA19323")
        f.close

    unittest.main()

    os.remove(case_file)

