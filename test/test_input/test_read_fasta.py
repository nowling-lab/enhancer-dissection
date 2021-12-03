import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import read_fasta_file

#Tests the ability for read_fasta_file to read fasta formatted sequences,
#With out without indels.
def test_read_fasta():
    one = ('ACE1_Fd03_1_A','TTGTGCTCGGATTGCTATGAATCCTTCAACCGCT')
    two = ('ACE1_Fd05_3_A','TTGTGCTCGGATTGCTATGAATCCTTCAACCGCT')
    three = ('ACE1_Ng3_1_A','TTGTGCTCGGATTGCTATG----CTTCAACCGCT')
    output_list = (one, two, three)
    fasta = read_fasta_file('test/test_input/input_files/test_fasta.fa', False)
    keys = fasta.keys()
    assert len(keys) == len(output_list)
    for index, key in enumerate(keys):
        seqeunce = fasta[key]
        correct_name, correct_sequence = output_list[index]
        assert key == correct_name
        assert seqeunce == correct_sequence
