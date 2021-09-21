def main():
    fasta = read_fasta_file('temp_files_pre_params/fasta_files/nardini_luciferase_fragments.fasta', True)
    seq_with_indels = read_fasta_file('temp_files_pre_params/fasta_files/nardini_A_only_with_indels.fa', False)

    #motif_dict = read_fimo_file('./temp_files_pre_params/fimo_pest/pest_streme_motifs/fimo.tsv')
    #motif_dict2 = read_fimo_file('./temp_files_pre_params/fimo_pest/pest_jaspar_motifs/fimo.tsv')
    #seq_dict = read_fasta_file('./temp_files_pre_params/fasta_files/nardini_reference_sequences.fa', False)
    #html_string = generate_html(motif_dict, motif_dict2, seq_dict)

    indel_locations = generate_indel_locals(seq_with_indels)
    new_indel_list = combine_indels(indel_locations)
    #print(indel_locations)

   # html_string_to_output(html_string, './test.html')

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
     """
    dynamic_html_string = None
    motif_keys = list(motif_dict1.keys())
    motif_keys.sort()
    for key in motif_keys:
        if dynamic_html_string == None:
            dynamic_html_string = """<p style="font-family:'Courier New'; word-wrap: break-word; width: 75%">"""
        else:
            dynamic_html_string += """<p style="font-family:'Courier New'; word-wrap: break-word; width: 75%">"""
        dynamic_html_string += ">" + str(key) + "<br>"

        indel_list = indel_dict[key] #??? get the keys to match I guess.. Think about it later.

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

            #if index_1_based in indel_dict: #look if indel is here
                

            if color == "purple":
                dynamic_html_string += '<span style="background:Plum;">'
                dynamic_html_string += char.upper()
                dynamic_html_string += "</span>"
            elif color == "red":
                dynamic_html_string += '<span style="background:PaleVioletRed;">'
                dynamic_html_string += char.upper()
                dynamic_html_string += "</span>"
            elif color == "blue":
                dynamic_html_string += '<span style="background:Aqua;">'
                dynamic_html_string += char.upper()
                dynamic_html_string += "</span>"
            else:
                dynamic_html_string += char.upper()

        dynamic_html_string += "\n</p>"

    html_string += dynamic_html_string
    html_string += '\n</body>'
    return html_string

def combine_indels(indel_dict):
    new_indel_dict = {}
    keys = list(indel_dict.keys())
    indel_width = 1
    for key in keys:
        new_indel_dict[key] = []
        indel_list = indel_dict[key]
        for index, location in enumerate(key):
            if indel_width > 1:
                indel_width -= 1
                continue

            jump = False
            temp_index = index + 1

            while not jump:
                if int(indel_list[temp_index]) - int(indel_list[temp_index-1]) == 1:
                    temp_index += 1
                    indel_width += 1
                else:
                    jump = True
            indel_string = ""
            for x in range(indel_width):
                indel_string += "-"
            new_indel_dict[key].append((indel_list[index], indel_string))
        
    new_keys = list(new_indel_dict.keys())
    print(new_indel_dict)

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
                start = line_split[3]
                stop = line_split[4]

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
                    if color != ch_color:
                        overlap_dict[x] = "purple"
                else:
                    overlap_dict[x] = color

main()