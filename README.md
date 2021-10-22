# enhancer-disection

Tutorial:
    This program hasn't been updated to use the command-line as of yet. 
    There are various python files within this repo which do different 
    tasks. The main file that will be used is: clustal_format_highlighter.py. However, previously clustal_omega_highlightor.py and fimo_highlightor_html.py were used for output. 

    As currently we are only running clustal_format_highlighter this tutorial only partains to that.

    clustal_format_highlighter has all of the up-to date items that display in our current output. To run the format highlighter, you will need to call a single method that contains some paramters. 

    This method is the main_abstraction method.      
    
    main_abstraction(indel_fasta_path, a_only_bool, streme_tsv_path, jaspar_tsv_path, sequences_fasta_path, output_path):


    It takes in 6 parameters in it to run:
        indel_fasta_path: A file in fasta format which is the output of clustal omega.
        
        a_only_bool: A boolean condidtion to only use the a only labeled sequences for inputting indel_fasta_path and sequences_fasta_path. 

        streme_tsv_path: The path to the Fimo out fimo.tsv file when running Fimo with the streme motif on the sequences

        jaspar_tsv_path: The path to the Fimo out fimo.tsv file when running Fimo with the jaspar motif on the sequences
        
        sequences_fasta_path: A file in fasta format which is the raw seqeunces without indels or any other input

        output_path: A path to the file to output to. So for example, '~/highlights.html' will output to a linux home directory and generate the file 'highlights.html'

        Note that indel_fasta_path and sequences_fasta_path must have the exact same sequences and labels for this program to work, even if you are running clustal omega multiple times to properly formulate indels. The files must then be merged into a single file
        