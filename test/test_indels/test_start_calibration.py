import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import calibrate_start_location

#Tests the ability for read_fasta_file to read fasta formatted sequences,
#With out without indels.
def test_start_calibration():
        test_indel_dict = {'seq_1': [(10, '-----'), (20, '-----'), (50, '-----')]}
        test_start_location = 100
        test_key = 'seq_1'
        correct_new_start = 85

        new_start = calibrate_start_location(test_start_location, test_indel_dict, test_key)

        assert correct_new_start == new_start
   
