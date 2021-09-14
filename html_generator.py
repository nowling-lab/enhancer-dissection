from os import read

def main():
    motif_dict = read_fimo_file('./temp_files_pre_params/enhancer-dissection-out/FIMO_16_enhancers/fimo.tsv')
    seq_dict = read_fasta_file('./temp_files_pre_params/16_enhancers.fa')
    html_string = generate_html(motif_dict, seq_dict)
    html_string_to_output(html_string, './test.html')

def html_string_to_output(html_string, outputdir):
    output = open(outputdir, 'w')
    output.write(html_string)
    output.close

def generate_html(motif_dict, seq_dict):
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
     """
    before_tag = '<span style="background-color:DodgerBlue">'
    after_tag = '</span>'
    tag_length = len(before_tag) + len(after_tag)
    dynamic_html_string = None
    motif_keys = list(motif_dict.keys())
    motif_keys.sort()
    for key in motif_keys:
        if dynamic_html_string == None:
            dynamic_html_string = "<p>\n"
        else:
            dynamic_html_string += "<p>\n"
        dynamic_html_string += ">" + str(key) + "\n"

        sequence = seq_dict[key]
        highlight_list = motif_dict[key]
        highlight_list = sorted(highlight_list, key=lambda x: x[0])
        highlight_list2 = clean_overlapping_motifs(highlight_list)
        #print(highlight_list, "\n\n")
        #print(highlight_list2, "\n\n")
        previous_length = None
        for index, highlight in enumerate(highlight_list):
            start, end = highlight
            end = end - 1
            if index > 0:
                motif_width = end - start + 1
                dist_to_next_motif = start - highlight_list[index -1][1]
                next_motif_start = previous_length + dist_to_next_motif
                next_motif_end = motif_width + next_motif_start

                seq_start = sequence[:next_motif_start]
                seq_motif = sequence[next_motif_start - 1: next_motif_end]
                seq_end = sequence[next_motif_end :]
                sequence = seq_start + before_tag + seq_motif + after_tag + seq_end
                previous_length = len(seq_start) + len(seq_motif) + tag_length
            else:
                seq_start = sequence[:start]
                seq_motif = sequence[start - 1: end]
                seq_end = sequence[end:]
                sequence = seq_start + before_tag + seq_motif + after_tag + seq_end
                previous_length = len(seq_start) + len(seq_motif) + tag_length
        dynamic_html_string += sequence
        dynamic_html_string += "\n</p>"

    html_string += dynamic_html_string
    html_string += '\n</body>'
    return html_string

def clean_overlapping_motifs(highlight_list):
    new_list = []
    for index, high_light in enumerate(highlight_list):
        end = None
        for x in range(index + 1, len(highlight_list)):
            if high_light[1] >= highlight_list[x][0]:
                end = highlight_list[x][1]
            else:
                break
        if end is not None:
            new_list.append((high_light[0], end))
        else:
            print(new_list[-1][1])
            if new_list[-1][1] != high_light[1]:
                new_list.append(high_light)
    return sorted(new_list, key=lambda x: x[0])

def read_fasta_file(file_path):
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
                    sequence_dictionary[int(sequence_name)] = sequence
                    sequence_name = split_header[0]
                    sequence_name = sequence_name[1:]
                    sequence = None
            else:
                if sequence == None:
                    sequence = line.strip()
                else:
                    sequence += line.strip() 
    sequence_dictionary[int(sequence_name)] = sequence
    return sequence_dictionary

def read_fimo_file(file_path):
    sequence_name_dict = {}
    with open(file_path) as f:
            header = f.readline() #to get rid of it
            for line in f:
                if len(line) <= 1:
                    return sequence_name_dict
                line_split = line.split()
                seq_name = int(line_split[2])
                start = int(line_split[3])
                stop = int(line_split[4])

                if seq_name not in sequence_name_dict:
                    sequence_name_dict[seq_name] = []
                else:
                    sequence_name_dict[seq_name].append((start, stop))  
    return sequence_name_dict
               
main()