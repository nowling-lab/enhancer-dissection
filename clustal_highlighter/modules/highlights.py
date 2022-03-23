from encodings import normalize_encoding
from clustal_highlighter.modules.character import Character
from clustal_highlighter.modules.file_handler import *
from collections import deque


class Highlights:
    def __init__(self, fasta_path: str):
        sequence_dict = read_fasta_file(fasta_path)
        self.sequences = self._generate_sequence_dictionary(sequence_dict)
        self.outputs = [] #array of strings containing full html file outs. Because why not?
        self._sequences_grouped = {}
        self.indel_dict = None
        self.variant_data = None
        self.group_all = True
        
    def _generate_sequence_dictionary(self, sequences: dict) -> dict:
        temp_sequences = {}
        
        for sequence in sequences:
            temp_sequences[sequence] = self._sequnece_as_Characters(sequences[sequence])
        return temp_sequences
    
    def _sequnece_as_Characters(self, sequence: str) -> list:
            char_obj_list = deque()
            for char in sequence:
                char_obj_list.append(Character(char))
            return char_obj_list

    def add_highlights(self, motifs_descriptor:str, file_path:str, color:str):
        # motifs descriptor is not yet used. It's there for when the HTML file will allow a variable size
        # of inputs. For now it will stay streme and jaspar but this is to let it scale indefinitly and remind me
        # to actually make that happen
            
        motifs = read_fimo_file(file_path)
        self._color_characters(motifs, color, motifs_descriptor)
        
    def _color_characters(self, motifs:dict, color:str, motifs_descriptor:str):
        for sequence in motifs:
            if sequence not in self.sequences:
                print("Mismatch between supplied FIMO file and sequences original sequence file, aborting coloring")
                return
            #Check all keys are valid before applying colors

        for sequence in motifs:
            highlights = motifs[sequence]

            for start, end, motif_id in highlights:
                for x in range(start - 1, end): #From 1 base to 0 base
                    self.sequences[sequence][x].add_motif(motifs_descriptor, motif_id, color.lower())
    
    def _group_sequences(self):
        for key in self.sequences.keys(): #Loop through all of the sequences
            self._find_similar_sequences(key)
    
    def _group_all_sequences(self):
        self._sequences_grouped['all'] = set()
        for key in self.sequences.keys():
            self._sequences_grouped['all'].add(key)
       
    def _find_similar_sequences(self, key:str): 
        key_split = key.split('-')
        first_part_key = key_split[0]

        if len(self._sequences_grouped) > 0:
            last_key = list(self._sequences_grouped.keys())[-1]
            last_list = list(self._sequences_grouped[last_key])
            if key in last_list:
                return #If this key was already done
            #we don't want to do it again so we skip. This is a clustal
            #omega format thing since we include multiple sequences 
            #per block

        self._group_similar_sequences(first_part_key, key) 
                     
    def _group_similar_sequences(self, first_part_key:str, key:str):
        self._sequences_grouped[first_part_key] = set()
        similar_sequences = self._sequences_grouped[first_part_key]
        for seq_name in self.sequences.keys():
            is_int = True
            try:
                int(first_part_key)
            except:
                is_int = False
            
            if first_part_key in seq_name and not is_int:
                similar_sequences.add(seq_name)
                #finds all the like-keys. So all the KLF ones ect
                
        if len(similar_sequences) == 0:
            similar_sequences.add(key)
        return              
                  
    def add_indels(self, path_to_indel_file:str):
        indel_fasta = read_fasta_file(path_to_indel_file)
        if not self._verify_matching_keys(indel_fasta):
            raise Exception("Key mismatch, aborting")
        indel_dict = self._parse_indels(indel_fasta)
        self.indel_dict = indel_dict
        
    def _append_indels_to_internal_list(self):
        self._add_indels_to_sequences(self.indel_dict)
        self._color_indels()

    def _color_indels(self):
        for sequence in self.sequences:
            sequence_character_list = self.sequences[sequence]
            for index, character in enumerate(sequence_character_list):                
                if character.character == '-':
                    if index > 0 and index < (len(sequence_character_list) - 1):
                        left_char, right_char = self._find_nearest_non_indels(index, sequence_character_list)
                        character.set_indel_color(left_char, right_char)
    
    def _find_nearest_non_indels(self, index, sequence:list):
        output_tuple = [None,None]
        left_copy = index
        right_copy = index
        
        found_left = False
        while(left_copy > 0 and not found_left):
            left_copy -= 1
            character_at_index = sequence[left_copy]
            if character_at_index.character != '-':
                output_tuple[0] = character_at_index
                found_left = True

        found_right = False
        while(right_copy < (len(sequence) - 1) and not found_right):
            right_copy += 1
            character_at_index = sequence[right_copy]
            if character_at_index.character != '-':
                output_tuple[1] = character_at_index
                found_right = True
                
        return output_tuple
            
    def _verify_matching_keys(self, fasta_dictionary:dict) -> bool:
        for sequence in fasta_dictionary:
            if sequence not in self.sequences:
                return False
        return True
    
    def _parse_indels(self, indel_fasta:dict) -> dict:
        indel_dict = {}
        for sequence in indel_fasta:        
            indel_dict[sequence] = []
            for index, character in enumerate(indel_fasta[sequence]):
                if character == '-':
                    indel_dict[sequence].append((index, character))
        return indel_dict
                    
    def _add_indels_to_sequences(self, indel_dict:dict) -> dict:
        for sequence in indel_dict:
            current_sequence = self.sequences[sequence]
            for location, dash in indel_dict[sequence]:
                if location < len(current_sequence):
                    current_sequence.insert(location, Character(dash))
                else:
                    current_sequence.append(Character(dash))    
                
    
    def generate_html_file(self):
        if self.indel_dict != None:
            self._append_indels_to_internal_list()
            
        html_string = html_header()
         # Large HTML header up top, then adds to it below with dynamic_html_string
        dynamic_html_string = "<br>"
        motif_keys = list(self.sequences.keys())
        motif_keys.sort()
        
        if self.group_all:
            self._group_all_sequences()
        else:
            self._group_sequences()
        
        for key_to_list in self._sequences_grouped:
            dynamic_html_string += "<br> <span> New Sequence </span>"
            key_list = list(self._sequences_grouped[key_to_list])
            #This is the start of a new sequence in the output
            list_of_lines = []

            line_length = 70
            self._normalize_line_length(key_list, list_of_lines, line_length)
            
            if(len(list_of_lines) == 0):
                stop = 1
            else:
                stop = len(list_of_lines[0][1])
            counter = 0
            position = 1
            while counter < stop: #Loop through however many lines we got
                max_len = self._find_max_key_length(list_of_lines)

                dynamic_html_string += '<pre>'
                rows_to_compare = []
                
                if self.variant_data != None:
                    dynamic_html_string += self._append_variant_data(max_len, position)
                
                for key, row in list_of_lines:
                    rows_to_compare.append(row[counter])
                    dynamic_html_string += self._compare_append_rows(row, counter, max_len, key)

                dynamic_html_string += self._append_stars(max_len, rows_to_compare)
                
                position_string, position = self._append_position(max_len, rows_to_compare, position)
                dynamic_html_string += position_string
                
                dynamic_html_string += '</pre>' #this is the last block since it's excluded
                counter += 1 #From the list. 

        html_string += dynamic_html_string
        html_string += '\n</body>'
        
        self.outputs.append(html_string)
        return self.outputs[-1]
    
    
    def _append_stars(self, max_len, rows_to_compare):
        padding = self._generate_padding_string(max_len, 'Stars')
        
        star_str = 'stars' + padding + ': '
        check_list = set()
        for row in rows_to_compare:
            check_list.add(len(row))
        if len(rows_to_compare) > 0:
            star_str += self._generate_continuity_stars(rows_to_compare)
        star_str += '<br>' 
    
        return star_str

    def _generate_continuity_stars(self, row_list):
        #Generates the stars for a list of 70 length strings
        star_string = ""
        for index, char in enumerate(row_list[-1]):
            chars_at_index = set()
            #Add all the characters at a single index to a set
            for row in row_list:
                chars_at_index.add(row[index].character)
                #If we have multiple chars at an index then we want empty
            if len(chars_at_index) > 1:
                star_string += ' '
            else: #else put a star there
                star_string += "*"

        return star_string

    def _generate_padding_string(self, max_len:int, key:str):
        ##Pads out the keys so it lines everything up properly
        padding_str = " "
        if max_len > len(key):
            padding = max_len - len(key) 
            for x in range(padding):
                padding_str += " "
        return padding_str 
    
    def _append_position(self, max_len:int, rows_to_compare:list, position:int):
        padding = self._generate_padding_string(max_len, 'Pos')
        
        pos_string = 'Pos' + padding + ': Start: ' + str(position) + ","
        
        #Just an easy way to keep the loop more simple since it's +1 in the loop
        position += len(rows_to_compare[0]) - 1

        pos_string += " End: " + str(position)
        position += 1
        
        return pos_string, position
    
    def _convert_line_to_html(self, line:list):
        html_out = ""
        for character in line:
            html_out += character.to_string()
        return html_out
    
    def _compare_append_rows(self, row:list, counter:int, max_len:int, key:str):
        row_string = ""
        padding_str = self._generate_padding_string(max_len, key)
        #For every key that like, as in for all KLF's,
        #Grab the row and print them 
        #also adds to the rows_to_compare for when I do star comparisons 
        row_string +=  key + padding_str + ": " 
        row_string += self._convert_line_to_html(row[counter])
        row_string += '<br>'
        return row_string
    
    def _normalize_line_length(self, key_list:list, list_of_lines:list, line_length:int):
        for key in key_list:
            line_list = [] #loops through all the keys
            combined_list = self.sequences[key]
            line = []
            for index, character in enumerate(combined_list):                
                if index % line_length == 0 and index != 0:
                    line_list.append(line.copy())
                    line.clear()

                line.append(character)
                
            line_list.append(line.copy())
            line.clear()
            list_of_lines.append((key, line_list.copy()))
            line_list.clear()
            #This essentially just splits the whole massive sequence into
            #Multiple 70-length sequences for clustal format
            
    def _find_max_key_length(self, list_of_lines:list):
        keys_lengths = []
        for key, row in list_of_lines:
            keys_lengths.append(len(key)) 
        
        keys_lengths.append(len('stars'))
        
        max_len = max(keys_lengths) 
        return max_len
        #this last loop is to find the longest key so we can add
        #white space to other keys to make it line up properly
        
    def add_variant_data(self, file_path: str) -> None:
        variant_data = read_variant_stats(file_path)
        self.variant_data = variant_data
    
    def _append_variant_data(self, max_len, position):
        padding = self._generate_padding_string(max_len, 'Variant')
        
        variant_string = 'Variant' + padding + ": "
        for x in range(position, position + 70): #70 is line width...
            if x in self.variant_data:
                char1, char2, chance1, chance2 = self.variant_data[x]
                chance1 = float(round((chance1 * 100), 3))
                chance2 = float(round((chance2 * 100), 3))
                normalized_chance = None
                if chance1 >= 50.0:
                    normalized_chance = (chance1 - 50)/(100 - 50)
                else:
                    normalized_chance = (chance2 - 50)/(100 - 50)
                    
                red = 255 * (1 - normalized_chance)
                green = 255 * normalized_chance
                blue = 0
                    
                variant_string += f'<span style="color:rgb({red},{green},{blue})" data-toggle="tooltip" data-animation="false" title ="Appearances: {char1}: {chance1}% {char2}: {chance2}%">^</span>'
            else:
                variant_string += ' '
        
        variant_string += "<br>"
        
        return variant_string
    
    #as_html += ' data-toggle="tooltip" data-animation="false" title = "' + self.tooltip + '"' 
