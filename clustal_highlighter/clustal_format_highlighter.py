import sys
import os

sys.path.append(os.getcwd())

from clustal_highlighter.modules.file_handler import *

def main():
    
    if len(sys.argv) == 6:
        indel_fasta_path = sys.argv[1]
        streme_tsv_path = sys.argv[2]
        jaspar_tsv_path = sys.argv[3]
        sequences_fasta_path = sys.argv[4]
        output_path = sys.argv[5]
        main_abstraction(indel_fasta_path, streme_tsv_path, jaspar_tsv_path, sequences_fasta_path, output_path)
    else: 
        print("Invalid number of sys arguments, these need to be: \n" +
              "Path to indel fasta (if N/A just use the fasta file), fimo ran with streme(tsv), fimo ran with jaspar(tsv), the fasta file with sequences and the output path for the html")
    
    return    

def main_abstraction(indel_fasta_path, streme_tsv_path, jaspar_tsv_path, sequences_fasta_path, output_path):
    """This method abstracts the main method so other users don't need to remember which order to call functions in

    Args:
        indel_fasta_path (string): Path to the clustal omega indel file in fasta format
        a_only_bool (boolean): True or False in order to only capture A only sequences in fasta files
        streme_tsv_path (string): Path to Fimo output from running sequences with the streme motif file
        jaspar_tsv_path (string): Path to Fimo output from running sequences with the Jaspar motif file
        sequences_fasta_path (string): Path to the sequences file in fasta format
        output_path (string): Path to output file. Note this must go to a .html file: ~/highlights.html as an example
    """
    indel_fasta = read_fasta_file(indel_fasta_path)

    indel_dict = generate_indel_locals(indel_fasta)
    combined_indel_dict = combine_indels(indel_dict)

    streme_motifs = read_fimo_file(streme_tsv_path)
    jaspar_motifs = read_fimo_file(jaspar_tsv_path)

    sequence_dict = read_fasta_file(sequences_fasta_path)
    combined_dicts = combine_dictionaries(streme_motifs, jaspar_motifs, sequence_dict, combined_indel_dict)
    html_output = generate_html(combined_dicts)

    html_string_to_output(html_output, output_path)
    return

def find_matched_sequences(matched_sequences, first_part_key, motif_keys):
    matched_sequences[first_part_key] = set()
    setty = matched_sequences[first_part_key]
    for key2 in motif_keys:
        is_int = True
        try:
            int(first_part_key)
        except:
            is_int = False
        
        if first_part_key in key2 and not is_int:
            setty.add(key2)
            #finds all the like-keys. So all the KLF ones ect
    return setty

def normalize_line_length(key_list, combined_dict, list_of_lines, line_length):
    for key in key_list:
        line_list = [] #loops through all the keys
        combined_list = combined_dict[key]
        line = []
        for index, char_color in enumerate(combined_list):                
            if index % line_length == 0 and index != 0:
                line_list.append(line.copy())
                line.clear()

            line.append(char_color)
            print(char_color)
        line_list.append(line.copy())
        line.clear()
        list_of_lines.append((key, line_list.copy()))
        line_list.clear()
        #This essentially just splits the whole massive sequence into
        #Multiple 70-length sequences for clustal format

def find_max_key_length(list_of_lines):
    keys_lengths = []
    for key, row in list_of_lines:
        keys_lengths.append(len(key)) 
    
    keys_lengths.append(len('stars'))
    
    max_len = max(keys_lengths) 
    return max_len
    #this last loop is to find the longest key so we can add
    #white space to other keys to make it line up properly

def compare_append_rows(row, counter, max_len, key):
    row_string = ""
    padding_str = generate_padding_string(max_len, key)
    #For every key that like, as in for all KLF's,
    #Grab the row and print them 
    #also adds to the rows_to_compare for when I do star comparisons 
    row_string +=  key + padding_str + ": " 
    row_string += convert_line_to_html(row[counter])
    row_string += '<br>'
    return row_string

