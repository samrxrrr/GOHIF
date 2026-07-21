"""
GOHIF Quality Utilities

Reusable sequencing-quality functions for FASTQ and related
biological sequence formats.
"""

from statistics import mean


def phred_scores(quality_string, offset=33):
    """
    Convert an ASCII FASTQ quality string into numeric Phred scores.

    Parameters
    ----------
    quality_string : str
        FASTQ ASCII quality string.

    offset : int
        ASCII offset. Standard modern FASTQ uses Phred+33.

    Returns
    -------
    list[int]
    """

    if not quality_string:
        return []

    return [
        ord(character) - offset
        for character in quality_string
    ]


def detect_phred_encoding(quality_string):
    """
    Infer likely FASTQ Phred encoding from observed ASCII characters.

    Returns
    -------
    str
        PHRED+33
        PHRED+64_POSSIBLE
        UNKNOWN
    """

    if not quality_string:
        return "UNKNOWN"

    ascii_values = [
        ord(character)
        for character in quality_string
    ]

    minimum_ascii = min(ascii_values)

    if minimum_ascii < 64:
        return "PHRED+33"

    return "PHRED+64_POSSIBLE"


def quality_summary(scores):
    """
    Calculate basic quality statistics from numeric Phred scores.
    """

    if not scores:

        return {
            "Quality_Count": 0,
            "Min_Quality": 0,
            "Max_Quality": 0,
            "Average_Quality": 0
        }

    return {
        "Quality_Count":
            len(scores),

        "Min_Quality":
            min(scores),

        "Max_Quality":
            max(scores),

        "Average_Quality":
            round(mean(scores), 2)
    }


def count_bases_at_or_above_quality(scores, threshold):
    """
    Count bases with Phred quality >= threshold.
    """

    return sum(
        score >= threshold
        for score in scores
    )


def quality_percentage(scores, threshold):
    """
    Percentage of bases with Phred quality >= threshold.
    """

    if not scores:
        return 0.0

    count = count_bases_at_or_above_quality(
        scores,
        threshold
    )

    return round(
        count * 100 / len(scores),
        2
    )


def q20_percentage(scores):
    """
    Percentage of bases with Phred score >= Q20.
    """

    return quality_percentage(
        scores,
        20
    )


def q30_percentage(scores):
    """
    Percentage of bases with Phred score >= Q30.
    """

    return quality_percentage(
        scores,
        30
    )


def error_probability(phred_score):
    """
    Convert a Phred score into estimated base-call error probability.

    Formula:
        P(error) = 10 ^ (-Q / 10)
    """

    try:

        score = float(phred_score)

    except (TypeError, ValueError):

        return None

    return 10 ** (
        -score / 10
    )


def mean_error_probability(scores):
    """
    Calculate mean estimated error probability across Phred scores.
    """

    if not scores:
        return 0.0

    probabilities = [
        error_probability(score)
        for score in scores
    ]

    return round(
        sum(probabilities) /
        len(probabilities),
        8
    )


def validate_quality_length(sequence, quality_string):
    """
    Validate that sequence and quality strings have equal length.
    """

    return (
        len(sequence) ==
        len(quality_string)
    )


def fastq_quality_metrics(quality_string, offset=33):
    """
    Generate reusable quality metadata for one FASTQ quality string.
    """

    scores = phred_scores(
        quality_string,
        offset=offset
    )

    summary = quality_summary(scores)

    summary.update({

        "Q20_Percent":
            q20_percentage(scores),

        "Q30_Percent":
            q30_percentage(scores),

        "Mean_Error_Probability":
            mean_error_probability(scores),

        "Phred_Encoding":
            detect_phred_encoding(
                quality_string
            )

    })

    return summary
