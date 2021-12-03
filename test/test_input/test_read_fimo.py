import sys
import os

sys.path.insert(0, os.getcwd())

from clustal_highlighter.clustal_format_highlighter import read_fimo_file


#This test matches the corrent outputs: one, two, three, and four
#To data gathered from read_fimo_file reading in the actual TSV.
#The inner loop is because multiple sequences can contian multiple motifs
#and as such this is calibrated to also test that function in read_fimo_file
def test_read_fimo():
    one = ('Seq_1', 0, 5, 'TEST-1')
    two = ('Seq_2', 6, 10, 'TEST-2')
    three = ('Seq_3', 10, 12, 'TEST-3')
    four = ('Seq_1', 25, 30, 'TEST-4')
    output_list = (one, two, three, four)
    fimo = read_fimo_file('test/test_input/input_files/test_fimo.tsv')
    for output in output_list:
        search_string, start, end, motif_id = output
        search_result = fimo[search_string]
        for seq in search_result:
            if motif_id == seq[-1]:
                fimo_start, fimo_end, fimo_motif_id = seq
                assert start == fimo_start
                assert end == fimo_end
                assert motif_id == fimo_motif_id 
        
    
