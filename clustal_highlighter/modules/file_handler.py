import os
import pandas as pd

get_reverse = {
        'A':'T',
        'T':'A',
        'G':'C',
        'C':'G'
    }

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
                strand = line_split[5]
                matched_sequence = line_split[-1]
                if strand == "-":
                    matched_sequence = reverse_comp(matched_sequence)

                if seq_name not in sequence_name_dict:
                    sequence_name_dict[seq_name] = []
                    sequence_name_dict[seq_name].append((start, stop, motif_alt_id, matched_sequence))
                else:
                    sequence_name_dict[seq_name].append((start, stop, motif_alt_id, matched_sequence))  
    return sequence_name_dict

def reverse_comp(sequence):
    global get_reverse
    rev_seq = sequence[::-1]
    rev_comp = ''
    for char in rev_seq:
        rev_comp += get_reverse[char]
    
    return rev_comp

def read_diverse_fimo_file(file_path):
    fimo_df = pd.read_csv(file_path, sep='\t', comment="#")
    fimo_df.drop(fimo_df.tail(3).index, inplace=True)
    return fimo_df

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

