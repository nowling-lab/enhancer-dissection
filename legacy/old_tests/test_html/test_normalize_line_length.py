import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import normalize_line_length

#Tests normalizing of lines so that each line is the same length for each
#sequence
def test_normalize_line_length():
    key_list = ['seq_1', 'seq_2']
    combined_dict = {'seq_1': [('A', 'None'), ('B', 'None'), ('C', 'None'), ('D', 'None')],
                     'seq_2': [('E', 'None'), ('F', 'None'), ('G', 'None'), ('H', 'None')]}
    line_length = 3
    list_of_lines = []
    normalize_line_length(key_list, combined_dict, list_of_lines, line_length)
    
    assert list_of_lines[0][0] == 'seq_1'
    assert list_of_lines[1][0] == 'seq_2'
    
    assert len(list_of_lines[0]) == 2
    assert len(list_of_lines[1]) == 2
    
    assert len(list_of_lines[0][1][0]) == line_length
    assert len(list_of_lines[1][1][0]) == line_length
    
    assert len(list_of_lines[0][1][1]) == 1
    assert len(list_of_lines[1][1][1]) == 1
    
    
