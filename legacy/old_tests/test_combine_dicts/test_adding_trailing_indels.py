import sys
import os
from typing import Sequence, overload

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import add_trailing_indels

def test_adding_trailing_indels():    
    overlap_dict = {1: ('blue', 'motif_1'), 2: ('bluex', 'motif_1, motif_2'), 
                      3: ('blue', 'motif_2'), 4: ('blue','motif_3'),
                      5: ('purple', 'Streme is: motif_3. Jaspar is motif_4'),
                      6: ('redx', 'motif_4, motif_5'), 7: ('red', 'motif_5'),
                      8: ('red', 'motif_6')}
    
    indel_list = [(1,'-'),(2, '-'), (4, '-'), (6, '-'), (8, '---')]
    
    test_sequence = 'TTGTGCTC'
    combined_list = []
    
    for index, char in enumerate(test_sequence):
        index_1_based = index + 1
        if index_1_based in overlap_dict:
            color, tooltip_str = overlap_dict[index_1_based]
        else:
            color = "none"
            tooltip_str = ""
    
        add_trailing_indels(indel_list, index_1_based, test_sequence, combined_list)
        
    correct_output = [('-', 'none'), ('-', 'none'), ('-', 'none')]
    
    assert combined_list == correct_output
   