import sys
import os
from typing import overload

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import color_characters

def test_color_characters():    
    overlap_dict = {1: ('blue', 'motif_1'), 2: ('bluex', 'motif_1, motif_2'), 
                      3: ('blue', 'motif_2')}
        
    test_sequence = 'TTG'
    combined_list = []
    
    for index, char in enumerate(test_sequence):
        index_1_based = index + 1
        if index_1_based in overlap_dict:
            color, tooltip_str = overlap_dict[index_1_based]
        else:
            color = "none"
            tooltip_str = ""
    
        color_characters(color, combined_list, char, tooltip_str)    
        
    correct_output = [('T', 'blue', 'motif_1'),('T', 'bluex', 'motif_1, motif_2'),('G', 'blue', 'motif_2')]
    
    assert combined_list == correct_output
   
    return
