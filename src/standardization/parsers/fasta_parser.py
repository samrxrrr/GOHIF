"""
GOHIF FASTA Parser
Scientific Metadata Enrichment
Modular Refactor Version 3.0
"""

from pathlib import Path

from src.standardization.base_parser import BaseParser

from src.standardization.common.metadata_builder import build_metadata

from src.standardization.common.sequence_utils import (
    DNA_ALPHABET,
    RNA_ALPHABET,
    PROTEIN_ALPHABET,
    infer_molecule_type,
    gc_content,
    base_counts,
    ambiguous_count,
)

from src.standardization.common.statistics import (
    summary_statistics,
    n50,
    n90,
    coefficient_of_variation,
)

from src.standardization.common.validators import (
    validate_fasta_structure,
    validation_status,
)


class FASTAParser(BaseParser):

    PARSER_NAME = "FASTAParser"
    PARSER_VERSION = "3.0"

    SUPPORTED_EXTENSIONS = {
        ".fa",
        ".fasta",
        ".faa",
        ".fna",
    }

    def detect(self, path):

        return (
            Path(path).suffix.lower()
            in self.SUPPORTED_EXTENSIONS
        )

    def read_fasta(self, path):
        """
        Streaming FASTA reader.

        Yields
        ------
        tuple
            (header, sequence)
        """

        header = None
        sequence = []

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as handle:

            for line in handle:

                line = line.strip()

                if not line:
                    continue

                if line.startswith(">"):

                    if header is not None:

                        yield (
                            header,
                            "".join(sequence),
                        )

                    header = line[1:].strip()
                    sequence = []

                else:

                    sequence.append(line)

        if header is not None:

            yield (
                header,
                "".join(sequence),
            )

    @staticmethod
    def _invalid_character_count(
        sequence,
        molecule_type,
    ):

        sequence = sequence.upper()

        if molecule_type in (
            "DNA",
            "RNA",
        ):

            valid = (
                DNA_ALPHABET
                | RNA_ALPHABET
            )

        else:

            valid = PROTEIN_ALPHABET

        return sum(
            character not in valid
            for character in sequence
        )

    def extract_metadata(self, path):

        path = Path(path)

        sequence_count = 0
        total_length = 0

        first_header = None
        shortest_header = None
        longest_header = None

        shortest_length = None
        longest_length = 0

        duplicate_headers = 0
        empty_sequences = 0
        ambiguous_characters = 0
        invalid_characters = 0

        seen_headers = set()

        lengths = []

        molecule_counts = {
            "DNA": 0,
            "RNA": 0,
            "PROTEIN": 0,
        }

        nucleotide_gc_values = []

        totals = {
            "A": 0,
            "C": 0,
            "G": 0,
            "T": 0,
            "U": 0,
            "N": 0,
        }

        for header, sequence in self.read_fasta(
            path
        ):

            sequence = sequence.upper()

            length = len(sequence)

            sequence_count += 1
            total_length += length

            lengths.append(length)

            if first_header is None:
                first_header = header

            if (
                shortest_length is None
                or length < shortest_length
            ):

                shortest_length = length
                shortest_header = header

            if length > longest_length:

                longest_length = length
                longest_header = header

            if header in seen_headers:

                duplicate_headers += 1

            seen_headers.add(header)

            if length == 0:

                empty_sequences += 1

            molecule = infer_molecule_type(
                sequence
            )

            molecule_counts[molecule] += 1

            counts = base_counts(sequence)

            for base in totals:

                totals[base] += counts[base]

            ambiguous_characters += (
                ambiguous_count(sequence)
            )

            invalid_characters += (
                self._invalid_character_count(
                    sequence,
                    molecule,
                )
            )

            if molecule in (
                "DNA",
                "RNA",
            ):

                nucleotide_gc_values.append(
                    gc_content(sequence)
                )

        stats = summary_statistics(
            lengths
        )

        if nucleotide_gc_values:

            average_gc = round(
                sum(nucleotide_gc_values)
                / len(nucleotide_gc_values),
                2,
            )

        else:

            average_gc = 0

        gc_count = (
            totals["G"]
            + totals["C"]
        )

        at_count = (
            totals["A"]
            + totals["T"]
            + totals["U"]
        )

        if total_length:

            overall_gc = round(
                gc_count
                * 100
                / total_length,
                2,
            )

            overall_at = round(
                at_count
                * 100
                / total_length,
                2,
            )

        else:

            overall_gc = 0
            overall_at = 0

        if sequence_count:

            dominant_type = max(
                molecule_counts,
                key=molecule_counts.get,
            )

        else:

            dominant_type = "UNKNOWN"

        scientific_metadata = {

            "Sequence_Count":
                sequence_count,

            "Total_Residues":
                total_length,

            "Min_Length":
                stats["Minimum"],

            "Max_Length":
                stats["Maximum"],

            "Average_Length":
                stats["Mean"],

            "Median_Length":
                stats["Median"],

            "Length_Standard_Deviation":
                stats[
                    "Standard_Deviation"
                ],

            "Length_CV_Percent":
                coefficient_of_variation(
                    lengths
                ),

            "N50":
                n50(lengths),

            "N90":
                n90(lengths),

            "First_Header":
                first_header,

            "Shortest_Header":
                shortest_header,

            "Longest_Header":
                longest_header,

            "Molecule_Type":
                dominant_type,

            "DNA_Sequence_Count":
                molecule_counts["DNA"],

            "RNA_Sequence_Count":
                molecule_counts["RNA"],

            "Protein_Sequence_Count":
                molecule_counts[
                    "PROTEIN"
                ],

            "Average_GC_Content":
                average_gc,

            "Overall_GC_Content":
                overall_gc,

            "Overall_AT_Content":
                overall_at,

            "GC_Count":
                gc_count,

            "AT_Count":
                at_count,

            "A_Count":
                totals["A"],

            "C_Count":
                totals["C"],

            "G_Count":
                totals["G"],

            "T_Count":
                totals["T"],

            "U_Count":
                totals["U"],

            "N_Count":
                totals["N"],

            "Duplicate_Headers":
                duplicate_headers,

            "Empty_Sequences":
                empty_sequences,

            "Ambiguous_Characters":
                ambiguous_characters,

            "Invalid_Characters":
                invalid_characters,
        }

        valid = validate_fasta_structure(
            path
        )

        return build_metadata(
            path=path,
            parser_name=self.PARSER_NAME,
            parser_version=self.PARSER_VERSION,
            scientific_metadata=scientific_metadata,
            validation_status=validation_status(
                valid
            ),
        )

    def validate(self, path):

        return validate_fasta_structure(
            path
        )

    def standardize(
        self,
        path,
        output_dir,
    ):

        return path

    def summarize(self, path):

        return self.extract_metadata(
            path
        )
