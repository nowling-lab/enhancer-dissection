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
    test_highlight.add_variant_data(indel_fasta_path)
    
    # test_highlight.add_indels(indel_fasta_path)
    
    # test_highlight.add_highlights('Streme', streme_tsv_path, 'Blue')
    # test_highlight.add_highlights('Jaspar', jaspar_tsv_path, 'Red')
    
    html_output = test_highlight.generate_html_file()
    
    html_string_to_output(html_output, output_path)

    return

main()
