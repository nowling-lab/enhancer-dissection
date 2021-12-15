import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import convert_line_to_html

def test_convert_line_to_html():
    item_list = [('A', 'red'), ('B', 'blue'), ('C', 'purple', 'tip'), ('E', 'blue'), ('F', 'red'), ('G', 'none')]
    html_out = convert_line_to_html(item_list)
    print(html_out)
    
test_convert_line_to_html
    
    
#TODO BUGGED CODE. FIX PLS