def append_stars(max_len, rows_to_compare):
    padding = generate_padding_string(max_len, 'Stars')
    
    star_str = 'stars' + padding + ': '
    check_list = set()
    for index, rows in enumerate(rows_to_compare):
        check_list.add(len(rows))
    if len(rows_to_compare) > 0:
        star_str += generate_continuity_stars(rows_to_compare)
    star_str += '<br>' 
    
    return star_str

def append_position(max_len, rows_to_compare, position):
    padding = generate_padding_string(max_len, 'Pos')
    
    pos_string = 'Pos' + padding + ': Start: ' + str(position) + ","
    
     #Just an easy way to keep the loop more simple since it's +1 in the loop
    position += len(rows_to_compare[0]) - 1

    pos_string += " End: " + str(position)
    position += 1
    
    return pos_string, position

def group_matched_sequences(matched_sequences, motif_keys, key):
    key_split = key.split('_')
    first_part_key = key_split[0]

    if len(matched_sequences) > 0:
        last_key = list(matched_sequences.keys())[-1]
        last_list = list(matched_sequences[last_key])
        if key in last_list:
            return #If this key was already done
        #we don't want to do it again so we skip. This is a clustal
        #omega format thing since we include multiple sequences 
        #per block

    setty = find_matched_sequences(matched_sequences, first_part_key, motif_keys)
    
    if len(setty) == 0:
        setty.add(key)

def generate_html(combined_dict):
    html_string = html_header()
     # Large HTML header up top, then adds to it below with dynamic_html_string
    dynamic_html_string = "<br>"
    motif_keys = list(combined_dict.keys())
    motif_keys.sort()

    matched_sequences = {}
    for key in motif_keys: #Loop through all of the sequences
        group_matched_sequences(matched_sequences, motif_keys, key)
    
    for key_to_list in matched_sequences:
        dynamic_html_string += "<br> <span> New Sequence </span>"
        key_list = list(matched_sequences[key_to_list])
        #This is the start of a new sequence in the output
        list_of_lines = []

        line_length = 70
        normalize_line_length(key_list, combined_dict, list_of_lines, line_length)
        
        if(len(list_of_lines) == 0):
            stop = 1
        else:
            stop = len(list_of_lines[0][1])
        counter = 0
        position = 1
        while counter < stop: #Loop through however many lines we got
            max_len = find_max_key_length(list_of_lines)

            dynamic_html_string += '<pre>'
            rows_to_compare = []
            for key, row in list_of_lines:
                rows_to_compare.append(row[counter])
                dynamic_html_string += compare_append_rows(row, counter, max_len, key)

            ##dynamic_html_string += append_stars(max_len, rows_to_compare)
            
            position_string, position = append_position(max_len, rows_to_compare, position)
            dynamic_html_string += position_string
            
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
    for item in line:
        char = None
        color = None
        tooltip_str = None
        class_color = ""
        if len(item) == 3:
            char, color, tooltip_str = item
            if 'x' in color:
                class_color = color[:-1]
            else:
                class_color = color
            html_out += '<span class="' + class_color + '" data-toggle="tooltip" data-animation="false" title = "' + tooltip_str + '"'
        else:
            char, color = item
            if 'x' in color:
                class_color = color[:-1]
            else:
                class_color = color
            
        if 'none' not in color: #Is it possible for this not to be an -? Check if highlights without tooltip is possible
            html_out += '<span class="' + class_color + '"' 
            
        if 'none' not in color:
            html_out += '>'
            html_out += char
            html_out += "</span>"
        else:
            html_out += char
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

def generate_overlap_dict(motif_dict1, motif_dict2, key):
    highlight_list = motif_dict1[key]
    highlight_list = sorted(highlight_list, key=lambda x: x[0])
    overlap_dict = {} #getting the sequences
    
    highlight_overlaps(highlight_list, overlap_dict, "blue")

    highlight_list2 = motif_dict2[key]
    highlight_list2 = sorted(highlight_list2, key=lambda x: x[0])
    
    highlight_overlaps(highlight_list2, overlap_dict, "red")
    #adding all the highlighting to the proper lists
    
    return overlap_dict

