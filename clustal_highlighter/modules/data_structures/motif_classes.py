from dataclasses import dataclass


@dataclass(repr=True)
class Motif:
    start: int
    stop: int
    motif_alt_id: str
    mathed_sequence: str
    orientation: str
    p_value: str
    
    def as_tuple(self):
        return (self.start, self.stop, self.motif_alt_id, self.mathed_sequence, self.orientation, self.p_value)