import sys
import os
import pytest

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import read_fasta_file

@pytest.mark.sanity
def test_read_fasta():
    fasta = read_fasta_file('test/test_input/input_files/test_fasta.fa', False)
    assert fasta == "hi"

    
