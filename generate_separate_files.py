def main():
    #All the sequences in nardini
    path_to_nardini_all = '/home/petersjg/windows_directory/nardini_groups/nardini_all_a_to_b.fa'
    #All sequences and their indals from clustal
    path_to_indel_all = '/home/petersjg/windows_directory/nardini_groups/clustal_results/nardini_b_to_a_clustal.fa'
    
    #Output locations of files I would like to print to. These exist already
    ACE1_file =  '/home/petersjg/enhancer-dissection/figure4files/ACE1/ACE1.fa'
    AP_file = '/home/petersjg/enhancer-dissection/figure4files/AP/AP.fa'
    KLF_file = '/home/petersjg/enhancer-dissection/figure4files/KLF/KLF.fa'
    LRIM1_file = '/home/petersjg/enhancer-dissection/figure4files/LRIM1/LRIM1.fa'
    OVO_file = '/home/petersjg/enhancer-dissection/figure4files/OVO/OVO.fa'
    RDL_file ='/home/petersjg/enhancer-dissection/figure4files/RDL/RDL.fa'
    
    #Output locations of indels files I would like to print to. These exist already
    ACE1_indel_file =  '/home/petersjg/enhancer-dissection/figure4files/ACE1/ACE1_Indels.fa'
    AP_indel_file = '/home/petersjg/enhancer-dissection/figure4files/AP/AP_Indels.fa'
    KLF_indel_file = '/home/petersjg/enhancer-dissection/figure4files/KLF/KLF_Indels.fa'
    LRIM1_indel_file = '/home/petersjg/enhancer-dissection/figure4files/LRIM1/LRIM1_Indels.fa'
    OVO_indel_file = '/home/petersjg/enhancer-dissection/figure4files/OVO/OVO_Indels.fa'
    RDL_indel_file ='/home/petersjg/enhancer-dissection/figure4files/RDL/RDL_Indels.fa'
     
    output_files = [ACE1_file, AP_file, KLF_file, LRIM1_file, OVO_file, RDL_file]
    output_indel_files = [ACE1_indel_file, AP_indel_file, KLF_indel_file, LRIM1_indel_file, OVO_indel_file, RDL_indel_file] 
    
    generate_files_from_paths(path_to_nardini_all, output_files)
    generate_files_from_paths(path_to_indel_all, output_indel_files)    
        
    return

def generate_files_from_paths(source_path, output_list_paths):
    
    seq_dict = read_fasta_file(source_path)
    
    similar_key_dict = group_similar_keys(seq_dict)     

    for key in similar_key_dict:
        search_key = ''
        if key == 'APT2':
            search_key = 'AP'
        else:
            search_key = key
            
        for path in output_list_paths:
            if search_key in path:
                print_seq_list_to_file(similar_key_dict[key], path)
            

    return

def print_seq_list_to_file(like_sequences, file_path):
    seq_file = open(file_path, 'w')
    for seqs in like_sequences:
        fasta_string = '>' + seqs[0] + '\n' + seqs[1] + '\n\n'
        seq_file.write(fasta_string)
        
    seq_file.close()
        
    return

def group_similar_keys(seq_dict):
    key_start = ""
    similar_key_dict = {}
    for key in seq_dict.keys():
        key_split = key.split('_')                
        
        if key_start in key_split:
            similar_key_dict[key_start].append((key, seq_dict[key]))
        else:
            key_start = key_split[0]
            similar_key_dict[key_start] = [(key, seq_dict[key])] 
    
    return similar_key_dict

def read_fasta_file(file_path):
    #Reads in a fasta file. Standard stuff
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
                    sequence_dictionary[sequence_name] = sequence
                    sequence_name = split_header[0]
                    sequence_name = sequence_name[1:]
                    sequence = None
            else:
                if sequence == None:
                    sequence = line.strip()
                else:
                    sequence += line.strip() 
    sequence_dictionary[sequence_name] = sequence
    return sequence_dictionary

main()