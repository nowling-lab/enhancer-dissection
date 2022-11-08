from Bio.Seq import Seq

def main():
    nardini_fasta_all = './temp_files_pre_params/fasta_files/nardini_luciferase_fragments.fasta'
    seq_dict = read_fasta_file(nardini_fasta_all, False)
    seq_dict = reverse_compliment_B_seqs(seq_dict)
    
    separate_key_types = {}
    for key in seq_dict:
        split_key = key.split('_')
        group = split_key[0]
        if group in separate_key_types:
            separate_key_types[group].append(key)
        else:
            separate_key_types[group] = [key]
    
    for group in separate_key_types:
        print_key_group(group, separate_key_types[group], seq_dict)
    
    
        
    return

def print_key_group(group, keys, sequence_dictionary):
    output_file = '/home/petersjg/windows_directory/nardini_groups/' + group + ".fa"
    file = open(output_file, 'w')
    output_string = ""
    for key in keys:
        new_key = ""
        if '_B' in key:
            new_key += key[:-1]
            new_key += 'A'
        else:
            new_key = key
        output_string += '>' + new_key + '\n'
        output_string += sequence_dictionary[key] + '\n\n'
    
    file.write(str(output_string))
        

def reverse_compliment_B_seqs(seq_dict):
    keys = list(seq_dict.keys())
    new_seq_dict = {}
    for key in keys:
        new_seq_dict[key] = ""
        seq = seq_dict[key]
        if '_B' in key or '_b' in key:
            seq = Seq(seq)
            seq = seq.reverse_complement()
        new_seq_dict[key] = seq
    return new_seq_dict

def output_A_seqs(fasta, output, keys):
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

def read_fasta_file(file_path, only_A):
    sequence_dictionary = {}
    sequence = None
    sequence_name = None
    with open(file_path) as f:
        for line in f:
            if '>' in line:
                header = line
                split_header = header.split()                   

                if sequence_name == None:
                    sequence = None
                    sequence_name = split_header[0]
                    sequence_name = sequence_name[1:]
                else:
                    if ('_A' or '_a') in sequence_name or not only_A:
                        sequence_dictionary[sequence_name] = sequence
                    sequence_name = split_header[0]
                    sequence_name = sequence_name[1:]
                    sequence = None
            else:
                if sequence == None:
                    sequence = line.strip()
                else:
                    sequence += line.strip() 
    if ('_A' or '_a') in sequence_name or not only_A:
        sequence_dictionary[sequence_name] = sequence
    return sequence_dictionary

main()