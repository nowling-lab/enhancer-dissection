from os import read
from typing import Literal


def main():
    ### INDEL FILE PATHS
    ACE1_A_indels = '/home/petersjg/Windows_Directory/indel-fasta-files/ACE1_A_Indels.fa'
    APT2_A_indels = '/home/petersjg/Windows_Directory/indel-fasta-files/APT2_A_Indels.fa'
    KLF_A_indels = '/home/petersjg/Windows_Directory/indel-fasta-files/KLF_A_Indels.fa'
    LRIM_A_indels = '/home/petersjg/Windows_Directory/indel-fasta-files/LRIM_A_Indels.fa'
    all_indels_merged = './a_only_indels/indel-fasta-files/nardini_a_only_merged.fa'
    pfin1_7051_indels = '/home/petersjg/Windows_Directory/7051_Pfin1_aligned.fasta'
    
    ### WITHOUT INDELS FILE PATHS
    ACE1_A = '/home/petersjg/Windows_Directory/a-only-fasta-files/ACE1_A.fa'
    APT2_A = '/home/petersjg/Windows_Directory/a-only-fasta-files/APT2_A.fa'
    KLF_A = '/home/petersjg/Windows_Directory/a-only-fasta-files/KLF_A.fa'
    LRIM_A = '/home/petersjg/Windows_Directory/a-only-fasta-files/LRIM_A.fa'
    pfin1_7051 = '/home/petersjg/Windows_Directory/7051_Pfin1_sequences.txt' 

    ### Nardini luciferase fragments
    nardini_fasta_all = './temp_files_pre_params/fasta_files/nardini_luciferase_fragments.fasta'
    nardini_a_only_fasta = './temp_files_pre_params/fasta_files/nardini_luciferase_fragments_A_only.fasta'

    ### Fimo file paths
    streme_motifs_nardini = './temp_files_pre_params/fimo_a_only/fimo_streme_a_only/fimo.tsv'
    jaspar_motifs_nardini = './temp_files_pre_params/fimo_a_only/fimo_jaspar_a_only/fimo.tsv'
    streme_motifs_pfin1 = '/home/petersjg/Windows_Directory/7051_Pfin1_fimo/streme/fimo.tsv'
    jaspar_motifs_pfin1 = '/home/petersjg/Windows_Directory/7051_Pfin1_fimo/jaspar/fimo.tsv'

    output_path = '/home/petersjg/Windows_Directory'
    output_file_path = output_path + '/nardini_highlights.html'

    #main_abstraction(pfin1_7051_indels, False, streme_motifs_pfin1, jaspar_motifs_pfin1, pfin1_7051, output_file_path)

    main_abstraction(all_indels_merged, False, streme_motifs_nardini, jaspar_motifs_nardini, nardini_a_only_fasta, output_file_path)
    return    

def main_abstraction(indel_fasta_path, a_only_bool, streme_tsv_path, jaspar_tsv_path, sequences_fasta_path, output_path):
    """This method abstracts the main method so other users don't need to remember which order to call functions in

    Args:
        indel_fasta_path (string): Path to the clustal omega indel file in fasta format
        a_only_bool (boolean): True or False in order to only capture A only sequences in fasta files
        streme_tsv_path (string): Path to Fimo output from running sequences with the streme motif file
        jaspar_tsv_path (string): Path to Fimo output from running sequences with the Jaspar motif file
        sequences_fasta_path (string): Path to the sequences file in fasta format
        output_path (string): Path to output file. Note this must go to a .html file: ~/highlights.html as an example
    """
    indel_fasta = read_fasta_file(indel_fasta_path, a_only_bool)
    indel_dict = generate_indel_locals(indel_fasta)
    combined_indel_dict = combine_indels(indel_dict)

    streme_motifs = read_fimo_file(streme_tsv_path)
    jaspar_motifs = read_fimo_file(jaspar_tsv_path)

    sequence_dict = read_fasta_file(sequences_fasta_path, a_only_bool)
    combined_dicts = combine_dictionaries(streme_motifs, jaspar_motifs, sequence_dict, combined_indel_dict)
    html_output = generate_html(combined_dicts)

    html_string_to_output(html_output, output_path)
    return

