from clustal_highlighter.modules.fasta_highlighter_LEGACY.modules.character import Character
from clustal_highlighter.modules.fasta_highlighter_LEGACY.modules.file_handler import *
from clustal_highlighter.modules.fasta_highlighter_LEGACY.modules.html_framework import *
from clustal_highlighter.modules.fasta_highlighter_LEGACY.modules.variant_handler import *
from clustal_highlighter.modules.fasta_highlighter_LEGACY.modules.data_classes import *
from collections import deque
import logging
import statistics

from clustal_highlighter.modules.logger import *
default_logger = True

class Highlights:
    global logger
    logger = logging.getLogger('generic_highlights')

    def __init__(self, seq_dict: dict, chromosome: str = None, offset=1, seq_end=None):
        self.offset = offset
        self.seq_start = offset
        self.seq_end = seq_end
        sequence_dict = seq_dict
        self.has_indels = False
        #from sequence fasta, compare with: self.num_nucleotides_inaccessible
        self.sequence_positions_N = 0    
    
        self.sequences = self._generate_sequence_dictionary(sequence_dict)
        if self.seq_end == None:
            keys = list(self.sequences.keys())
            max_len = max([len(self.sequences[key]) for key in keys]) #list compression getting all seq sizes and calling max
            self.seq_end = max_len
            if self.seq_start != 0:
                self.seq_end += self.seq_start + 1
        
        self.outputs = []  # array of strings containing full html file outs. Because why not?
        self._sequences_grouped = {}
        self.indel_dict = None
        self.variant_data = None
        
        #Set this flag if variants are added. This does NOT mean that there were 
        #variants found within this region. It just means that they were asked for when the software
        #was ran
        self.variants_given = False
        self.group_all = True
        self.highlight_styles = {}
        
        self.motif_names = []
        
        #variables for runtime checks
        self.highlights_name = None
        self.variant_matches = 0
        self.variant_mismatches = 0
        self.highlights_requested = {}
        self.wrong_chars = 0
        self.variants_found = 0   
        
        self.motif_counts = {}     
        
        self.csv_wanted = False
        file_path = ""
        #Table data
        self.name = chromosome
        #name, sequence_start, sequence_stop, motif, count
        self.motif_counts_csv = None
        #name, sequence_start, sequence_stop, motif_descriptor, coverage
        self.coverage = {}
        self.coverage_csv = None
        #name, sequence_start, sequence_stop, variant_pos, ref, alt, ref%, alt%
        self.varaints_csv = None
        self.variants_with_percent = []
        #chromosome, sequence_start, sequence_stop, num_variants, num_accessible_variants, num_accessible_nucleotides, accessibility_given, min_motif_percent_coverage, max_motif_percent_coverag, num_motif_matrices_given
        self.summary_csv = None
        self.motif_percent_coverage = {}
        self.motif_sets = None
        self.motif_coverage = None
        
        #accessibility variables
        self.has_accessibility = False
        self.num_variants_accessible = 0
        self.num_nucleotides_accessible = 0
        
        #from accessibility fasta
        self.num_nucleotides_inaccessible = 0
        
        #site pi
        self.site_pi_dict = None
        self.pi_scores_array = None
        
        #genotype numbers variables 
        self.genotype_dict = {}
    
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
        pos_counter = self.seq_start
        for char in sequence:
            char_obj_list.append(Character(char, pos_counter))
            pos_counter += 1
            if char == "-" and not self.has_indels:
                self.has_indels = True
            elif char =="N":
                self.sequence_positions_N += 1
        
        info(logger, f"{logger.name} has {self.sequence_positions_N} nucleotides that have not be sequenced (N)")
        return char_obj_list

    def add_highlights(self, motifs_descriptor: str, file_path: str, color: str, html_color: str):
        """Adds motifs to character objects at given locations from a given file path. 

        Args:
            motifs_descriptor (str): A description of the motifs given. "streme" is a description of motifs for motifs found by running Streme by meme suite
            file_path (str): A file path to the results of running Fimo with a given motif file
            color (str): The color description of what the highlights should be
            html_color (str): The actual HTML color (rbg, name or otherwise) which will be used to color the positions given in the femo results tsv
        """
        
        motifs = read_fimo_file(file_path)
        
        self.motif_names.append(motifs_descriptor)
        
        if(default_logger and len(motifs.keys()) == 1):
            global logger
            logger = logging.getLogger(list(motifs.keys())[0])
        
        for key in motifs:
            tmp_motif_highlights = motif_highlights(motifs_descriptor, len(motifs[key]), 0)
            self.highlights_requested[motifs_descriptor] = tmp_motif_highlights
        
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
                print(motifs.keys())
                print(self.sequences.keys())
                print("Mismatch between supplied FIMO file and sequences in original sequence file, aborting coloring")
                return
            # Check all keys are valid before applying colors

        motif_highlights = self.highlights_requested[motifs_descriptor]
    
        self.motif_counts[motifs_descriptor] = {}
        motif_counts_per_descriptor = self.motif_counts[motifs_descriptor]
    
        for sequence in motifs:
            highlights = motifs[sequence]
            
            for start, end, motif_id, matched_sequence in highlights:
                if motif_id in motif_counts_per_descriptor:
                    motif_counts_per_descriptor[motif_id] += 1
                else:
                    motif_counts_per_descriptor[motif_id] = 1
                    
                motif_highlights.motifs_applied += 1
                counter = 0
                for x in range(start - 1, end):  # From 1 base to 0 base
                    current_char = self.sequences[sequence][x]
                    current_char.add_motif(
                        motifs_descriptor, motif_id, color.lower())
                    
                    matched_char = matched_sequence[counter]
                    if current_char.character != matched_char:
                        warning(logger, f'In {sequence} a matched highlight overlapped the wrong character!')
                   
                    counter += 1
        if motif_highlights.is_equal():
            info(logger, motif_highlights.to_string())
        else:
            warning(logger, f'Mismatch between requested highlights and applied highlights. {motif_highlights.to_string()}')

    def _group_sequences(self):
        """Groups sequences by the first part of their name, delimited by -
        """
        for key in self.sequences.keys():  # Loop through all of the sequences
            self._find_similar_sequences(key)

    def _group_all_sequences(self):
        """Groups all sequnces together so the clustal output is all of them compared to each other 
        """
        self._sequences_grouped['all'] = list()
        for key in self.sequences.keys():
            self._sequences_grouped['all'].append(key)

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

    def add_accessibility(self, accessibility_seq):
        self.has_accessibility = True
        for sequence in self.sequences:
            for index, accessability_char in enumerate(accessibility_seq):
                index_char_obj = self.sequences[sequence][index]
                if accessability_char == 'N':
                    index_char_obj.is_accessible = False
                    self.num_nucleotides_inaccessible += 1
                else:
                    index_char_obj.is_accessible = True
                    self.num_nucleotides_accessible += 1

        info(logger, f'{logger.name} has {self.num_nucleotides_inaccessible} nucleotides inaccessible')


    def _get_length(self):
        return self.seq_end - self.seq_start + 1
    
    #CSV related CSV methods
    def enable_csv(self, file_path):
        self.csv_wanted = True
        self.file_path = file_path
    
    def chromosome_name(self, name):
        return name
        
    def _motif_and_count_rows(self):
        self.motif_counts_csv = []
        for motif_descriptor in self.motif_counts:
            for motif in self.motif_counts[motif_descriptor]:
                self.motif_counts_csv.append((self.name,
                                              self.seq_start,
                                              self.seq_end,
                                              motif,
                                              self.motif_counts[motif_descriptor][motif]))

    def _motif_descriptor_coverage(self):
        tmp_array = []
        for motif_descriptor in self.coverage:
            tmp_array.append((self.name,
                              self.seq_start,
                              self.seq_end,
                              motif_descriptor,
                              self.coverage[motif_descriptor]))
            
        self.coverage_csv = tmp_array    
        
    def _summary_stats(self):
        #fill with NaN if variants were not given
        if not self.variants_given:
            variants_found = "NaN"
        else:
            variants_found = self.variants_found
        
        #fill with NaN if accessibility was not given
        if not self.has_accessibility:
            num_variants_accessible = "NaN"
            num_nucleotides_accessible = "NaN"
        else:
            num_variants_accessible = self.num_variants_accessible
            num_nucleotides_accessible = self.num_nucleotides_accessible
        
        if self.pi_scores_array != None and len(self.pi_scores_array) >= 2:
            pi_scores_mean = round(statistics.mean(self.pi_scores_array), 3)
            pi_scores_stdev = round(statistics.stdev(self.pi_scores_array), 3)
        elif self.pi_scores_array != None and len(self.pi_scores_array) == 1:
            pi_scores_mean = round(self.pi_scores_array[0], 3)
            pi_scores_stdev = 0
        else:
            pi_scores_mean = "NaN"
            pi_scores_stdev = "NaN"
        
        mean_missing, std_missing = self._calculate_genotype_stats()
        
        total_highlight_coverage = self._calculate_total_coverage()
        
        self.summary_csv = [[self.file_path,
                             self.name,
                             self.seq_start,
                             self.seq_end,
                             self._get_length(),
                             variants_found,
                             num_variants_accessible,
                             num_nucleotides_accessible,
                             pi_scores_mean,
                             pi_scores_stdev,
                             mean_missing,
                             std_missing,
                             self.sequence_positions_N,
                             total_highlight_coverage]]
        
        for motif_name in self.motif_counts:
            self.summary_csv[0].append(len(self.motif_counts[motif_name]))
            
            this_sequence = list(self.motif_coverage.keys())[0]
            self.summary_csv[0].append(self.motif_coverage[this_sequence][motif_name])
            
    def _calculate_total_coverage(self):
        #there should only be 1 sequence when this is called.
        #this method does not get called for fasta highlighter
        #maybe inforce this by just grabbing the 0th?
        num_highlighted = 0
        for seq in self.sequences:
            for char in self.sequences[seq]:
                if char.modified:
                    num_highlighted += 1
            
        return num_highlighted
            
    
    def _calculate_genotype_stats(self):
        """This function returns the mean of the number of samples that are valid for each variant. It also returns the standard deviation of that number

        Returns:
            tuple: (mean, stdev)
        """
        num_missing_samples = []
        for _, (num_samples, num_invalid) in self.genotype_dict.items():
            num_missing_samples.append(num_invalid)
        if len(num_missing_samples) >= 2:
            mean_missing = round(statistics.mean(num_missing_samples),3)
            std_missing = round(statistics.stdev(num_missing_samples),3)
        elif len(num_missing_samples) == 1:   
            mean_missing = num_missing_samples[0]
            std_missing = 0
        else:
            mean_missing = 'NaN'
            std_missing = 'NaN'
        
        return (mean_missing, std_missing)
            
    def _calc_percentage(self, numerator, decimal_places):
        return round((numerator/self._get_length())*100, decimal_places)
            
    def _variant_statistics(self):
        self.varaints_csv = self.variants_with_percent 
   
    def _save_csv_data(self):
        self._motif_and_count_rows()
        self._motif_descriptor_coverage()
        self._summary_stats()
        if self.variant_data != None:
            self._variant_statistics()
        
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

        html_class_string += """.clear{
            background:white !important;
        }"""

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

        button_string += "\n</span>"

        button_string += '\n<script type="text/javascript">\n'
        button_string += "$(document).ready(function () {\n"

        button_string += """$('[data-toggle="tooltip"]').tooltip();\n"""

        keys_reverse = keys[::-1]
    
        opposite_lookup_table = {}
        
        for index, key in enumerate(keys):
            opposite_lookup_table[key] = keys_reverse[index]

        for key in keys:
            button_string += f"""$("#toggle_{key}").click(function() """ + "{\n"
            button_string += f"""   $( "span.{key}" ).toggleClass( "clear" );\n"""
            button_string += f"""   $( "span.purple" ).toggleClass( "{opposite_lookup_table[key]}" );"""
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
    
    def _log_variants(self, seq_name, chars):
        """Logs variant data gathered over the course of the generating the html for this highlight
        """
        #guard clause in case I do an oops and put this in the wrong spot
        if self.variant_data == None:
            raise Exception("Cannot run log variants without variant data loaded")
        
        if self.wrong_chars == 0:
            info(logger, f'All variants in {seq_name} match with the reference allele at their positions')
        else:
            warning(logger, f'{self.wrong_chars} Variants out of {len(self.variant_data)} have been found in {seq_name} which the reference allele does not match the underlying sequence. This is {round(self.wrong_chars/len(self.variant_data), 3)} percent')

        info(logger, f'Num variants found: {self.variants_found} within a region containing {len(chars)} nucleotides')
        info(logger, f'Percent of variable nucleotides in region: {self.variants_found/len(chars)}')

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

    def _compare_append_rows(self, row: list, counter: int, max_len: int, key : str, row_end_position: int):
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

    def add_variant_data(self, df, max_missing_frac=None, min_allele_freq=None) -> None:
        """Adds variant data to the object
            NOTE: current variants are only SNPs
        Args:
            file_path (str): A file path to variant data. This returns a dict of positions and what variations could be there and their positions 
        """
        self.variants_given = True
        variant_data = generate_variant_dict(self.seq_start, self.seq_end, df, logger, max_missing_frac, min_allele_freq)
        if len(variant_data) > 0:
            self.variant_data = variant_data
            
    def add_pi_data(self, site_pi_dict):
        self.site_pi_dict = site_pi_dict  
        self.pi_scores_array = []
        if self.variant_data != None:
            for pos in self.variant_data:
                if pos in self.site_pi_dict:
                    self.pi_scores_array.append(self.site_pi_dict[pos])

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
        
        seq_name = list(self.sequences.keys())[0]
        chars = self.sequences[seq_name]
        max = self.seq_start + len(chars)
        
        for x in range(position, position + 70):  # 70 is line width...
            x_offset = (x + self.offset - 1)
            if x_offset in self.variant_data:
                ref, alt, chance1, chance2, total_samples, samples_invalid = self.variant_data[x_offset]
                self.genotype_dict[x_offset] = (total_samples, samples_invalid)
                
                current_char = chars[x_offset-self.seq_start]
                if current_char.position != x_offset:
                    warning(logger, f'Variant not lined up with character position! Character position: {current_char.position}, Variant position: {x_offset}, Character in Object: {current_char.character}, Ref: {ref}, Alt: {alt}')

                if (x_offset-self.seq_start) < max:
                    if (ref != current_char.character):
                        self.wrong_chars += 1
                self.variants_found += 1
            
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

                self.variants_with_percent.append((self.name, self.seq_start, self.seq_end, current_char.position, ref, alt, chance1, chance2, current_char.is_accessible))
                
                if current_char.is_accessible == True:
                    self.num_variants_accessible += 1
                    accessibility = "accessible"
                elif current_char.is_accessible == False:
                    accessibility = "not accessible"
                    
                if current_char.is_accessible != None:
                    accessibility_string = f" and is {accessibility}"
                else:
                    accessibility_string = ""
                
                variant_string += f'<span style="color:rgb({red},{green},{blue})" data-toggle="tooltip" data-animation="false" title ="{ref}: {chance1}% {alt}: {chance2}%{accessibility_string}">^</span>'
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
    
    def _calculate_motif_stats(self):
        keys = self.sequences.keys()
        motif_coverage = {}
        motif_sets = {}
        for motif_name in self.motif_names:
            motif_sets[motif_name] = set()
            
        for key in keys:
            sequence = self.sequences[key]
            motif_coverage[key] = {'length': len(sequence)}
            for name in self.motif_names:
                motif_coverage[key][name] = 0
            for char in sequence:
                if char.motif_files != {}:
                    for motif_name in char.motif_files:
                        for motif in char.motif_files[motif_name]:
                            motif_sets[motif_name].add(motif)
                        if motif_name in motif_coverage[key]:
                            motif_coverage[key][motif_name] += 1
                            
        for key, value in motif_coverage.items():
            for motif_name in self.motif_names:
                if value[motif_name] == 0:
                    warning(logger, f'Sequence {key} did not have any found motifs for {motif_name}')
        
        return (motif_sets, motif_coverage)
    
    def _pretty_print_motifs(self):
        table_string = ""
        for motif_descriptor in self.motif_counts:
            table_string += f"""
            </br>
            <table>
                <thead>
                <tr>
                    {motif_descriptor} Motif Apperances
                </tr> 
                <tr>
                    <td>Motif</td>
                    <td>Count</td>    
                </tr> 
                </thead>
                <tbody>"""
            motif_counts = []
            for motif in self.motif_counts[motif_descriptor]:
                count = self.motif_counts[motif_descriptor][motif]
                motif_counts.append((motif, count))
            motif_counts.sort(key=lambda x:x[1], reverse=True)    
            
            for motif, count in motif_counts:
                row = f"""<tr>
                    <td>{motif}</td>
                    <td>{count}</td>
                    </tr> """
                table_string += row    
            table_string += "</tbody> </table>"
        return table_string
    
    def _pretty_print_variants(self, length):
        #print(self.variants_found, self.variants_found/length)
        return
    
    def _generate_table(self, num_variants, percent_variable, motifs_found, motif_coverage):
        unique_motifs_rows = self._unique_motifs_table(motifs_found)
        motif_coverage_table = self._motif_coverage_table(motif_coverage)
        if self.has_accessibility and self.variants_found > 0:
            accessibility_string = f"""
            <tr>
                <td>Percent of variants that are accessible:</td>
                <td>{round(self.num_variants_accessible/self.variants_found*100,1)}%</td>
            </tr>
            <tr>
                <td>Percent of nucleotides that are accessible:</td>
                <td>{self._calc_percentage(self.num_nucleotides_accessible, 1)}%</td>
            </tr>
            """
        else:
            accessibility_string = ""
        
        table_string = f"""<table>
            <thead>
            <tr>
                Summary Stats
            </tr> 
            </thead>
            <tbody>
            <tr>
                <td>Variants in region:</td>
                <td>{num_variants}</td>
            </tr>
            <tr>
                <td>Percent of nucleotides with variants:</td>
                <td>{percent_variable}%</td>
            </tr>
            {accessibility_string}
            {unique_motifs_rows}
            {motif_coverage_table}
            </tbody>
        </table>
        """
        
        return table_string
    
    def _unique_motifs_table(self, motifs_sets):
        table_rows = ''
        for motif_name in motifs_sets:
            row_string = self._stats_row_template(motif_name, len(motifs_sets[motif_name])) 
            table_rows += row_string
                    
        return table_rows
    
    def _motif_coverage_table(self, motif_coverage):
        table_string = ''
        for sequence_motif_info in motif_coverage:
            table_string += self._motif_row_template(motif_coverage[sequence_motif_info], sequence_motif_info)
        
        return table_string  
        
        
    def _motif_row_template(self, motif_info, sequence_name):
        length = motif_info['length']
        table_string = ""
        if len(list(self._sequences_grouped.keys())[-1]) == 1:
            table_string += f"""<tr>
                <td><b>{sequence_name}</b></td>
                </tr>"""
        for motif_name in self.motif_names:
            coverage =  round((motif_info[motif_name]/length) * 100, 1)
            self.coverage[motif_name] = coverage
            self.motif_percent_coverage[motif_name] = coverage
            table_string += f"""
                <tr>
                    <td>{motif_name} Percent Coverage:</td>
                    <td>{coverage}%</td>
                </tr>
            """
        return table_string
    
    def _stats_row_template(self, motif_description, uniq_found):
        row = f"""
            <tr>
                <td>Unique {motif_description} motifs found:</td>
                <td>{uniq_found}</td>
            </tr>"""
        return row
    
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
            if len(self.sequences) > 1:
                dynamic_html_string += "<br/> <span> New Sequence </span>"
            else:
                dynamic_html_string += "<br/>"
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

                    if counter + 1 >= stop:
                        row_end_position -= 1

                    dynamic_html_string += self._compare_append_rows(
                        row, counter, max_len, key, row_end_position)

                if row_end_position != None:
                    position = row_end_position + 1
                
                if len(rows_to_compare) > 1:
                    dynamic_html_string += self._append_stars(
                        max_len, rows_to_compare)

                dynamic_html_string += '</pre>'  # this is the last block since it's excluded
                counter += 1  # From the list.

        html_string += dynamic_html_string
        
        seq_name = list(self.sequences.keys())[0]
        chars = self.sequences[seq_name]
        
        if self.variant_data != None:   
            self._log_variants(seq_name, chars)
        else:
            num_sequnces = len(self.sequences.keys())
            if num_sequnces == 1:
                info(logger, f'{seq_name} has a region of length {len(chars)}')
            else:
                info(logger, f'{self.sequences.keys()} when alined are of length {len(chars)}')
        
                
        self.motif_sets, self.motif_coverage = self._calculate_motif_stats()
        motif_count_table = self._pretty_print_motifs()
        
        html_string += f'\n{self._generate_table(self.variants_found, round(self.variants_found/len(chars) * 100, 3), self.motif_sets, self.motif_coverage)}'        
        html_string += f'\n{motif_count_table}'
        
        # if self.variant_data != None:
        #     variant_stats = self._pretty_print_variants(len(chars))
        #     html_string += f'\n{variant_stats}'
        html_string += '\n</body>'
        
        if self.csv_wanted:
            self._save_csv_data()
        
        self.outputs.append(html_string)     
        return self.outputs[-1]
    
