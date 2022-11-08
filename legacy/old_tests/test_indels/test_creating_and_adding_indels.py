import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import calibrate_start_location, create_add_indel

#Tests the ability for read_fasta_file to read fasta formatted sequences,
#With out without indels.
def test_creating_and_adding_indels():
        key = "seq_1"
        test_indel_dict = {key: []}
        start_location = 10
        indel_width = 5
        
        create_add_indel(test_indel_dict, key, start_location, indel_width)
        
        indel_array = test_indel_dict[key]
        result_start_location, indel_string = indel_array[0]
        
        assert start_location == result_start_location
        assert '-----' == indel_string
