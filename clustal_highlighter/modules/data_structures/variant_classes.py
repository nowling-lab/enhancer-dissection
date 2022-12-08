from dataclasses import dataclass


@dataclass(repr=True)
class variant_stats:
    "Class to hold the data returned from parsing the VCF file"
    ref: str
    alt: str
    ref_percent: float
    alt_percent: float
    num_samples: int
    missing_allele_count: int

    def as_tuple(self):
        return (
            self.ref,
            self.alt,
            self.ref_percent,
            self.alt_percent,
            self.num_samples,
            self.missing_allele_count,
        )