def generate_html(combined_dict):
    html_string = """
    <!DOCTYPE html>
    <html lang="en-US">
    <head>
        <title>Html Conversion</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="Keywords"
        content="HTML">
        <meta name="Description"
          content="This is a highlighted FIMO output thingy">
    </head>
    <body>
    <h> Legend: </h>
    <div style="background:Aqua; width:75%;"> This is for fimo run with streme.txt as the motif file </div>
    <div style="background:PaleVioletRed; width:75%"> This is for fimo run with JASPAR as the motif file </div>
    <div style="background:Plum; width:75%"> This is for when those highlighted motifs overlap </div>
    <div style=width:75%; word-wrap: break-word;> Colored &#8209;'s indicate that the indel is within a single motif. If they are not colored, then that means the indel is between two of the same (JASPAR or streme) motif </div>
     """
     # Large HTML header up top, then adds to it below with dynamic_html_string
    dynamic_html_string = "<br>"
    motif_keys = list(combined_dict.keys())
    motif_keys.sort()

    matched_sequences = {}
    first_part_key = ''
    for key in motif_keys: #Loop through all of the sequences
        key_split = key.split('_')
        first_part_key = key_split[0]

        if len(matched_sequences) > 0:
            last_key = list(matched_sequences.keys())[-1]
            last_list = list(matched_sequences[last_key])
            if key in last_list:
                continue #If this key was already done
            #we don't want to do it again so we skip. This is a clustal
            #omega format thing since we include multiple sequences 
            #per block

        matched_sequences[first_part_key] = set()
        setty = matched_sequences[first_part_key]
        for key2 in motif_keys:
            if first_part_key in key2:
                setty.add(key2)
                #finds all the like-keys. So all the KLF ones ect

    for key_to_list in matched_sequences:
        dynamic_html_string += "<br> <span> New Sequence </span>"
        key_list = list(matched_sequences[key_to_list])
        #This is the start of a new sequence in the output
        list_of_lines = []

        for key in key_list:
            line_list = [] #loops through all the keys
            combined_list = combined_dict[key]
            line = []
            for index, char_color in enumerate(combined_list):
                char, color = char_color
                if index % 70 == 0 and index != 0:
                    line_list.append(line.copy())
                    line.clear()
                line.append((char, color))
            line_list.append(line.copy())
            line.clear()
            list_of_lines.append((key, line_list.copy()))
            line_list.clear()
            #This essentially just splits the whole massive sequence into
            #Multiple 70-length sequences for clustal format


        stop = len(list_of_lines[0][1])
        counter = 0
        while counter < stop: #Loop through however many lines we got
            keys_lengths = []
            for key, row in list_of_lines:
                keys_lengths.append(len(key)) 
            
            max_len = max(keys_lengths) 
            #this last loop is to find the longest key so we can add
            #white space to other keys to make it line up properly

            dynamic_html_string += '<pre>'
            rows_to_compare = []
            for key, row in list_of_lines:
                rows_to_compare.append(row[counter])
                padding_str = generate_padding_string(max_len, key)
                #For every key that like, as in for all KLF's,
                #Grab the row and print them 
                #also adds to the rows_to_compare for when I do star comparisons 
                dynamic_html_string +=  key + padding_str + ": " 
                dynamic_html_string += convert_line_to_html(row[counter])
                dynamic_html_string += '<br>'

            padding = generate_padding_string(max_len, 'Stars')
            dynamic_html_string += 'stars' + padding + ': '
            dynamic_html_string += generate_continuity_stars(rows_to_compare)
            dynamic_html_string += '<br>' 
            dynamic_html_string += '</pre>' #this is the last block since it's excluded
            counter += 1 #From the list. 

    html_string += dynamic_html_string
    html_string += '\n</body>'
    return html_string

def generate_padding_string(max_len, key):
    ##Pads out the keys so it lines everything up properly
    padding_str = " "
    if max_len > len(key):
        padding = max_len - len(key) 
        for x in range(padding):
            padding_str += " "
    return padding_str 

def generate_continuity_stars(row_list):
    #Generates the stars for a list of 70 length strings
    star_string = ""
    for index, char in enumerate(row_list[-1]):
        chars_at_index = set()
        #Add all the characters at a single index to a set
        for row in row_list:
            chars_at_index.add(row[index][0])
            #If we have multiple chars at an index then we want empty
        if len(chars_at_index) > 1:
            star_string += ' '
        else: #else put a star there
            star_string += "*"

    return star_string

