from clustal_highlighter.modules.character import Character
from clustal_highlighter.modules.file_handler import *


class Highlights:
    def __init__(self, fasta_path: str):
        sequence_dict = read_fasta_file(fasta_path)
        self.sequences = self._generate_sequence_dictionary(sequence_dict)
        self.outputs = [] #array of strings containing full html file outs. Because why not?
        self._sequences_grouped = {}

    def _generate_sequence_dictionary(self, sequences: dict) -> dict:
        temp_sequences = {}
        
        for sequence in sequences:
            temp_sequences[sequence] = self._sequnece_as_Characters(sequences[sequence])
        return temp_sequences
    
    def _sequnece_as_Characters(self, sequence: str) -> list:
            char_obj_list = []
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
                     
                     
    def generate_html_file(self):
        
        html_string = html_header()
         # Large HTML header up top, then adds to it below with dynamic_html_string
        dynamic_html_string = "<br>"
        motif_keys = list(self.sequences.keys())
        motif_keys.sort()
        
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
                for key, row in list_of_lines:
                    rows_to_compare.append(row[counter])
                    dynamic_html_string += self._compare_append_rows(row, counter, max_len, key)

                ##dynamic_html_string += append_stars(max_len, rows_to_compare)
                
                position_string, position = self._append_position(max_len, rows_to_compare, position)
                dynamic_html_string += position_string
                
                dynamic_html_string += '</pre>' #this is the last block since it's excluded
                counter += 1 #From the list. 

        html_string += dynamic_html_string
        html_string += '\n</body>'
        
        self.outputs.append(html_string)
        return self.outputs[-1]

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