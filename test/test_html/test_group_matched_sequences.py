import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import group_matched_sequences

def test_group_matched_sequences():
    keys = ['Seq_1', 'Seq_2', 'Seq_3', 'alt_1', 'alt_2']
    matched_sequences = {}
    for key in keys:
        group_matched_sequences(matched_sequences, keys, key)
    
    assert "Seq" in matched_sequences.keys()
    assert 'alt' in matched_sequences.keys()
    
    seq_seqs = matched_sequences['Seq']
    assert len(seq_seqs) == 3
    alt_seqs = matched_sequences['alt']
    assert len(alt_seqs) == 2        
    