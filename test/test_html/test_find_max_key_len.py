import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import find_max_key_length

def test_find_max_key_len():
    line_list = [('seq_1', [[('A', 'None'), ('B', 'None'), ('C', 'None')], [('D', 'None')]]),
                 ('sequences_2', [[('E', 'None'), ('F', 'None'), ('G', 'None')], [('H', 'None')]])]
   
    max_len = find_max_key_length(line_list)
    
    assert max_len == 11