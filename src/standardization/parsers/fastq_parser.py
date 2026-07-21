"""
GOHIF FASTQ Parser
Scientific Metadata Enrichment
Modular Refactor Version 3.0
"""

from pathlib import Path

from src.standardization.base_parser import BaseParser

from src.standardization.common.metadata_builder import build_metadata

from src.standardization.common.sequence_utils import (
    gc_content,
)

from src.standardization.common.statistics import (
    summary_statistics,
    coefficient_of_variation,
)

from src.standardization.common.quality_utils import (
    phred_scores,
    error_probability,
)

from src.standardization.common.validators import (
    validate_fastq_structure,
    validation_status,
)


class FASTQParser(BaseParser):

    PARSER_NAME = "FASTQParser"
    PARSER_VERSION = "3.0"

    SUPPORTED_EXTENSIONS = {
        ".fastq",
        ".fq",
    }

    def detect(self, path):

        return (
            Path(path).suffix.lower()
            in self.SUPPORTED_EXTENSIONS
        )

    def read_fastq(self, path):
        """
        Streaming FASTQ reader.

        Yields
        ------
        tuple
            (header, sequence, quality)
        """

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as handle:

            while True:

                header = handle.readline()

                if not header:
                    break

                sequence = handle.readline()
                plus = handle.readline()
                quality = handle.readline()

                if (
                    not sequence
                    or not plus
                    or not quality
                ):
                    break

                header = header.rstrip("\r\n")
                sequence = sequence.rstrip("\r\n")
                plus = plus.rstrip("\r\n")
                quality = quality.rstrip("\r\n")

                if not header.startswith("@"):
                    continue

                if not plus.startswith("+"):
                    continue

                yield (
                    header[1:].strip(),
                    sequence.strip(),
                    quality.strip(),
                )

    def extract_metadata(self, path):

        path = Path(path)

        read_count = 0
        total_length = 0
        total_n = 0

        first_read = None

        read_lengths = []

        gc_values = []

        quality_count = 0
        quality_sum = 0
        quality_min = None
        quality_max = None

        q20_count = 0
        q30_count = 0

        error_probability_sum = 0.0

        quality_length_mismatches = 0

        observed_ascii_min = None

        for (
            header,
            sequence,
            quality,
        ) in self.read_fastq(path):

            sequence = sequence.upper()

            length = len(sequence)

            read_count += 1
            total_length += length

            read_lengths.append(length)

            if first_read is None:
                first_read = header

            gc_values.append(
                gc_content(sequence)
            )

            total_n += sequence.count("N")

            if len(sequence) != len(quality):

                quality_length_mismatches += 1

            if quality:

                local_ascii_min = min(
                    ord(character)
                    for character in quality
                )

                if (
                    observed_ascii_min is None
                    or local_ascii_min
                    < observed_ascii_min
                ):

                    observed_ascii_min = (
                        local_ascii_min
                    )

            scores = phred_scores(
                quality,
                offset=33,
            )

            if scores:

                quality_count += len(scores)

                quality_sum += sum(scores)

                local_min = min(scores)
                local_max = max(scores)

                if (
                    quality_min is None
                    or local_min < quality_min
                ):

                    quality_min = local_min

                if (
                    quality_max is None
                    or local_max > quality_max
                ):

                    quality_max = local_max

                q20_count += sum(
                    score >= 20
                    for score in scores
                )

                q30_count += sum(
                    score >= 30
                    for score in scores
                )

                error_probability_sum += sum(
                    error_probability(score)
                    for score in scores
                )

        length_stats = summary_statistics(
            read_lengths
        )

        if gc_values:

            average_gc = round(
                sum(gc_values)
                / len(gc_values),
                2,
            )

        else:

            average_gc = 0

        if quality_count:

            average_quality = round(
                quality_sum
                / quality_count,
                2,
            )

            q20_percent = round(
                q20_count
                * 100
                / quality_count,
                2,
            )

            q30_percent = round(
                q30_count
                * 100
                / quality_count,
                2,
            )

            mean_error_probability = round(
                error_probability_sum
                / quality_count,
                8,
            )

        else:

            average_quality = 0
            quality_min = 0
            quality_max = 0

            q20_percent = 0.0
            q30_percent = 0.0

            mean_error_probability = 0.0

        if observed_ascii_min is None:

            phred_encoding = "UNKNOWN"

        elif observed_ascii_min < 64:

            phred_encoding = "Phred+33"

        else:

            phred_encoding = (
                "Phred+64_POSSIBLE"
            )

        scientific_metadata = {

            "Read_Count":
                read_count,

            "Total_Bases":
                total_length,

            "Min_Read_Length":
                length_stats["Minimum"],

            "Max_Read_Length":
                length_stats["Maximum"],

            "Average_Read_Length":
                length_stats["Mean"],

            "Median_Read_Length":
                length_stats["Median"],

            "Read_Length_Standard_Deviation":
                length_stats[
                    "Standard_Deviation"
                ],

            "Read_Length_CV_Percent":
                coefficient_of_variation(
                    read_lengths
                ),

            "First_Read":
                first_read,

            "Average_GC_Content":
                average_gc,

            "N_Count":
                total_n,

            "Quality_Base_Count":
                quality_count,

            "Average_Quality":
                average_quality,

            "Min_Quality":
                quality_min,

            "Max_Quality":
                quality_max,

            "Q20_Count":
                q20_count,

            "Q20_Percent":
                q20_percent,

            "Q30_Count":
                q30_count,

            "Q30_Percent":
                q30_percent,

            "Mean_Error_Probability":
                mean_error_probability,

            "Quality_Length_Mismatches":
                quality_length_mismatches,

            "Phred_Encoding":
                phred_encoding,
        }

        valid = validate_fastq_structure(
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

        return validate_fastq_structure(
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
