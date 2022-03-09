class Character:
    def __init__(self, char: str):
        self.character = char
        self.color = None
        
        self.html_string = None
        self.tooltip = None
        
        self.motif_files = {} #file_name/id -> list of motifs found at this character 
                            #Update to python 3.9+ and use dict[str, list] to specify types :)
        self.modified = False
        
    def generate_html_string(self):
        as_html = "<span"
        if self.modified == False:
            return self.character
        else:
            if self.color != None:
                as_html += ' class="' + self.color + '"'
            
            if len(self.motif_files) > 0:
                if self.tooltip == None:
                    self.generate_tooltip()            
                as_html += ' data-toggle="tooltip" data-animation="false" title = "' + self.tooltip + '"' 

            as_html += '>' + self.character + "</span>"
        return as_html
    
    def generate_tooltip(self):
        tooltip = ""
        for descriptor in self.motif_files:
            tooltip += " " + str(descriptor) + " is: "
            for motif_id in self.motif_files[descriptor]:
                tooltip += str(motif_id) + ", "
            tooltip = tooltip[:-2]
            
        self.tooltip = tooltip
            
    def set_color(self, color: str):
        if self.color != color and self.color != None:
            self.color = "purple"
        else:
            self.color = color
            
        self.modified = True
        
    def add_motif(self, motif_descriptor:str, motif_id:str, color:str):
        if motif_descriptor in self.motif_files:
            self.motif_files[motif_descriptor].add(motif_id)
        else:
            self.motif_files[motif_descriptor] = set()
            self.motif_files[motif_descriptor].add(motif_id)
            
        self.set_color(color)
        
    def set_indel_color(self, char_left, char_right):
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
        if self.html_string == None:
            self.html_string = self.generate_html_string()
        
        return self.html_string  