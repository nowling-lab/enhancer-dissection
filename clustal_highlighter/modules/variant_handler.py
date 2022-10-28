import pandas as pd
import pathlib
import gzip

from clustal_highlighter.modules.logger import *
logger = logging.getLogger()

def read_vcf_into_dataframe(file_path):
    file_extension = pathlib.Path(file_path).suffix
    file_opener = open
    open_as = 'r'
    if file_extension == '.gz':
        open_as = 'rt'
        file_opener = gzip.open

    comment_rows = 0
    with file_opener(file_path, open_as) as variant_data:        
        for line in variant_data:
            comment_rows += 1
            if line[0] == '#':
                if '#CHROM' in line:
                    break
                else:
                    pass
        
    return pd.read_csv(file_path, sep='\t', skiprows=(comment_rows-1), memory_map=True)


def find_variants_in_sequnce(seq_start, seq_end, df): #df is pandas dataframe
    variants = []
 
    variant_data = df.loc[(df['POS'] >= seq_start) & (df['POS'] <= seq_end)]
    
    for row in variant_data[:].to_numpy().tolist():
        variants.append(calculate_variant_stats(row))
    
    return variants

def calculate_variant_stats(logger, variant_Row, variant_dict, max_missing_frac=None, min_allele_freq=None):
    ref = variant_Row[3]
    alt = variant_Row[4]
    pos = variant_Row[1]
    variant_amount = len(variant_Row[9:]) 
    #0/1:0.34:11,21:31:99:0:638,0,340 takes that string and splits it into "1/0" and then takes that and makes it the tuple (1,0)
    #variant data starts from index 9, so we take 9 to the end... 
    cleaned_samples = [tuple(variant.split(':',1)[0].split('/')) for variant in variant_Row[9:]]
    # Each sample has 2 chromosome, so 2 reads for each position to find its allele 
    # I sum these separatley to account for errornous cases like 1/. or ./0
 
    #./. is missing data
    num_alt_allele_appearances = 0
    missing_allele_count = 0
    valid_allele_count = 0
    for sample in cleaned_samples:
        for allele in sample:
            if allele == "1":
                num_alt_allele_appearances += 1
                
            if allele == '.':
                missing_allele_count += 1
            else:  
                valid_allele_count += 1
        
    alt_percent = (num_alt_allele_appearances)/(valid_allele_count-missing_allele_count)
    ref_percent = 1-alt_percent

    if max_missing_frac is not None:
        num_samples = variant_amount
        max_individuals_missing = int(max_missing_frac * num_samples)
        if missing_allele_count >= max_individuals_missing:
            return
        
    if min_allele_freq is not None:
        min_percent = min((ref_percent, alt_percent))
        if min_percent <= min_allele_freq:
            return
    
    #Program short circuits on the above conditions and variant is not added to dictionary...
    variant_dict[int(pos)] = (ref, alt, ref_percent, alt_percent, len(cleaned_samples), missing_allele_count)

def get_peak_locations(file_path):
    peak_locations = {}
    column_names = ['chrom', 'start', 'end']
    df = pd.read_csv(file_path, sep="\t", usecols=range(3), names=column_names)
    
    df = df.groupby(['chrom'])
    chromosomes = df.groups.keys()
    for chromosome in chromosomes:
        group = df.get_group(chromosome)
        peak_locations[chromosome] = group[['start', 'end']].to_numpy().tolist()
    
    return peak_locations

def get_seq_string(file_path: str, seq_location: tuple) -> list:
    seq = []
    with open(file_path, 'r') as file:
        header = file.readline()
        char_pos = 0
        for line in file:
            for char in line:
                char_pos += 1
                if char_pos >= seq_location[0] and char_pos <= seq_location[1]:
                    seq.append((char, char_pos))
                elif char_pos > seq_location[1]:
                    break
                else:
                    pass
            if char_pos > seq_location[1]:
                pass

    return seq, header

def read_variant_stats(file_path: str) -> dict:
    comment_rows = 0
    with open(file_path, 'r') as variant_data:        
        for line in variant_data:
            comment_rows += 1
            if line[0] == '#':
                if '#CHROM' in line:
                    break
                else:
                    pass
        
    df = pd.read_csv(file_path, sep='\t', skiprows=(comment_rows-1))
    return df

def generate_variant_dict(seq_start, seq_end, df, logger, max_missing_frac=None, min_allele_freq=None): #df is pandas DataFrame
    variant_dict = {}
 
    variant_data = df.loc[(df['POS'] >= seq_start) & (df['POS'] <= seq_end)]
    
    for row in variant_data[:].to_numpy().tolist():
        calculate_variant_stats(logger, row, variant_dict, max_missing_frac, min_allele_freq)
    
    return variant_dict

def generate_pi_dict(path_to_diversity_file):
    diversity_df = pd.read_csv(path_to_diversity_file, sep='\t', header=0)
    diversity_pos_score = {}
    def add_to_dict(element, pi_score, dictionary):
        dictionary[element] = pi_score

    [add_to_dict(element, pi_score, diversity_pos_score) for element, pi_score in zip(diversity_df['POS'], diversity_df['PI'])]
    
    return diversity_pos_score

def read_fasta_file(file_path):
    #Reads in a fasta file. Standard stuff
    sequence_dictionary = {}
    sequence = None
    sequence_name = None
    with open(file_path) as f:
        for line in f:
            if '>' in line:
                header = line.split()[0]

                if sequence_name == None:
                    sequence = None
                    sequence_name = header[1:].strip()
                else:
                    sequence_dictionary[sequence_name] = sequence
                    sequence_name = header[1:].strip()
                    sequence = None
            else:
                if sequence == None:
                    sequence = line.strip()
                else:
                    sequence += line.strip() 
    
        sequence_dictionary[sequence_name] = sequence
    return sequence_dictionary
            
