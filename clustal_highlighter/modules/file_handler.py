import os
import pandas as pd

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

def read_fimo_file(file_path):
    #Reads in a fimo file, standard stuff
    sequence_name_dict = {}
    if not os.path.isfile(file_path):
        print("Fimo file not found, check input parameters")
    with open(file_path) as f:
            header = f.readline() #to get rid of it
            for line in f:
                if len(line) <= 1 or '#' in line:
                    if len(sequence_name_dict) > 0:
                        return sequence_name_dict
                    else: 
                        return None
                line_split = line.split()
                seq_name = line_split[2]
                start = int(line_split[3].strip())
                stop = int(line_split[4].strip())
                motif_alt_id = line_split[1]

                if seq_name not in sequence_name_dict:
                    sequence_name_dict[seq_name] = []
                    sequence_name_dict[seq_name].append((start, stop, motif_alt_id))
                else:
                    sequence_name_dict[seq_name].append((start, stop, motif_alt_id))  
    return sequence_name_dict

def read_diverse_fimo_file(file_path):
    fimo_df = pd.read_csv(file_path, sep='\t', comment="#")
    fimo_df.drop(fimo_df.tail(3).index, inplace=True)
    return fimo_df

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

def generate_variant_dict(seq_start, seq_end, df, max_missing_frac=None, min_allele_freq=None): #df is pandas DataFrame
    variant_dict = {}
 
    variant_data = df.loc[(df['POS'] >= seq_start) & (df['POS'] <= seq_end)]
    
    for row in variant_data[:].to_numpy().tolist():
        calculate_variant_stats(row, variant_dict, max_missing_frac, min_allele_freq)
    
    return variant_dict

def calculate_variant_stats(variant_Row, variant_dict, max_missing_frac=None, min_allele_freq=None):
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
    missing_allele = False
    num_missing_alleles = 0
    for sample in cleaned_samples:
        ref_val, alt_val = sample
        try:
            ref_1 += int(ref_val)
        except:
            missing_allele = True
            pass
        #2 blocks so one of them doesn't not get added if it was a 1...
        try:
            alt_1 += int(alt_val)     
        except:
            missing_allele = True
            pass
        
        if missing_allele:
            num_missing_alleles += 1
            missing_allele = False
    
    ref_percent = (ref_1 + alt_1)/(2*variant_amount)
    alt_percent = 1-ref_percent

    if max_missing_frac is not None:
        num_samples = variant_amount
        max_individuals_missing = int(max_missing_frac * num_samples)
        if num_missing_alleles >= max_individuals_missing:
            return
        
    if min_allele_freq is not None:
        min_percent = ref_percent if ref_percent < alt_percent else alt_percent
        if min_percent <= min_allele_freq:
            return
        
    #Program short circuits on the above conditions and variant is not added to dictionary...
    variant_dict[int(pos)] = (ref, alt, ref_percent, alt_percent)    

  #print(variant_Row[0:9]) This can be used if I want to make the code more human readable...
    # appearances = {
    #     'chromosome': chromosome,
    #     'position': pos,
    #     'ref_char': ref,
    #     'alt_char': alt,
    #     'ref_percent': ref_percent,
    #     'alt_percent': 1-ref_percent
    # } Ideal Appearances. Just to get it to work we use other.
                #1 index to 0 index

def __DEPREICATED_read_variant_stats(file_path: str) -> dict:
    variant_dict = {}
    df = pd.read_excel(file_path)
    df_list = list(df.itertuples(index=False, name=None))
    
    for line in df_list:
            pos = line[1]
            variant_dict[pos] = (line[3], line[5], line[10], line[11])
    return variant_dict
    
def html_string_to_output(html_string, outputdir):
    #just writes the html string to out
    outputdir = os.path.expanduser(outputdir)
    output = open(outputdir, 'w')
    output.write(html_string)
    output.close

def output_A_seqs(fasta, output, keys):
    #output but with sequences that have A only
    for key in keys:
        seq = fasta[key]
        temp_output_string = ">" + key + "\n"
        for index, char in enumerate(seq):
            if index % 80 == 0 and index > 0:
                temp_output_string += "\n"
                temp_output_string += char
            else:
                temp_output_string += char

        output.write(temp_output_string + '\n\n\n')
    output.close()

