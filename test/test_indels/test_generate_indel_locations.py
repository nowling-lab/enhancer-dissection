import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import generate_indel_locals

#Tests the ability for read_fasta_file to read fasta formatted sequences,
#With out without indels.
def test_generate_indel_locals():
    test_indel_fasta = {'seq_1': 'TTGC---CACCTAG----',
                        'seq_2': '-TTTT',
                        'seq_3': 'TTTT-'}
    
    correct_output_dict = {'seq_1': [5,6,7,15,16,17,18],
                           'seq_2': [1],
                           'seq_3': [5]}
   
