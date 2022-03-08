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
    
    def verify_color(self, motif_descriptor):
        for descriptor in self.motif_files:
            motifs_in_same_descriptor = self.motif_files[descriptor]
            
            if self.character == "-" and len(motifs_in_same_descriptor) > 1 and descriptor == motif_descriptor:
                self.color = None
            
    def set_color(self, color: str, motif_descriptor: str):
        if self.color != color and self.color != None:
            self.color = "purple"
        else:
            self.color = color
            
        self.verify_color(motif_descriptor)
        self.modified = True
        
    def add_motif(self, motif_descriptor:str, motif_id:str, color:str):
        if motif_descriptor in self.motif_files:
            self.motif_files[motif_descriptor].add(motif_id)
        else:
            self.motif_files[motif_descriptor] = set()
            self.motif_files[motif_descriptor].add(motif_id)
            
        self.set_color(color, motif_descriptor)
        
    def to_string(self) -> str:
        if self.html_string == None:
            self.html_string = self.generate_html_string()
        
        return self.html_string
    