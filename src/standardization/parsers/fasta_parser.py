"""
GOHIF FASTA Parser
Phase 6 - Scientific Metadata Enrichment
Version 2.2
"""

from pathlib import Path

from src.standardization.base_parser import BaseParser


class FASTAParser(BaseParser):

    DNA_ALPHABET = set("ACGTN")

    RNA_ALPHABET = set("ACGUN")

    PROTEIN_ALPHABET = set(
        "ABCDEFGHIKLMNPQRSTVWXYZ*"
    )

    def detect(self, path):

        return Path(path).suffix.lower() in [

            ".fa",
            ".fasta",
            ".faa",
            ".fna"

        ]

    def read_fasta(self, path):

        header = None

        sequence = []

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as handle:

            for line in handle:

                line = line.strip()

                if not line:
                    continue

                if line.startswith(">"):

                    if header is not None:

                        yield header, "".join(sequence)

                    header = line[1:].strip()

                    sequence = []

                else:

                    sequence.append(line)

        if header is not None:

            yield header, "".join(sequence)

    def infer_molecule_type(self, sequence):

        seq = sequence.upper()

        chars = set(seq)

        if chars <= self.DNA_ALPHABET:
            return "DNA"

        if chars <= self.RNA_ALPHABET:
            return "RNA"

        return "PROTEIN"

    def gc_content(self, sequence):

        seq = sequence.upper()

        if len(seq) == 0:

            return 0.0

        gc = seq.count("G") + seq.count("C")

        return round(
            gc * 100 / len(seq),
            2
        )

    def extract_metadata(self, path):

        path = Path(path)

        sequence_count = 0

        total_length = 0

        min_length = None

        max_length = 0

        first_header = None

        shortest_header = None

        longest_header = None

        duplicate_headers = 0

        empty_sequences = 0

        ambiguous_characters = 0

        invalid_characters = 0

        gc_total = 0

        seen_headers = set()

        molecule_counts = {

            "DNA": 0,

            "RNA": 0,

            "PROTEIN": 0

        }

        total_a = 0

        total_c = 0

        total_g = 0

        total_t = 0

        total_u = 0

        total_n = 0

        for header, sequence in self.read_fasta(path):

            sequence = sequence.upper()

            length = len(sequence)

            sequence_count += 1

            total_length += length

            if min_length is None:

                min_length = length
                shortest_header = header

            elif length < min_length:

                min_length = length
                shortest_header = header

            if length > max_length:

                max_length = length
                longest_header = header

            if first_header is None:

                first_header = header

            if header in seen_headers:

                duplicate_headers += 1

            seen_headers.add(header)

            if length == 0:

                empty_sequences += 1

            molecule = self.infer_molecule_type(sequence)

            molecule_counts[molecule] += 1

            total_a += sequence.count("A")
            total_c += sequence.count("C")
            total_g += sequence.count("G")
            total_t += sequence.count("T")
            total_u += sequence.count("U")
            total_n += sequence.count("N")

            if molecule in ("DNA", "RNA"):

                gc_total += self.gc_content(sequence)

                valid = self.DNA_ALPHABET | self.RNA_ALPHABET

            else:

                valid = self.PROTEIN_ALPHABET

            for char in sequence:

                if char not in valid:

                    invalid_characters += 1

            if molecule == "DNA":

                ambiguous_characters += sequence.count("N")

            elif molecule == "RNA":

                ambiguous_characters += sequence.count("N")

            else:

                ambiguous_characters += sequence.count("X")

        if sequence_count:

            average_length = round(
                total_length / sequence_count,
                2
            )

        else:

            average_length = 0

        dna_rna_sequences = (

            molecule_counts["DNA"] +
            molecule_counts["RNA"]

        )

        if dna_rna_sequences:

            average_gc = round(

                gc_total /
                dna_rna_sequences,

                2

            )

        else:

            average_gc = 0

        if total_length:

            gc_count = total_g + total_c

            at_count = total_a + total_t + total_u

            gc_percent = round(

                gc_count * 100 /
                total_length,

                2

            )

            at_percent = round(

                at_count * 100 /
                total_length,

                2

            )

        else:

            gc_count = 0

            at_count = 0

            gc_percent = 0

            at_percent = 0

        dominant_type = max(

            molecule_counts,

            key=molecule_counts.get

        )

        dominant_type = max(

            molecule_counts,

            key=molecule_counts.get

        )
        metadata = {

            "Filename":
                path.name,

            "Extension":
                path.suffix.lower(),

            "File_Size_MB":
                round(
                    path.stat().st_size / 1024 / 1024,
                    6
                ),

            "Sequence_Count":
                sequence_count,

            "Total_Residues":
                total_length,

            "Min_Length":
                min_length,

            "Max_Length":
                max_length,

            "Average_Length":
                average_length,

            "First_Header":
                first_header,

            "Shortest_Header":
                shortest_header,

            "Longest_Header":
                longest_header,

            "Molecule_Type":
                dominant_type,

            "Average_GC_Content":
                average_gc,

            "Overall_GC_Content":
                gc_percent,

            "Overall_AT_Content":
                at_percent,

            "GC_Count":
                gc_count,

            "AT_Count":
                at_count,

            "A_Count":
                total_a,

            "C_Count":
                total_c,

            "G_Count":
                total_g,

            "T_Count":
                total_t,

            "U_Count":
                total_u,

            "N_Count":
                total_n,

            "Duplicate_Headers":
                duplicate_headers,

            "Empty_Sequences":
                empty_sequences,

            "Ambiguous_Characters":
                ambiguous_characters,

            "Invalid_Characters":
                invalid_characters,

            "SHA256":
                self.sha256(path),

            "Validation_Status":
                "VALID",

            "Parser_Name":
                "FASTAParser",

            "Parser_Version":
                "2.2"

        }

        return metadata

    def validate(self, path):

        return True

    def standardize(self, path, output_dir):

        return path

    def summarize(self, path):

        return self.extract_metadata(path)
