class Character:
    def __init__(self, char: str, pos: int):
        self.character = char
        self.color = None
        self.position = pos
        
        self.html_string = None
        self.tooltip = None
        
        self.motif_files = {} #file_name/id -> list of motifs found at this character 
                            #Update to python 3.9+ and use dict[str, list] to specify types :)
        self.modified = False
        
    def generate_html_string(self):
        """Generates an html string which includes the tooltip and background class color

        Returns:
            String: The string of html
        """     
        as_html = "<span"

        if self.modified == False:
            return self.character
        else:
            if self.color != None:
                as_html += ' class="' + self.color + '"'
            
            if len(self.motif_files) > 0:
                self.generate_tooltip()            
                as_html += ' data-toggle="tooltip" data-animation="false" title = "' + self.tooltip + '"' 

            as_html += '>' + self.character + "</span>"
        return as_html
    
    def generate_tooltip(self):
        """Generates the tooltip based on the motif's that were presented to this character
        """
        tooltip = ""
        for descriptor in self.motif_files:
            tooltip += " " + str(descriptor) + " is: "
            for motif_id in self.motif_files[descriptor]:
                tooltip += str(motif_id) + ", "
            tooltip = tooltip[:-2]
            
        self.tooltip = tooltip
            
    def set_color(self, color: str):
        """Sets the color of this character

        Args:
            color (str): A string of what color this character is set to. This would be something like "blue" or "red"
        """
        if self.color != color and self.color != None:
            self.color = "purple"
        else:
            self.color = color
            
        self.modified = True
        
    def add_motif(self, motif_descriptor:str, motif_id:str, color:str):
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
        # TODO Go over this with nowling. I forgot this logic and didn't document it. Sadge
        if char_left == None or char_right == None:
            return
        else:  
            left_motif_dict = char_left.motif_files
            right_motif_dict = char_right.motif_files
            
            if left_motif_dict == right_motif_dict and len(left_motif_dict) == 1:
                self.set_color(char_left.color) #Left and right in this case have == color
            elif left_motif_dict == right_motif_dict and len(left_motif_dict) > 1:
                self.set_color('purple')
        
    def to_string(self) -> str:
        """Gets the html string representation of this character

        Returns:
            str: The html string that represents this character
        """
        #if self.html_string == None:
        self.html_string = self.generate_html_string()
        
        return self.html_string  