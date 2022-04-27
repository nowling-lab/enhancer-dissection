import pandas as pd

def read_vcf_into_dataframe(file_path):
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

def find_variants_in_sequnce(seq_start, seq_end, df): #df is pandas dataframe
    variants = []
 
    variant_data = df.loc[(df['POS'] >= seq_start) & (df['POS'] <= seq_end)]
    
    for row in variant_data[:].to_numpy().tolist():
        variants.append(calculate_variant_stats(row))
    
    return variants

def calculate_variant_stats(variant_Row):
    ref = variant_Row[3]
    alt = variant_Row[4]
    pos = variant_Row[1]
    chromosome = variant_Row[0]
    variant_amount = len(variant_Row[9:]) 
    #0/1:0.34:11,21:31:99:0:638,0,340 takes that string and splits it into "1/0" and then takes that and makes it the tuple (1,0)
    #variant data starts from index 9, so we take 9 to the end... 
    cleaned_samples = [tuple(variant.split(':', 1)[0].split('/', 1)) for variant in variant_Row[9:]]
    ref_1 = 0
    alt_1 = 0
    
    #./.
    for sample in cleaned_samples:
        ref_val, alt_val = sample
        try:
            ref_1 += int(ref_val)
        except:
            pass
        #2 blocks so one of them doesn't not get added if it was a 1...
        try:
            alt_1 += int(alt_val)     
        except:
            pass
    
    ref_percent = (ref_1 + alt_1)/(2*variant_amount)
    #print(variant_Row[0:9])
    appearances = {
        'chromosome': chromosome,
        'position': pos,
        'ref_char': ref,
        'alt_char': alt,
        'ref_percent': ref_percent,
        'alt_percent': 1-ref_percent
    }
    
    return appearances 

def get_peak_locations(file_path):
    peak_locations = {}
    df = pd.read_csv(file_path, sep=",")
    
    df = df.groupby(['seqnames'])
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

def read_fasta_file(file_path):
    #Reads in a fasta file. Standard stuff
    sequence_dictionary = {}
    sequence = None
    sequence_name = None
    with open(file_path) as f:
        for line in f:
            if '>' in line:
                header = line

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
            
