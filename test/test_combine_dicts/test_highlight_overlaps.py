import sys
import os
from typing import overload

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import highlight_overlaps

def test_highlight_overlaps():
    overlap_dict = {}
    highlight_list_1 = [(1,2,'motif_1'), (2,3,'motif_2'), (4,5,'motif_3')]
    highlight_list_2 = [(5,6,'motif_4'), (6,7,'motif_5')]
    
    
    highlight_overlaps(highlight_list_1, overlap_dict, 'blue')
    highlight_overlaps(highlight_list_2, overlap_dict, 'red')
    
    correct_output = {1: ('blue', 'motif_1'), 2: ('bluex', 'motif_1, motif_2'), 
                      3: ('blue', 'motif_2'), 4: ('blue','motif_3'),
                      5: ('purple', 'Streme is: motif_3. Jaspar is motif_4'),
                      6: ('redx', 'motif_4, motif_5'), 7: ('red', 'motif_5')}
    
    assert overlap_dict == correct_output
    
    return
