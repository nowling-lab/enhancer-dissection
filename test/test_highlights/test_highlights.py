import sys
import os
import pandas as pd 
import numpy as np

sys.path.insert(0, os.getcwd())

from clustal_highlighter.modules.highlights import Highlights
from clustal_highlighter.modules.character import Character
from clustal_highlighter.modules.file_handler import html_string_to_output, read_fasta_file
from clustal_highlighter.modules.variant_handler import read_vcf_into_dataframe

#Testing the highlights object

#Global variables:
sequence_path = './test/test_highlights/test_files/test_sequence.fa'
indel_path = './test/test_highlights/test_files/test_seq_aligned.fa'
variant_data = './test/test_highlights/test_files/test_variant_data.vcf'

after_import = """Pfin1_3_3
ACGGACTTTGATGAACGCAAGGGCCGTTGCTCGAGGACACGGCGACTCGAGGGAAATCCTGTTTTCGGGG
TTGCTTTTGCTCTTACTGCTTTATTTTTTGTGCACACAGGCGAAAGAGAACCCGAAAAATAAATGTGAA
Pfin1_3_3_consensus0
ACGGACTTTGATGAACGCAAGGGCCGTTGCTCGAGGACACGGCGACTCGAGGGAAATCCTGTTTTCGGGG
TTGCTTTTGCTCTTACTGCTTTATTTTTTGTGCACACAGGCGAAAGAGAACCCGAAAAATAAATGTGAA
Pfin1_3_3_consensus1
ACGGACTTTGATGAACGCAAGGGCCGTTGCTCGAGGACACGGCGACTCGAGGGAAATCCTGTTTTCGGGG
TTGTTTTTGCTCTTACTGCTTTATTTTTTGTGCACACAGGCGAAAGGGAACCCGAAAAATAAATTTGAA
agap7051Pfin1_59_3PF
ACGGACTTTGATGAACGCAAGGGCCGTTGCTCGAGGACACGGCGACTCGAGGGAAATCCTGTTTTCGGGG
TTGCCTTTGCTCTTACTGCTTTATTTTTTTGTGCACACAGGCGAAAGAAAACCCGAAAAATAAATGGGA"""

correct_variant_data = """Variant              : <span class="variant"><span style="color:rgb(7.389900000000002,247.6101,0)" data-toggle="tooltip" data-animation="false" title ="Appearances: C: 98.551% T: 1.449%">^</span><span style="color:rgb(3.6974999999999607,251.30250000000004,0)" data-toggle="tooltip" data-animation="false" title ="Appearances: C: 99.275% A: 0.725%">^</span>  <span style="color:rgb(3.6974999999999607,251.30250000000004,0)" data-toggle="tooltip" data-animation="false" title ="Appearances: C: 99.275% T: 0.725%">^</span>                                                                <span style="color:rgb(3.6974999999999607,251.30250000000004,0)" data-toggle="tooltip" data-animation="false" title ="Appearances: G: 99.275% A: 0.725%">^</span></span><br>"""

list_of_lines = [
    ('keyshort', ['this','is','a','sequence']),
    ('keylongerthanshort', ['this','is','a','sequence']),
    ('keys', ['this','is','a','sequence']),
    ('keyactuallysuperlong', ['this','is','a','sequence'])
]

sequence_dict = read_fasta_file(sequence_path)

test_highlight = Highlights(sequence_dict) #to pass self to functions

def test_highlights():
        temp_highlight = Highlights(sequence_dict)
        
        stored_sequence = temp_highlight._to_string()
        assert stored_sequence == after_import
        
def test_max_key_length():
    max_key_len = Highlights._find_max_key_length(None, list_of_lines)
    true_max_length = len(list_of_lines[-1][0])
    
    assert max_key_len == true_max_length

def test_calculate_position():
    new_position = Highlights._calculate_position(None, 70, 1) #1 indexed, but row size is 70
    assert new_position == 70 

def test_continuinty_stars():
    str_1 = "this_is_a_test_string"
    str_2 = "this_ s_a_test_string"
    str_3 = " his_is_a_test_strin "
    char_list_1 = []
    char_list_2 = []
    char_list_3 = []
    for index, char in enumerate(str_1):
         char_list_1.append(Character(str_1[index]))
         char_list_2.append(Character(str_2[index]))
         char_list_3.append(Character(str_3[index]))
         
    true_stars = " **** ************** "
    row_list = [char_list_1, char_list_2, char_list_3]
    stars = Highlights._generate_continuity_stars(None, row_list)  
    
    assert stars == true_stars

def test_find_nearest_non_indels():
    test_seq = 'AAAAAAAAAAAB-----CAAAAAAAAAAA'
    test_seq_list = []
    for char in test_seq:
        test_seq_list.append(Character(char))
    correct_tuple = ('B', 'C') #note this is the to_string, not the object
        
    nearest_chars = Highlights._find_nearest_non_indels(None, 14, test_seq_list) #an indel is at 14
    generated_tuple = (nearest_chars[0].to_string(), nearest_chars[1].to_string())
            
    assert correct_tuple == generated_tuple
    
    test_seq = [Character('-'), Character('A')]
    correct_tuple = (None, 'A')
    nearest_chars = Highlights._find_nearest_non_indels(None, 0, test_seq)
    generated_tuple = (nearest_chars[0], nearest_chars[1].to_string())
    assert correct_tuple == generated_tuple
    
    test_seq = [Character('A'), Character('-')]
    correct_tuple = ('A', None)
    nearest_chars = Highlights._find_nearest_non_indels(None, 1, test_seq)
    generated_tuple = (nearest_chars[0].to_string(), nearest_chars[1])
    assert correct_tuple == generated_tuple

def test_variant_data():
    temp_highlights = Highlights(sequence_dict)
    vcf_df = read_vcf_into_dataframe(variant_data)
    temp_highlights.add_variant_data(vcf_df)
    variant_string = temp_highlights._append_variant_data(20, 0)
    html_string_to_output(temp_highlights.generate_html_file(), '~/test_highlight.html')
    print(temp_highlights.variant_data)
    #visually count and see if it works. 
    #assert False
    #Uncomment to see print statement above.


# Note, color characters and variant data tests rely on 
# a build of code that worked, verifying that it produced the correct output
# and then making sure the output of the function is that

# if any changes are made, these must be manually verified again
# and any strings updated so the test is consistent.

# The reason this is still helpful is it makes sure that other 
# random changes don't somehow break this code and this will
# be a smoke signal that something is wrong and needs to be looked into

test_highlights()