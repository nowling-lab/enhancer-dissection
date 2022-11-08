from dataclasses import dataclass, fields
        
@dataclass(repr=True)
class motif_highlights:
    "Class to keep track of how many fimo highlights were applied"
    motif_name: str
    motifs_in_file: int
    motifs_applied: int            
    
    def to_string(self):
        return f'{self.motif_name} had {self.motifs_in_file} highlights in file and {self.motifs_applied} highlights applied'
    
    def is_equal(self):
        if self.motifs_in_file == self.motifs_applied:
            return True
        else:
            return False