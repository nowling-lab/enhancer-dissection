# enhancer-dissection
 
#NOTE: Debian users please rease the warnings at the bottom of this file
 
The two programs in this project display variant data, motif data (via highlights). They differ only by their inputs. fasta_highlighter takes groups of aligned sequen es (all orientated the same way) in order to compare by the sequence data. Motifs are commonly overlayed on these. 

genome_highlighter does this but takes singular sequences given by a BED file and pulls those locations from a supplied FASTA formatted sequence file in order to display highlights on individual sequences. 

Requirements:
    Make sure FIMO is installed and added to your PATH environment variable. You can get fimo here by downloading meme-suite: https://meme-suite.org/meme/doc/download.html
    
And then install following their installation instructions.

To add FIMO and other programs to your path:
    
1. Backup your current PATH 

       $ echo $PATH > ~/path.txt
    
2. In your home directory (cd ~/) add a folder called bin (mkdir $HOME/bin)

       $ cd ~/
       $ mkdir $HOME/bin

3. From where you installed meme-suite cd meme-(version)/srcs

       $ cd meme-(version)/srcs

4. Next copy fimo to that folder you created in the home directory 
     
       $ cp fimo ~/bin
     
5. Add the programs in that program to the PATH 

       $ export PATH="$PATH:$HOME/bin"
    
If there are other programs you would like to add to the path in the future then adding them in bin and running step 5 again

Installing and running the software with a Python Environment:
    First go to a location where you would like to install the software with cd. Then follow these commands:

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ git clone git@github.com:nowling-lab/enhancer-dissection.git
    $ cd enhancer-dissection
    $ python setup.py install
    
There are 2 currently supported programs:
    
The first program is ran by calling genome_highlighter.
The arguments that are taken are:

     --seq-file SEQ_FILE   Path to fasta formatted sequence file
     --motif-files MOTIF_FILES [MOTIF_FILES ...]
                           A list of motif_name motif_file_path tuples for all the motifs that you want in the output
     --variant-data VARIANT_DATA
                           Path to VCF file containing variant data
     --peaks PEAKS         Path to BED file containing the locations of the different regions that you want highlights of (e.g. the start and end positions of enhancers)
     --output-dir OUTPUT_DIR
                           Output file directory. Will store output and be used as a working directory.
     --max-missing-frac [MAX_MISSING_FRAC]
                           0-1 float representing what percent of missing allele information makes a variant not display
     --min-allele-freq [MIN_ALLELE_FREQ]
                           0-1 float representing what minimum percent appearance an allele must have in order for a
                           variant to display
                           
 An example of running this program is as follows:
 
     $ genome_highlighter --seq-file ~/VectorBase-56_AgambiaePEST_Genome.fasta --motif-files JASPAR ~/JASPAR2020_CORE_insects_non-redundant_pfms_meme.txt streme ~/streme_motifs.txt --variant-data ~/ag1000g_2L_bfaso_coluzzii.vcf --peaks ~/X_peaks.bed 
    
The second program is ran by calling fasta_highlighter.
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
     
     $ fasta_highlighter --seq-file /path/to/sequence/file.fasta --motif-files JASPAR /path/to/jaspar/motifs.txt streme /path/to/streme/motifs.txt --outputdir /path/to/output/folder

- - -

For debian users (Not debian-based, but specifically debian) when running python setup.py install there might be a failure to install because of a missing dependency cython. This only happens on debian for some reason but can be fixed by running:

    $ pip install cython
    
And then running 

    $ python setup.py install
 
A few more times. It sometimes will break saying you don't have numpy, but just run it once or twice more and it will finish installing. 
Also be aware that the pandas installation takes a really long time but just wait it out and it will work. 
