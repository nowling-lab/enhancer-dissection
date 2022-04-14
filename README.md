# enhancer-dissection
 
This program adds highlights to a given sequence based on results of FIMO running with motif file. This is useful for showing which motifs are in a sequence and where. 

Requirements:
    Make sure FIMO is installed and added to your PATH environment variable. You can get fimo here by downloading meme-suite:https://meme-suite.org/meme/doc/download.html
    
    And then install following their installation instructions.

    To add FIMO and other programs to your path:
        1. Backup your current PATH (echo $PATH > ~/path.txt)
        2. In your home directory (cd ~/) add a folder called bin (mkdir $HOME/bin)
        3. From where you installed meme-suite cd meme-(version)/srcs
        4. Next copy fimo to that folder you created in the home directory (cp fimo ~/bin)
        5. Add the programs in that program to the PATH (export PATH="$PATH:$HOME/bin")
    
    If there are other programs you would like to add to the path in the future then adding them in bin and running step 5 again

Installing and running the software with a Python Environment:
    First go to a location where you would like to install the software with cd. Then follow these commands:

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ git clone git@github.com:nowling-lab/enhancer-dissection.git
    $ cd enhancer-dissection
    $ python setup.py install
    
    The program is then ran by calling fasta_highlighter.
    The arguments that are taken are:
        --seq-file SEQ_FILE
            Fasta formatted sequnece file
        --motif-files MOTIF_FILES [MOTIF_FILES ...]
            A list of motif_name motif_file_path tuples for all the motifs that you want in the output
        --indel-file LIST
            Fasta formatted sequence file with indels
        --outputdir OUTPUTDIR
            Output file directory

    An example of running this program is this:
     
     fasta_highlighter --seq-file /path/to/sequence/file.fasta --motif-files JASPAR /path/to/jaspar/motifs.txt streme /path/to/streme/motifs.txt