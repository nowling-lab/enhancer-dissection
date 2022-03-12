import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.modules.character import Character

#Tests the ability for read_fasta_file to read fasta formatted sequences,
#With out without indels.
def test_html_string():
        #Character only
        char_1 = Character('A')
        assert char_1.to_string() == 'A'
   
        #Class Color Only
        char_2 = Character('A')
        char_2.set_color('blue')
        
        correct_output = '<span class="blue">A</span>'
        assert char_2.to_string() == correct_output
        
        #Color and Tooltip
        char_3 = Character('A')
        char_3.add_motif('Test', 'motif_1', 'blue') #Will set color as well
        
        correct_output = '<span class="blue" data-toggle="tooltip" data-animation="false" title = " Test is: motif_1">A</span>'
        assert char_3.to_string() == correct_output
        
        char_3.html_string = None
        
        char_3.add_motif("Test2", 'motif_2', "red")
        correct_output = '<span class="purple" data-toggle="tooltip" data-animation="false" title = " Test is: motif_1 Test2 is: motif_2">A</span>'
        print(char_3.to_string())
        assert char_3.to_string() == correct_output