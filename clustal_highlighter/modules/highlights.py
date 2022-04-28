from ctypes import pointer
from clustal_highlighter.modules.character import Character
from clustal_highlighter.modules.file_handler import *
from clustal_highlighter.modules.html_framework import *
from collections import deque


class Highlights:
    def __init__(self, seq_dict: dict, offset=0, seq_end=None):
        self.offset = offset
        self.seq_start = offset
        self.seq_end = seq_end
        sequence_dict = seq_dict
        self.has_indels = False
        self.sequences = self._generate_sequence_dictionary(sequence_dict)
        self.outputs = []  # array of strings containing full html file outs. Because why not?
        self._sequences_grouped = {}
        self.indel_dict = None
        self.variant_data = None
        self.group_all = True
        self.highlight_styles = {}
        

    def _generate_sequence_dictionary(self, sequences: dict) -> dict:
        """Given a dictionary of sequences this transforms them into Character objects in the same format 

        Args:
            sequences (dict): A dictionary of sequence_names: sequence 

        Returns:
            dict: The sequence dictionary but made of characters instead
        """
        temp_sequences = {}

        for sequence in sequences:
            temp_sequences[sequence] = self._sequence_as_Characters(
                sequences[sequence])
        return temp_sequences

    def _sequence_as_Characters(self, sequence: str) -> list:
        """Takes a string sequnece and transforms it into a list of Characters instead. Uses a deque instead of a normal list for O(1) appending

        Args:
            sequence (str): A sequnece represented by a single string

        Returns:
            list: A identical list to the string but made up of Characters
        """
        char_obj_list = deque()
        for char in sequence:
            char_obj_list.append(Character(char))
            if char == "-" and not self.has_indels:
                self.has_indels = True
        return char_obj_list

    def add_highlights(self, motifs_descriptor: str, file_path: str, color: str, html_color: str):
        """Adds motifs to character objects at given locations from a given file path. 

        Args:
            motifs_descriptor (str): A description of the motifs given. "streme" is a description of motifs for motifs found by running Streme by meme suite
            file_path (str): A file path to the results of running Fimo with a given motif file
            color (str): The color description of what the highlights should be
            html_color (str): The actual HTML color (rbg, name or otherwise) which will be used to color the positions given in the femo results tsv
        """
        # motifs descriptor is not yet used. It's there for when the HTML file will allow a variable size
        # of inputs. For now it will stay streme and jaspar but this is to let it scale indefinitly and remind me
        # to actually make that happen

        motifs = read_fimo_file(file_path)
        if motifs:
            self._add_html_style(color.lower(), html_color, motifs_descriptor)
            self._color_characters(motifs, color, motifs_descriptor)

    def _add_html_style(self, color: str, html_color: str, motifs_descriptor: str):
        """This adds a class based on the color description and actual html color passed in from add_highlights. 

        Args:
            color (str): The description of the color, used to name the class
            html_color (str): The actual html color that is to be used to color the characters
            motifs_descriptor (str): A description of what the motif color is to be used for
        """
        class_name = "." + color + "{\n"
        background = f" background:{html_color};"
        class_string = (class_name + background + '\n}\n')

        self.highlight_styles[color] = (
            class_string, motifs_descriptor, html_color)

    def _color_characters(self, motifs: dict, color: str, motifs_descriptor: str):
        """Goes through the provided idecies and adds the motif and its color to the characters there

        Args:
            motifs (dict): A dictionary of motifs, given as sequence_name: [motif1, motif2, ..., motifn]
            color (str): The color to be used to give to those characters at those positions
            motifs_descriptor (str): The descriptor used to describe the motifs being colored
        """
        for sequence in motifs:
            if sequence not in self.sequences:
                print(
                    "Mismatch between supplied FIMO file and sequences in original sequence file, aborting coloring")
                return
            # Check all keys are valid before applying colors

        for sequence in motifs:
            highlights = motifs[sequence]

            for start, end, motif_id in highlights:
                for x in range(start - 1, end):  # From 1 base to 0 base
                    self.sequences[sequence][x].add_motif(
                        motifs_descriptor, motif_id, color.lower())

    def _group_sequences(self):
        """Groups sequences by the first part of their name, delimited by -
        """
        for key in self.sequences.keys():  # Loop through all of the sequences
            self._find_similar_sequences(key)

    def _group_all_sequences(self):
        """Groups all sequnces together so the clustal output is all of them compared to each other 
        """
        self._sequences_grouped['all'] = set()
        for key in self.sequences.keys():
            self._sequences_grouped['all'].add(key)

    def _find_similar_sequences(self, key: str):
        """Finds sequences that are similar to the given keys

        Args:
            key (str): A key describing a sequence

        Returns:
            None: Breaks early if we've already used this key to form a group
        """
        key_split = key.split('-')
        first_part_key = key_split[0]

        if len(self._sequences_grouped) > 0:
            last_key = list(self._sequences_grouped.keys())[-1]
            last_list = list(self._sequences_grouped[last_key])
            if key in last_list:
                return  # If this key was already done
            # we don't want to do it again so we skip. This is a clustal
            # omega format thing since we include multiple sequences
            # per block

        self._group_similar_sequences(first_part_key, key)

    def _group_similar_sequences(self, first_part_key: str, key: str):
        """Groups sequences by a provided first part key. The whole key is passed just in case this key is not similar to any others

        Args:
            first_part_key (str): The first part of a key Iam-aKey has the first part key of Iam 
            key (str): The entire key of the above example would be Iam-aKey
        """
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
                # finds all the like-keys. So all the KLF ones ect

        if len(similar_sequences) == 0:
            similar_sequences.add(key)
        return

    def add_indels(self, path_to_indel_file: str):
        """Adds indels to the list of characters, inserting new Character objects where required

        Args:
            path_to_indel_file (str): The path to the indel file, this is simply an aligned file in fasta format with -'s where indels have been found in the genomes

        Raises:
            Exception: If the keys in the sequences in this file mismatch the current sequences an exception is raised 
        """
        indel_fasta = read_fasta_file(path_to_indel_file)
        if not self._verify_matching_keys(indel_fasta):
            raise Exception("Key mismatch, aborting")
        indel_dict = self._parse_indels(indel_fasta)
        self.indel_dict = indel_dict

    def _append_indels_to_internal_list(self):
        """Calls the required functions to add indels to the internal sequnece list
        """
        self._add_indels_to_sequences(self.indel_dict)
        self._color_indels()

    def _color_indels(self):
        """Adds indels to the internal list, passing the nearest left and right characters to the Character (new indel) to see if it should be colored or not
        """
        for sequence in self.sequences:
            sequence_character_list = self.sequences[sequence]
            for index, character in enumerate(sequence_character_list):
                if character.character == '-':
                    if index > 0 and index < (len(sequence_character_list) - 1):
                        left_char, right_char = self._find_nearest_non_indels(
                            index, sequence_character_list)
                        character.set_indel_color(left_char, right_char)

    def _find_nearest_non_indels(self, index, sequence: list):
        """Finds the nearest non-indel left and right of a current index

        Args:
            index (int): The index of the indel being added
            sequence (list): The sequence of Characters that this indel is being inserted into

        Returns:
            Tuple (left, right): Tuple of Characters (1 left and right) of nearerst non-indels, or None in those spots if the end of the list happens before a non-indel 
        """
        output_tuple = [None, None]
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

    def _verify_matching_keys(self, fasta_dictionary: dict) -> bool:
        """Verifies that a passed dcitionary matches the current internal one for keys

        Args:
            fasta_dictionary (dict): A squence dictionary of names to sequences

        Returns:
            bool: If this sequence is valid or not
        """
        for sequence in fasta_dictionary:
            if sequence not in self.sequences:
                return False
        return True

    def _parse_indels(self, indel_fasta: dict) -> dict:
        """Finds indels is passed indel fasta dictionry of names: sequences with indels imbedded

        Args:
            indel_fasta (dict): A fasta file with sequnces that have indels

        Returns:
            dict: An indel dictionary which has tuples of locations and -'s where indels are found. Keys are sequence names
        """
        indel_dict = {}
        for sequence in indel_fasta:
            indel_dict[sequence] = []
            for index, character in enumerate(indel_fasta[sequence]):
                if character == '-':
                    indel_dict[sequence].append((index, character))
        return indel_dict

    def _add_indels_to_sequences(self, indel_dict: dict):
        """Inserts indels into the sequence at given locations

        Args:
            indel_dict (dict): The dictionary returned from _parse_indels

        """
        for sequence in indel_dict:
            current_sequence = self.sequences[sequence]
            for location, dash in indel_dict[sequence]:
                if location < len(current_sequence):
                    current_sequence.insert(location, Character(dash))
                else:
                    current_sequence.append(Character(dash))

    def _add_html_classes(self):
        """Adds html classes to the html file

        Returns:
            String: The string that contains all the html classes for the file
        """
        keys = list(self.highlight_styles.keys())
        keys.sort()

        html_class_string = ""
        for key in keys:
            class_string, motifs_descriptor, html_color = self.highlight_styles[key]
            html_class_string += class_string
        html_class_string += "</style>\n"
        return html_class_string

    def _add_html_legend(self):
        """Adds the legend describing what highlights and other additions are within the file
        """
        keys = list(self.highlight_styles.keys())
        keys.sort()

        legend_string = ""
        if self.variant_data != None or self.indel_dict != None or len(keys) > 0:
            legend_string = """
            </head>
            <body>
            <div> Legend: </div>
            
            """

        for key in keys:
            class_string, motifs_descriptor, html_color = self.highlight_styles[key]
            legend_string += f'<div class = "{key} heading"> This color is for the {motifs_descriptor} descriptor given </div>\n'

        if len(keys) > 1:
            legend_string += f'<div class = "purple heading"> This is for overlapping highlights </div>\n'

        if self.indel_dict != None:
            legend_string += """<div class = "clear" style="width:75%; word-wrap: break-word;"> Colored &#8209;'s indicate that the indel is between 2 characters that have an identical set of motifs. If they are not colored, then that means the character to the left has a different set of motifs than the one to the right of the indel. </div>"""

        if self.variant_data != None:
            legend_string += """<div class = "clear" style="width:75%; word-wrap: break-word;"> ^'s indicate that Variant data is available for that position. Mouse over to view stats </div>"""

        return legend_string

    def _add_html_buttons(self):
        """Adds buttons to toggle different features if they are toggleable
        """
        button_string = "<span>"
        keys = list(self.highlight_styles.keys())
        keys.sort()

        for key in keys:
            class_string, motifs_descriptor, html_color = self.highlight_styles[key]
            button_string += f"""\n<button id="toggle_{key}" type="button" class="btn" style="background:{html_color}">Toggle {key}</button>"""

        if self.variant_data != None:
            button_string += """\n<button id="toggle_variant" type="button" class="btn btn-secondary">Toggle Variant ^'s</button>"""

        if len(keys) > 1:
            button_string += """\n<button id="toggle_purple" type="button" class="btn" style="background:Plum">Toggle Purple</button>"""

        button_string += "\n</span>"

        button_string += '\n<script type="text/javascript">\n'
        button_string += "$(document).ready(function () {\n"

        button_string += """$('[data-toggle="tooltip"]').tooltip();\n"""

        for key in keys:
            button_string += f"""$("#toggle_{key}").click(function() """ + "{\n"
            button_string += f"""   $( "span.{key}" ).toggleClass( "clear" );\n"""
            button_string += "});\n\n"

        if len(keys) > 1:
            button_string += f"""$("#toggle_purple").click(function() """ + \
                "{\n"
            button_string += f"""   $( "span.purple" ).toggleClass( "clear" );\n"""
            button_string += "});\n\n"

        if self.variant_data != None:
            button_string += """$('#toggle_variant').click(function(){
                $( "span.variant" ).toggleClass( "hidden" );
            });
            """
        button_string += "}); \n</script>"
        return button_string

    def _generate_html(self):
        """Generates the html header which contains classes, the legend and the buttons

        Returns:
            String: The html string which defines the above features
        """
        html_string = html_heading()
        html_string += self._add_html_classes()
        html_string += self._add_html_legend()
        html_string += self._add_html_buttons()
        return html_string

    def generate_html_file(self):
        """Generates the entire html file and returns that string as output

        Returns:
            String: A string that is the HTML file that can later be printed and viewed
        """
        if self.indel_dict != None:
            self._append_indels_to_internal_list()
        elif self.has_indels:
            self._color_indels()

        html_string = self._generate_html()
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
            # This is the start of a new sequence in the output
            list_of_lines = []

            line_length = 70
            self._normalize_line_length(key_list, list_of_lines, line_length)

            if(len(list_of_lines) == 0):
                stop = 1
            else:
                stop = len(list_of_lines[0][1])

            counter = 0
            position = 1 + self.offset
            while counter < stop:  # Loop through however many lines we got
                max_len = self._find_max_key_length(list_of_lines)

                dynamic_html_string += '<pre>'
                rows_to_compare = []

                if self.variant_data != None:
                    dynamic_html_string += self._append_variant_data(
                        max_len, counter+1)

                row_end_position = None
                for key, row in list_of_lines:
                    rows_to_compare.append(row[counter])
                    row_end_position = self._calculate_position(
                        len(row[counter]), position)
                    dynamic_html_string += self._compare_append_rows(
                        row, counter, max_len, key, row_end_position)

                if row_end_position != None:
                    position = row_end_position + 1

                dynamic_html_string += self._append_stars(
                    max_len, rows_to_compare)

                dynamic_html_string += '</pre>'  # this is the last block since it's excluded
                counter += 1  # From the list.

        html_string += dynamic_html_string
        html_string += '\n</body>'

        self.outputs.append(html_string)
        return self.outputs[-1]

    def _append_stars(self, max_len, rows_to_compare):
        """Adds the continunity stars to the html file

        Args:
            max_len (Int): The maximum length of the longest key in the keys and descriptors
            rows_to_compare (List): 70 length rows of Characters that define each clustal block

        Returns:
            String: The string of stars which show the continunity of some columns
        """
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
        """Compares up the row to see if the specific column is continuous or not 

        Args:
            row_list (List): A list of 70 Character rows that is being compared

        Returns:
            String: *'s that define if a column is a continuous or not. 
        """
        # Generates the stars for a list of 70 length strings
        star_string = ""
        for index, char in enumerate(row_list[-1]):
            chars_at_index = set()
            # Add all the characters at a single index to a set
            for row in row_list:
                try:
                    chars_at_index.add(row[index].character)
                except:
                    pass
                # If we have multiple chars at an index then we want empty
            if len(chars_at_index) > 1:
                star_string += ' '
            else:  # else put a star there
                star_string += "*"

        return star_string

    def _generate_padding_string(self, max_len: int, key: str):
        """Generates padding to make the descriptions on the left side of the HTML output the same indentation

        Args:
            max_len (int): The biggest length item in the keys
            key (str): The key that is current needing padding

        Returns:
            String: Spaces which space out the keys so everything is even
        """
        # Pads out the keys so it lines everything up properly
        padding_str = " "
        if max_len > len(key):
            padding = max_len - len(key)
            for x in range(padding):
                padding_str += " "
        return padding_str

    def _calculate_position(self, row_size, row_start: int):
        """Keeps track of the end of the row in order to track position to place the clustal positions at the end of the sequences
        """
        # Just an easy way to keep the loop more simple since it's +1 in the loop
        row_end_position = row_start + row_size

        return row_end_position - 1

    def _convert_line_to_html(self, line: list):
        """Converts a given list of Characters to a string of html

        Args:
            line (list): A list of Characters

        Returns:
            String: The html representation of that list of Characters
        """
        html_out = ""
        for character in line:
            html_out += character.to_string()
        return html_out

    def _compare_append_rows(self, row: list, counter: int, max_len: int, key: str, row_end_position: int):
        """Converts a row to an html row with a name on the left and position at the right.
           Creates a singsequence_name     : sequence 70 Character lengthed html string with position at the end

        Args:
            row (list): A list of Character rows
            counter (int): A counter of which block this belongs to
            max_len (int): The maximum length name so that spacing is even
            key (str): The key of the current sequence
            row_end_position (int): The end of the rows length to put for clustal formatting

        Returns:
            _type_: _description_
        """
        row_string = ""
        padding_str = self._generate_padding_string(max_len, key)
        # For every key that like, as in for all KLF's,
        # Grab the row and print them
        # also adds to the rows_to_compare for when I do star comparisons
        row_string += key + padding_str + ": "
        row_string += self._convert_line_to_html(row[counter])
        row_string += " " + str(row_end_position)
        row_string += '<br>'
        return row_string

    def _normalize_line_length(self, key_list: list, list_of_lines: list, line_length: int):
        """Normalizes line length to be consistent. 70 is the current standard that is being used

        Args:
            key_list (list): The list of keys of the sequences in this group (all or grouped by that first part of the keys)
            list_of_lines (list): The list of lines that defines that group
            line_length (int): The length to normalize to
        """
        for key in key_list:
            line_list = []  # loops through all the keys
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
            # This essentially just splits the whole massive sequence into
            # Multiple 70-length sequences for clustal format

    def _find_max_key_length(self, list_of_lines: list):
        """Finds the maximum key length of all the keys

        Args:
            list_of_lines (list): The list of lines in the group which will be printed together

        Returns:
            int: the maximm length of the longest key
        """
        keys_lengths = []
        for key, row in list_of_lines:
            keys_lengths.append(len(key))

        keys_lengths.append(len('stars'))

        max_len = max(keys_lengths)
        return max_len
        # this last loop is to find the longest key so we can add
        # white space to other keys to make it line up properly

    def add_variant_data(self, df) -> None:
        """Adds variant data to the object

        Args:
            file_path (str): A file path to variant data. This returns a dict of positions and what variations could be there and their positions 
        """
        variant_data = generate_variant_dict(self.seq_start, self.seq_end, df)
        if len(variant_data) > 0:
            self.variant_data = variant_data

    def _append_variant_data(self, max_len, row):
        """Appends variant data to the html string

        Args:
            max_len (int): Maximum key length
            row (int): Which block this belongs to. Which row respective to each sequence is this (of the 70 lengthed rows)

        Returns:
            String: A string that contains ^'s for where variants are found with tool tips at those spots
        """
        padding = self._generate_padding_string(max_len, 'Variant')
        position = 1
        if row > 1:
            position = (row-1) * 70
            position += 1

        variant_string = 'Variant' + padding + ": " + '<span class="variant">'
        for x in range(position, position + 70):  # 70 is line width...
            x_offset = (x + self.offset)
            if x_offset in self.variant_data:
                char1, char2, chance1, chance2 = self.variant_data[x_offset]
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

        variant_string += "</span>" + "<br>"

        return variant_string

    def _to_string(self):
        """Generates HTML 70 blocked strings using the to_string of the Characters. This is used for testing

        Returns:
            String: The HTML output as described above
        """
        keys = list(self.sequences.keys())
        keys.sort()
        output_string = ''
        for key in keys:
            output_string += f'{key}\n'
            for index, character in enumerate(self.sequences[key]):
                output_string += character.to_string()
                if index == 69:  # Breaks after 70 char, 0 indexed
                    output_string += '\n'
            output_string += '\n'
        output_string = output_string[:-2]  # getting rid of last newline

        return output_string
