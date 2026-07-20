"""
GOHIF Parser Registry
Phase 5

Central registry for all metadata parsers.
"""

from src.standardization.parsers.tabular_parser import TabularParser
from src.standardization.parsers.json_parser import JSONParser
from src.standardization.parsers.fasta_parser import FASTAParser
from src.standardization.parsers.fastq_parser import FASTQParser
from src.standardization.parsers.generic_data_parser import GenericDataParser
from src.standardization.parsers.hmmer_parser import HMMERParser
from src.standardization.parsers.archive_parser import ArchiveParser


PARSER_REGISTRY = {

    "TABULAR": TabularParser(),

    "JSON": JSONParser(),

    "FASTA": FASTAParser(),

    "FASTQ": FASTQParser(),

    "GENERIC_DATA": GenericDataParser(),

    "HMMER_DB": HMMERParser(),

    "ARCHIVE": ArchiveParser(),

}


def get_parser(file_class):
    return PARSER_REGISTRY.get(file_class)


def supported_classes():
    return sorted(PARSER_REGISTRY.keys())


def parser_count():
    return len(PARSER_REGISTRY)
