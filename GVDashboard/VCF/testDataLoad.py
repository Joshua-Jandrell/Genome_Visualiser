"""
Unit tests for data load sand peek systems
"""
import unittest,os
from dataLoad import peek_vcf_data

MED_PATH = os.path.realpath('Data/med.vcf.gz')
AFR_SMALL_PATH = os.path.realpath('Data/afr-small.vcf.gz')

class Test_peek_vcf_data(unittest.TestCase):
    def test_unformated_chr_number_is_found(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH)
        self.assertEqual(afr_small['CHROM/number'], 9)

    def test_formated_chr_number_is_found(self):
        med = peek_vcf_data(MED_PATH)
        self.assertEqual(med['CHROM/number'], 1)
    def test_peek_gets_chr_format(self):
        med = peek_vcf_data(MED_PATH)
        self.assertEqual(med['CHROM/prefix'],"chr")

    def test_peek_gets_fist_pos(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH)
        self.assertEqual(afr_small['POS/first'], 10163)

    def test_peek_gets_fist_pos(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH)
        self.assertEqual(afr_small['POS/first'], 10163)

    def test_peek_gets_last_pos_not_at_end(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH, 1747)
        self.assertEqual(afr_small['POS/last'], 102814)

    def test_peek_gets_last_pos_at_end(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH, 1749)
        self.assertEqual(afr_small['POS/last'], 102827)

    def test_peek_gets_last_pos_exactly_at_end(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH, 1748) # Note 1748 is exactly at the end (fringe case)
        self.assertEqual(afr_small['POS/last'], 102827)

    def test_peek_detected_when_at_end(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH, 5000)
        self.assertTrue(afr_small['POS/at_end'])

    def test_peek_detected_when_exactly_at_end(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH, 1748) # Note 1748 is exactly at the end (fringe case)
        self.assertTrue(afr_small['POS/at_end'])

    def test_peek_detected_when_not_at_end(self):
        afr_small = peek_vcf_data(AFR_SMALL_PATH, 1747)
        self.assertFalse(afr_small['POS/at_end'])

    def test_peek_gets_sample_count(self):
        med = peek_vcf_data(MED_PATH, 10)
        self.assertEqual(med['samples/count'], 4)

if __name__ == "__main__":
    unittest.main()