"""Module that contains the character class.
"""
from clustal_highlighter.modules.data_structures.variant_classes import variant_stats
import json

class Character:
    """A character class, dedicated to simplifying how I store and represent nucleotides and their highlights"""

    def __init__(self, char: str, pos: int):
        self.character = char
        self.color = None
        self.position = pos

        self.html_string = None
        self.tooltip = None

        self.motif_files = {}  # file_name/id -> Set of motifs found at this character
        self.modified = False

        self.is_accessible = "N/A"
        
        self.variant_stats:variant_stats = None
        
        # global variables for the 3 colors (steps) in the color bar in the HTML pages
        self.color_bar_val1 = (54, 98, 57)
        self.color_bar_val2 = (177, 63, 35)
        self.color_bar_val3 = (288, 98, 17)

    def add_variant(self, variant_info:variant_stats):
        self.variant_stats = variant_info
        self.modified = True

    def generate_variant_div(self):
        # Alert! These calculations for ref_percent_100 and alt_percent_100
        # are done again in highlights.py... Please change both if you change
        # 1 unless there is a good reason for it.
        ref_percent = float(round(self.variant_stats.ref_percent, 3))
        ref_percent_100 = float(round((ref_percent*100),3))
        alt_percent_100 = float(round((self.variant_stats.alt_percent*100),3))
        
        #colorbar color match with variant percent...
        new_color = None
        if ref_percent <= 0.5:
            relative_percent = ref_percent/0.5
            new_color = self._calculate_color(relative_percent, self.color_bar_val1, self.color_bar_val2)
        else:
            relative_percent = (ref_percent-0.5)/0.5
            new_color = self._calculate_color(relative_percent, self.color_bar_val2, self.color_bar_val3)

        if self.is_accessible == True:
            self.num_variants_accessible += 1
            accessibility = "accessible"
        elif self.is_accessible == False:
            accessibility = "not accessible"

        if self.is_accessible != "N/A":
            accessibility_string = f" and is {accessibility}"
        else:
            accessibility_string = ""

        ref, alt = self.variant_stats.ref, self.variant_stats.alt

        return  f'<div class="variant_hat" style="color:hsl({new_color[0]},{new_color[1]}%,{new_color[2]}%)" data-toggle="tooltip" data-ref="{ref_percent_100}" data-animation="false" title ="{ref}: {ref_percent_100}% {alt}: {alt_percent_100}%{accessibility_string}">^</div>'

    def _calculate_color(self, ref_percent, color1, color2):
            hue_diff = color2[0] - color1[0]
            sat_diff = color2[1] - color1[1]
            lumen_diff = color2[2] - color1[2]
            return (color1[0] + (hue_diff*ref_percent),
                    color1[1] + (sat_diff*ref_percent),
                    color1[2] + (lumen_diff*ref_percent))
    
    def get_variant_dict(self):
        # Alert! These calculations for ref_percent_100 and alt_percent_100
        # are done again in highlights.py... Please change both if you change
        # 1 unless there is a good reason for it.
        ref_percent = float(round(self.variant_stats.ref_percent, 3))
        ref_percent_100 = float(round((ref_percent*100),3))
        alt_percent_100 = float(round((self.variant_stats.alt_percent*100),3))
        
        #colorbar color match with variant percent...
        new_color = None
        if ref_percent <= 0.5:
            relative_percent = ref_percent/0.5
            new_color = self._calculate_color(relative_percent, self.color_bar_val1, self.color_bar_val2)
        else:
            relative_percent = (ref_percent-0.5)/0.5
            new_color = self._calculate_color(relative_percent, self.color_bar_val2, self.color_bar_val3)

        ref, alt = self.variant_stats.ref, self.variant_stats.alt
        return {
            "color":f'hsl({new_color[0]},{new_color[1]}%,{new_color[2]}%)',
            "accessibility": f'{self.is_accessible}',
            "ref_percent": ref_percent_100,
            "alt_percent": alt_percent_100   
        }
    
    def get_motif_dict(self):
        ret_dict = {}
        for motif, motif_set in self.motif_files.items():
            ret_dict[motif] = list(motif_set)
        ret_dict['color'] = self.color
        return ret_dict 
    
    def generate_html(self):
        if self.modified is False:
            return self.character
        else:            
            if len(self.motif_files) != 0:
                motif_json = json.dumps(self.get_motif_dict())
                motif_data = f"data-motif='{motif_json}'"
            else:
                motif_data = ""
            if self.variant_stats != None:
                variant_json = json.dumps(self.get_variant_dict())
                variant_data = f"data-variant='{variant_json}'"
            else:
                variant_data = ""
                
            color_str = None
            if self.color == None:
                color_str = ""
            else:
                color_str = f"data-{self.color}"
            
            return f"""<highlight-variant {color_str} data-position='{self.position}' data-character='{self.character}' {motif_data} {variant_data}></highlight-variant>"""
    
    def generate_html_string(self):
        """Generates an html string which includes the tooltip and background class color

        Returns:
            String: The string of html
        """
        as_html = "<span"

        if self.modified is False:
            return self.character

        class_list = []
        
        if self.color is not None:
            class_list.append(self.color)
            class_list.append("motif")
            
        # add html classes to span string
        if class_list != []:
            classes = ""
            for html_class in class_list:
                classes += html_class + " "
            classes = classes[0:-1]
            
            as_html += f' class = "{classes}"'

        if len(self.motif_files) > 0:
            self.generate_tooltip()
            as_html += f' data-toggle="tooltip" data-animation="false" title = "{self.tooltip}"'

        as_html += ">" + self.character + "</span>"
        
        if self.variant_stats is not None:
            variant_hat = self.generate_variant_div()
            as_html = f'<span class="has_variant">{as_html}{variant_hat}</span>'
        
        return as_html

    def generate_tooltip(self):
        """Generates the tooltip based on the motif's that were presented to this character"""
        tooltip = ""
        for descriptor, motifs in self.motif_files.items():
            tooltip += " " + str(descriptor) + " is: "
            for motif in motifs:
                tooltip += str(motif) + ", "
            tooltip = tooltip[:-2]

        self.tooltip = tooltip

    def set_color(self, color: str):
        """Sets the color of this character

        Args:
            color (str): A string of what color this character is set to. This would be something like "blue" or "red"
        """
        if self.color != color and self.color is not None:
            self.color = "purple"
        else:
            self.color = color

        self.modified = True

    def add_motif(self, motif_descriptor: str, motif_id: str, color: str):
        """Adds a motif to the current character. This is motif data from when a highlight is called and a fimo.tsv is passed

        Args:
            motif_descriptor (str): A description of the motif. This is generally something like "streme" for streme generated motifs or "jaspar" if gathered in other ways
            motif_id (str): The id of the motif currently being presented to this character
            color (str): the color this motif should display in the output file
        """
        if motif_descriptor in self.motif_files:
            self.motif_files[motif_descriptor].add(motif_id)
        else:
            self.motif_files[motif_descriptor] = set()
            self.motif_files[motif_descriptor].add(motif_id)

        self.set_color(color)

    def set_indel_color(self, char_left, char_right):
        """If this character is an indel, then this character has additional logic to define if it should have a color or not

        Args:
            char_left (Character): The first non-motif character to the left of the group of indels that include this indel
            char_right (Character): The right character similar to the left
        """
        if char_left is None or char_right is None:
            return

        left_motif_dict = char_left.motif_files
        right_motif_dict = char_right.motif_files

        if left_motif_dict == right_motif_dict and len(left_motif_dict) == 1:
            self.set_color(char_left.color)  # Left and right in this case have == color
        elif left_motif_dict == right_motif_dict and len(left_motif_dict) > 1:
            self.set_color("purple")

    def set_accessible(self, is_accessible):
        """Setter for accessability

        Args:
            is_accessible (bool): Sets if this nucleotide is accessible or not
        """
        self.is_accessible = is_accessible

    def to_string(self) -> str:
        """Gets the html string representation of this character

        Returns:
            str: The html string that represents this character
        """
        # if self.html_string == None:
        self.html_string = self.generate_html()

        return self.html_string
