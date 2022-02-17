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

    pfin_with_indels = read_fasta_file(pfin1_7051_indels, False)
    pfin_indel_locations = generate_indel_locals(pfin_with_indels)
    new_indel_list = combine_indels(pfin_indel_locations)

    motif_dict = read_fimo_file('/home/petersjg/Windows_Directory/7051_Pfin1_fimo/streme/fimo.tsv')
    motif_dict2 = read_fimo_file('/home/petersjg/Windows_Directory/7051_Pfin1_fimo/jaspar/fimo.tsv')

    seq_dict = read_fasta_file(pfin1_7051, False)
    html_string = generate_html(motif_dict, motif_dict2, seq_dict, new_indel_list)

    html_string_to_output(html_string, './highlights.html')
    return    

def generate_html(motif_dict1, motif_dict2, seq_dict, indel_dict):
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
    dynamic_html_string = None
    motif_keys = list(motif_dict1.keys())
    motif_keys.sort()
    
    for key in motif_keys:
        if dynamic_html_string == None:
            dynamic_html_string = """<p style="font-family:'Courier New'; word-wrap: break-word; width: 75%; white-space: normal">"""
        else:
            dynamic_html_string += """<p style="font-family:'Courier New'; word-wrap: break-word; width: 75%; white-space: normal">"""
        dynamic_html_string += ">" + str(key) + "<br>"
        
        if indel_dict != None:
            indel_list = indel_dict[key]
        else:
            indel_list = {}

        sequence = seq_dict[key]
        highlight_list = motif_dict1[key]
        highlight_list = sorted(highlight_list, key=lambda x: x[0])
        overlap_dict = {}
        
        highlight_overlaps(highlight_list, overlap_dict, "blue")

        highlight_list2 = motif_dict2[key]
        highlight_list2 = sorted(highlight_list2, key=lambda x: x[0])
        
        highlight_overlaps(highlight_list2, overlap_dict, "red")

        for index, char in enumerate(sequence):
            index_1_based = index + 1
            if index_1_based in overlap_dict:
                color = overlap_dict[index_1_based]
            else:
                color = "none"
            
            for pos, indel_str in indel_list:
                if pos == index:
                    if (index_1_based - 1) in overlap_dict and (index_1_based) in overlap_dict:
                        prev_color = overlap_dict[index_1_based - 1]
                        if 'x' in prev_color or 'x' in color:
                            dynamic_html_string += generate_indel_string(indel_str)
                            continue                
                        if color == "purple":
                            dynamic_html_string += '<span style="background:Plum;">'
                            dynamic_html_string += generate_indel_string(indel_str)
                            dynamic_html_string += "</span>"
                        elif color == "red":
                            dynamic_html_string += '<span style="background:PaleVioletRed;">'
                            dynamic_html_string += generate_indel_string(indel_str)
                            dynamic_html_string += "</span>"
                        elif color == "blue":
                            dynamic_html_string += '<span style="background:Aqua;">'
                            dynamic_html_string += generate_indel_string(indel_str)
                            dynamic_html_string += "</span>"       
                    else:
                        dynamic_html_string += generate_indel_string(indel_str)                    
                    break                    

            if color == "purple":
                dynamic_html_string += '<span style="background:Plum;">'
                dynamic_html_string += char.upper()
                dynamic_html_string += "</span>"
            elif color == "red" or color == "redx":
                dynamic_html_string += '<span style="background:PaleVioletRed;">'
                dynamic_html_string += char.upper()
                dynamic_html_string += "</span>"
            elif color == "blue" or color ==  "bluex":
                dynamic_html_string += '<span style="background:Aqua;">'
                dynamic_html_string += char.upper()
                dynamic_html_string += "</span>"
            else:
                dynamic_html_string += char.upper()
            
            if index_1_based == len(sequence) and indel_list[-1][0] == len(sequence):
                dynamic_html_string += generate_indel_string(indel_list[-1][1])

        dynamic_html_string += "\n</p>"

    html_string += dynamic_html_string
    html_string += '\n</body>'
    return html_string

def generate_indel_string(indel_string):
    return_string = ""
    for char in indel_string:
        return_string += '-'
    return return_string

def combine_indels(indel_dict):
    new_indel_dict = {}
    keys = list(indel_dict.keys())
    for key in keys:
        new_indel_dict[key] = []
        indel_list = indel_dict[key]
        if len(indel_list) == 0:
            continue
        start_location = indel_list[0]
        indel_width = 1
        for index, location in enumerate(indel_list):
            if index + 1 >= len(indel_list):
                break
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
    indels_in_key = new_indel_dict[key]
    total_length_of_indels = 0
    for indel in indels_in_key:
        indel_string = indel[1]
        str_len = len(indel_string)
        total_length_of_indels += str_len
    
    return start_location - total_length_of_indels

def create_add_indel(new_indel_dict, key, start_location, indel_width):
    indel_string = ""
    for x in range(indel_width):
        indel_string += "-"
    new_indel_dict[key].append((start_location, indel_string))

def generate_indel_locals(seqs_with_indels):
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
    output = open(outputdir, 'w')
    output.write(html_string)
    output.close

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

def read_fimo_file(file_path):
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