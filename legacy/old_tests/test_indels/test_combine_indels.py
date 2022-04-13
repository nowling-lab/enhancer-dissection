import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import combine_indels

#Tests the ability for read_fasta_file to read fasta formatted sequences,
#With out without indels.
def test_combine_indels():
    indel_dict = {'seq_1': [10, 15, 16, 17, 18, 20, 25, 28, 29, 30],
                  'seq_2': [10, 11, 12, 14, 16, 17, 18],
                  'seq_3': [10]}
    output_dict = {'seq_1': [(9, '-'), (13, '----'), (14, '-'), (18, '-'), (20, '---')],
                   'seq_2': [(9, '---'), (10,'-'), (11, '---')],
                   'seq_3': [(9, '-')]}
    
    combined_indel_dict = combine_indels(indel_dict)
    
    assert output_dict == combined_indel_dict    
