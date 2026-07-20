"""
GOHIF Sequence Utilities

Reusable biological sequence functions.
"""

from collections import Counter


DNA_ALPHABET = set("ACGTN")

RNA_ALPHABET = set("ACGUN")

PROTEIN_ALPHABET = set(
    "ABCDEFGHIKLMNPQRSTVWXYZ*"
)


def infer_molecule_type(sequence):
    """
    Infer whether a sequence is DNA, RNA or Protein.
    """

    seq = sequence.upper()

    chars = set(seq)

    if chars <= DNA_ALPHABET:
        return "DNA"

    if chars <= RNA_ALPHABET:
        return "RNA"

    return "PROTEIN"


def gc_content(sequence):
    """
    Calculate GC percentage.
    """

    seq = sequence.upper()

    if len(seq) == 0:
        return 0.0

    gc = seq.count("G") + seq.count("C")

    return round(
        gc * 100 / len(seq),
        2
    )


def base_counts(sequence):
    """
    Count nucleotide frequencies.
    """

    seq = sequence.upper()

    return {

        "A": seq.count("A"),

        "C": seq.count("C"),

        "G": seq.count("G"),

        "T": seq.count("T"),

        "U": seq.count("U"),

        "N": seq.count("N")

    }


def sequence_length(sequence):

    return len(sequence)


def composition(sequence):
    """
    Return residue composition.
    """

    seq = sequence.upper()

    return dict(
        Counter(seq)
    )


def ambiguous_count(sequence):
    """
    Count ambiguous symbols.

    DNA/RNA -> N

    Protein -> X
    """

    seq = sequence.upper()

    molecule = infer_molecule_type(seq)

    if molecule == "PROTEIN":

        return seq.count("X")

    return seq.count("N")
