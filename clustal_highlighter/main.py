import sys
import os

sys.path.append(os.getcwd())

from clustal_highlighter.modules.file_handler import *
from clustal_highlighter.modules.highlights import Highlights
from clustal_highlighter.modules.character import Character


def main():
    if len(sys.argv) == 6:
        indel_fasta_path = sys.argv[1]
        streme_tsv_path = sys.argv[2]
        jaspar_tsv_path = sys.argv[3]
        sequences_fasta_path = sys.argv[4]
        output_path = sys.argv[5]

        main_abstraction(indel_fasta_path, streme_tsv_path,
                         jaspar_tsv_path, sequences_fasta_path, output_path)
    else:
        print("Invalid number of sys arguments, these need to be: \n" +
              "Path to indel fasta (if N/A just use the fasta file), fimo ran with streme(tsv), fimo ran with jaspar(tsv), the fasta file with sequences and the output path for the html")


def main_abstraction(indel_fasta_path, streme_tsv_path, jaspar_tsv_path, sequences_fasta_path, output_path):
    
    
    test_highlight = Highlights(sequences_fasta_path)
    
    test_highlight.add_highlights('Streme', streme_tsv_path, 'Blue')
    test_highlight.add_highlights('Jaspar', jaspar_tsv_path, 'Red')
    test_highlight.add_indels(indel_fasta_path)
    
    html_output = test_highlight.generate_html_file()
    
    html_string_to_output(html_output, output_path)
    
    #indel_fasta = read_fasta_file(indel_fasta_path)
    
    #indel_dict = generate_indel_locals(indel_fasta)
    # combined_indel_dict = combine_indels(indel_dict) First iteration without indels

    #streme_motifs = read_fimo_file(streme_tsv_path)
    #jaspar_motifs = read_fimo_file(jaspar_tsv_path)

    #sequence_dict = read_fasta_file(sequences_fasta_path)

    return


def generate_indel_locals(seqs_with_indels):
    # inital generations of index -> location list
    keys = list(seqs_with_indels.keys())
    indel_locations = {}
    for key in keys:
        if key not in indel_locations:
            indel_locations[key] = []

        seq = seqs_with_indels[key]

        for index, char in enumerate(seq):
            if char == '-':
                indel_locations[key].append(index + 1)

    return indel_locations


main()