def convert_line_to_html(line):
    html_out = ""
    for char, color in line:
        if color == "purple":
            html_out += '<span style="background:Plum;">'
            html_out += char
            html_out += "</span>"
        elif color == "red" or color == "redx":
            html_out += '<span style="background:PaleVioletRed;">'
            html_out += char
            html_out += "</span>"
        elif color == "blue" or color ==  "bluex":
            html_out += '<span style="background:Aqua;">'
            html_out += char
            html_out += "</span>"
        else:
            html_out += char.upper()
    #Just generates the proper HTML styling for a given char and its color
    return html_out

def return_sequences(line):
    #Just some translating stuff from non-pre tags to pre-tags. 
    return_string = ""
    for char, color in line:
        if 'pre' in char:
            return_string += "-"
        else:
            return_string += char
    return return_string

def combine_dictionaries(motif_dict1, motif_dict2, seq_dict, indel_dict):
    #Combines all the dictionaries and indels into one single one.
    motif_keys = list(motif_dict1.keys())
    motif_keys.sort()
    combined_dict = {}

    for key in motif_keys: #Go for all keys
        combined_list = []        
        if indel_dict != None:
            indel_list = indel_dict[key]
        else:
            indel_list = {} #if not there make it 

        sequence = seq_dict[key]
        highlight_list = motif_dict1[key]
        highlight_list = sorted(highlight_list, key=lambda x: x[0])
        overlap_dict = {} #getting the sequences
        
        highlight_overlaps(highlight_list, overlap_dict, "blue")

        highlight_list2 = motif_dict2[key]
        highlight_list2 = sorted(highlight_list2, key=lambda x: x[0])
        
        highlight_overlaps(highlight_list2, overlap_dict, "red")
        #adding all the highlighting to the proper lists

        for index, char in enumerate(sequence):
            index_1_based = index + 1
            if index_1_based in overlap_dict:
                color = overlap_dict[index_1_based]
            else:
                color = "none"
                #if there is no color then put none there 
            
            for pos, indel_str in indel_list:
                #This loop colors the indels properly
                #just does logic to check if it's the same motif
                #and some other stuff to see if the indel is colored
                if pos == index:
                    if (index_1_based - 1) in overlap_dict and (index_1_based) in overlap_dict:
                        prev_color = overlap_dict[index_1_based - 1]
                        if 'x' in prev_color or 'x' in color:
                            add_indel_string_to_list(indel_str, combined_list, 'none')
                            continue                
                        if color == "purple":
                            add_indel_string_to_list(indel_str, combined_list, 'purple')
                        elif color == "red":
                            add_indel_string_to_list(indel_str, combined_list, 'red')
                        elif color == "blue":
                            add_indel_string_to_list(indel_str, combined_list, 'blue')     
                    else:
                        add_indel_string_to_list(indel_str, combined_list, 'none')                    
                    break                    
                
            #Adding tupules of character.upper() and its color to a combined list
            #This is so I can then split it up for clustal later
            if color == "purple":
                combined_list.append((char.upper(), 'purple'))
            elif color == "red" or color == "redx":
                if color == 'redx':
                    combined_list.append((char.upper(), 'redx'))
                else:
                    combined_list.append((char.upper(), 'red'))
            elif color == "blue" or color ==  "bluex":
                if color == 'bluex':
                    combined_list.append((char.upper(), 'bluex'))
                else:
                    combined_list.append((char.upper(), 'blue'))
            else:
                combined_list.append((char.upper(), 'none'))
            
            if len(indel_list) > 0:
                if index_1_based == len(sequence) and indel_list[-1][0] == len(sequence):
                    add_indel_string_to_list(indel_list[-1][1], combined_list, 'none')
            
        combined_dict[key] = combined_list

    combined_dict[motif_keys[-1]] = combined_list

    return combined_dict

def add_indel_string_to_list(indel_string, combined_list, color):
    #makes indels tupoles with colors and adds them to combined list
    for char in indel_string:
        combined_list.append(('-', color))


def generate_indel_string(indel_string):
    #This used to help with HTML formatting, but now it's 
    #Just an abstraction. I could get rid of it but it makes it a
    #little more readable with calling a method for it so it'll stay
    return_string = ""
    for char in indel_string:
        return_string += '-'

    return return_string

