"""
GOHIF Statistical Utilities

Reusable statistical functions for biological datasets.

These functions are shared across all parsers and analytical
modules to ensure consistent statistical calculations.
"""

from statistics import mean, median, stdev


def summary_statistics(values):
    """
    Compute summary statistics for a list of numeric values.

    Parameters
    ----------
    values : list[int | float]

    Returns
    -------
    dict
    """

    if not values:

        return {
            "Count": 0,
            "Minimum": 0,
            "Maximum": 0,
            "Mean": 0,
            "Median": 0,
            "Standard_Deviation": 0
        }

    result = {

        "Count": len(values),

        "Minimum": min(values),

        "Maximum": max(values),

        "Mean": round(
            mean(values),
            2
        ),

        "Median": round(
            median(values),
            2
        ),

        "Standard_Deviation": (
            round(stdev(values), 2)
            if len(values) > 1
            else 0
        )

    }

    return result


def n50(lengths):
    """
    Compute N50 statistic.

    Parameters
    ----------
    lengths : list[int]

    Returns
    -------
    int
    """

    if not lengths:
        return 0

    lengths = sorted(
        lengths,
        reverse=True
    )

    total = sum(lengths)

    threshold = total / 2

    cumulative = 0

    for length in lengths:

        cumulative += length

        if cumulative >= threshold:
            return length

    return 0


def n90(lengths):
    """
    Compute N90 statistic.
    """

    if not lengths:
        return 0

    lengths = sorted(
        lengths,
        reverse=True
    )

    total = sum(lengths)

    threshold = total * 0.90

    cumulative = 0

    for length in lengths:

        cumulative += length

        if cumulative >= threshold:
            return length

    return 0


def coefficient_of_variation(values):
    """
    Calculate coefficient of variation (%).
    """

    if len(values) < 2:
        return 0

    m = mean(values)

    if m == 0:
        return 0

    return round(
        (stdev(values) / m) * 100,
        2
    )
