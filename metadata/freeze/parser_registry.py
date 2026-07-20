"""
GOHIF Parser Registry
"""

PARSER_REGISTRY = {

    "FASTA": "FASTAParser",
    "FASTQ": "FASTQParser",
    "SRA": "SRAParser",

    "TABULAR": "TabularParser",
    "TEXT": "TextParser",
    "JSON": "JSONParser",

    "ARCHIVE": "ArchiveParser",

    "BLAST_DB": "BlastDBParser",

    "DATABASE_SEGMENT": "DatabaseSegmentParser",

    "HMMER_DB": "HMMERParser",

    "GENERIC_DATA": "GenericDataParser",

    "PROTEIN_STRUCTURE": "PDBParser"

}


def get_parser(file_class):

    return PARSER_REGISTRY.get(file_class)