def color_characters(color, combined_list, char, tooltip_str):
    if color == "purple":
        combined_list.append((char.upper(), 'purple', tooltip_str))
    elif color == "red" or color == "redx":
        if color == 'redx':
            combined_list.append((char.upper(), 'redx', tooltip_str))
        else:
            combined_list.append((char.upper(), 'red', tooltip_str))
    elif color == "blue" or color ==  "bluex":
        if color == 'bluex':
            combined_list.append((char.upper(), 'bluex', tooltip_str))
        else:
            combined_list.append((char.upper(), 'blue', tooltip_str))
    else:
        combined_list.append((char.upper(), 'none'))
    
def add_trailing_indels(indel_list, index_1_based, sequence, combined_list):
    if len(indel_list) > 0:
        if index_1_based == len(sequence) and indel_list[-1][0] == len(sequence):
            add_indel_string_to_list(indel_list[-1][1], combined_list, 'none')

def color_indels(indel_list, index, index_1_based, overlap_dict, combined_list, color):
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
    return

def combine_dictionaries(motif_dict1, motif_dict2, seq_dict, indel_dict):
    #Combines all the dictionaries and indels into one single one.
    motif_keys = list(motif_dict1.keys())
    motif_keys.sort()
    combined_dict = {}

    for key in motif_keys: #Go for all keys
        combined_list = []        
        
        if indel_dict != None and len(indel_dict) != 0:
            indel_list = indel_dict[key]
        else:
            indel_list = {} #if not there make it 
            
        sequence = seq_dict[key]

        overlap_dict = generate_overlap_dict(motif_dict1, motif_dict2, key)

        for index, char in enumerate(sequence):
            index_1_based = index + 1
            if index_1_based in overlap_dict:
                color, tooltip_str = overlap_dict[index_1_based]
            else:
                color = "none"
                tooltip_str = ""
                #if there is no color then put none there 
            
            #color indels here
            color_indels(indel_list, index, index_1_based, overlap_dict, combined_list, color)                  
            #Adding tupules of character.upper() and its color to a combined list
            #This is so I can then split it up for clustal later
            color_characters(color, combined_list, char, tooltip_str)
            
            #add trailing indels
            add_trailing_indels(indel_list, index_1_based, sequence, combined_list)
            
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

def highlight_overlaps(highlight_list, overlap_dict, color):
    #highlights the overlaps between the two motif files output
    #also highlights the base given color as well (color) for
    #streme and jaspar. 
    #so generates the colors per positoin so that I know
    #where motifs are and where they overlap essentially 
    for highlight in highlight_list:
            start, end, alt_motif_id = highlight
            for x in range(int(start), int(end) + 1):
                if x in overlap_dict:
                    ch_color = overlap_dict[x][0]
                    
                    if 'x' in ch_color:
                        ch_color = ch_color[:-1]

                    if color != ch_color:
                        old_color, alt_id = overlap_dict[x]
                        if 'x' in old_color:
                            old_color = old_color[:-1]
                            
                        tooltip_str = ""
                        if 'red' in old_color:
                            tooltip_str = 'Jaspar is: ' + alt_id + ', Streme is ' + alt_motif_id
                        elif 'blue' in old_color:
                            tooltip_str = 'Streme is: ' + alt_id + '. Jaspar is ' + alt_motif_id
                        overlap_dict[x] = ("purple", tooltip_str)
                    elif color == ch_color:
                        old_color, alt_id = overlap_dict[x]
                        tooltip_str = alt_id + ", " + alt_motif_id
                        overlap_dict[x] = (color + 'x', tooltip_str)
                else:
                    overlap_dict[x] = (color, alt_motif_id)


if __name__ == "__main__":
   main()