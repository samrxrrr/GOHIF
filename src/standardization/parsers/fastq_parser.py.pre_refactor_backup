"""
GOHIF FASTQ Parser
Phase 6 - Scientific Metadata Enrichment
Version 2.0
"""

from pathlib import Path

from src.standardization.base_parser import BaseParser


class FASTQParser(BaseParser):

    def detect(self, path):

        return Path(path).suffix.lower() in [

            ".fastq",
            ".fq"

        ]

    def read_fastq(self, path):
        """
        Streaming FASTQ reader.

        Yields:
            (header, sequence, quality)
        """

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as handle:

            while True:

                header = handle.readline()

                if not header:
                    break

                sequence = handle.readline()

                plus = handle.readline()

                quality = handle.readline()

                if not quality:
                    break

                yield (

                    header.strip()[1:],

                    sequence.strip(),

                    quality.strip()

                )

    def phred_scores(self, quality):

        return [

            ord(char) - 33

            for char in quality

        ]

    def gc_content(self, sequence):

        seq = sequence.upper()

        if len(seq) == 0:

            return 0

        gc = seq.count("G") + seq.count("C")

        return round(

            gc * 100 / len(seq),

            2

        )

    def extract_metadata(self, path):

        path = Path(path)

        read_count = 0

        total_length = 0

        min_length = None

        max_length = 0

        gc_total = 0

        total_quality = 0

        quality_values = []

        first_read = None

        total_n = 0
        min_quality = None

        max_quality = None

        for header, sequence, quality in self.read_fastq(path):

            sequence = sequence.upper()

            length = len(sequence)

            scores = self.phred_scores(quality)

            read_count += 1

            total_length += length

            if first_read is None:

                first_read = header

            if min_length is None:

                min_length = length

            elif length < min_length:

                min_length = length

            if length > max_length:

                max_length = length

            gc_total += self.gc_content(sequence)

            total_n += sequence.count("N")

            if scores:

                total_quality += sum(scores)

                quality_values.extend(scores)

                local_min = min(scores)

                local_max = max(scores)

                if min_quality is None:

                    min_quality = local_min

                elif local_min < min_quality:

                    min_quality = local_min

                if max_quality is None:

                    max_quality = local_max

                elif local_max > max_quality:

                    max_quality = local_max

        if read_count:

            average_length = round(

                total_length / read_count,

                2

            )

            average_gc = round(

                gc_total / read_count,

                2

            )

        else:

            average_length = 0

            average_gc = 0

        if quality_values:

            average_quality = round(

                total_quality /

                len(quality_values),

                2

            )

        else:

            average_quality = 0

            min_quality = 0

            max_quality = 0

        phred_encoding = "Phred+33"
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

            "Read_Count":
                read_count,

            "Total_Bases":
                total_length,

            "Min_Read_Length":
                min_length,

            "Max_Read_Length":
                max_length,

            "Average_Read_Length":
                average_length,

            "First_Read":
                first_read,

            "Average_GC_Content":
                average_gc,

            "N_Count":
                total_n,

            "Average_Quality":
                average_quality,

            "Min_Quality":
                min_quality,

            "Max_Quality":
                max_quality,

            "Phred_Encoding":
                phred_encoding,

            "SHA256":
                self.sha256(path),

            "Validation_Status":
                "VALID",

            "Parser_Name":
                "FASTQParser",

            "Parser_Version":
                "2.0"

        }

        return metadata

    def validate(self, path):

        return True

    def standardize(self, path, output_dir):

        return path

    def summarize(self, path):

        return self.extract_metadata(path)