def combine_indels(indel_dict):
    #Indels start out as an index -> indel basis, this makes it
    #start index -> bunch of indels basis
    #This also properly finds the index where the indel needs to go in a
    #sequence where there are no indels since the indecies don't overlap
    new_indel_dict = {}
    keys = list(indel_dict.keys())
    for key in keys: #for all the keys with indels
        new_indel_dict[key] = []
        indel_list = indel_dict[key]
        
        if len(indel_list) == 0:
            continue
        start_location = indel_list[0]
        indel_width = 1
        
        for index, location in enumerate(indel_list): #then for the sequence associated to that key
            if index + 1 >= len(indel_list):
                if indel_width == 1:
                    start_location = location
                break #do a bunch of logic lmao it jut looks through and combines
            #the indels into one string, calibrates the start location and
            #then makes that into a new indel dict that has 
            #start_index -> ------ instead of index -> - in there...
            elif int(indel_list[index + 1]) - int(indel_list[index]) == 1:
                    if indel_width == 1:
                        start_location = location
                    indel_width += 1
            elif indel_width > 0:
                if indel_width == 1:
                    start_location = location
                start_location = calibrate_start_location(start_location, new_indel_dict, key)
                create_add_indel(new_indel_dict, key, start_location - 1, indel_width)                
                indel_width = 1
        indel_list = new_indel_dict[key]
        if indel_width > 0 and len(indel_list) == 0:
            start_location = calibrate_start_location(start_location, new_indel_dict, key)
            create_add_indel(new_indel_dict, key, start_location - 1, indel_width)
        elif indel_list[-1][0] != start_location:
            start_location = calibrate_start_location(start_location, new_indel_dict, key)
            create_add_indel(new_indel_dict, key, start_location - 1, indel_width)
    return new_indel_dict

def calibrate_start_location(start_location, new_indel_dict, key):
    #just subtracts the previous indels from the length of the list 
    #and then makes that the new index
    indels_in_key = new_indel_dict[key]
    total_length_of_indels = 0
    for indel in indels_in_key:
        indel_string = indel[1]
        str_len = len(indel_string)
        total_length_of_indels += str_len
    
    return start_location - total_length_of_indels

def create_add_indel(new_indel_dict, key, start_location, indel_width):
    indel_string = ""
    #given an indel of length x, generate a string of that many -'s
    for x in range(indel_width):
        indel_string += "-"
    new_indel_dict[key].append((start_location, indel_string))

def generate_indel_locals(seqs_with_indels):
    #inital generations of index -> location list
    keys = list(seqs_with_indels.keys())
    indel_locations = {}
    for key in keys:
        if key not in indel_locations:
            indel_locations[key] = []
        
        seq = seqs_with_indels[key]
        for index, char in enumerate(seq):
            if char == '-':
                indel_locations[key].append(index + 1)

    return indel_locations

def html_string_to_output(html_string, outputdir):
    #just writes the html string to out
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

def read_fasta_file(file_path, only_A):
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

def read_fimo_file(file_path):
    #Reads in a fimo file, standard stuff
    sequence_name_dict = {}
    with open(file_path) as f:
            header = f.readline() #to get rid of it
            for line in f:
                if len(line) <= 1:
                    return sequence_name_dict
                line_split = line.split()
                seq_name = line_split[2]
                start = int(line_split[3])
                stop = int(line_split[4])
                if seq_name not in sequence_name_dict:
                    sequence_name_dict[seq_name] = []
                    sequence_name_dict[seq_name].append((start, stop))
                else:
                    sequence_name_dict[seq_name].append((start, stop))  
    return sequence_name_dict

def highlight_overlaps(highlight_list, overlap_dict, color):
    #highlights the overlaps between the two motif files output
    #so generates the purple and colorx codes so that I know
    #where different motifs overlap essentially 
    for highlight in highlight_list:
            start, end = highlight
            for x in range(int(start), int(end) + 1):
                if x in overlap_dict:
                    ch_color = overlap_dict[x]
                    
                    if 'x' in ch_color:
                        ch_color = ch_color[:-1]

                    if color != ch_color:
                        overlap_dict[x] = "purple"
                    elif color == ch_color:
                        overlap_dict[x] = color + 'x'
                else:
                    overlap_dict[x] = color


main()