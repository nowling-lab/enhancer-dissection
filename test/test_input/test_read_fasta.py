import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import read_fasta_file

def read_fasta_test():
    fasta = read_fasta_file('test/test_input/input_files/test_fasta.fa', False)
    print(fasta)
    #assert fasta == "hi"
    
read_fasta_test()
    
