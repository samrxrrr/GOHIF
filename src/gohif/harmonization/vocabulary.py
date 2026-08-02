"""
GOHIF Canonical Vocabulary

Every synonym maps to one canonical representation.
"""

PROVIDER_MAP = {

    "WHO": "World Health Organization",
    "WOAH": "World Organisation for Animal Health",
    "OIE": "World Organisation for Animal Health",

    "FAO": "Food and Agriculture Organization",

    "NCBI": "National Center for Biotechnology Information",

    "GEO": "Gene Expression Omnibus",

    "ENA": "European Nucleotide Archive",

    "FDA": "U.S. Food and Drug Administration",

    "USDA": "United States Department of Agriculture",

}

DOMAIN_MAP = {

    "Human":"Human",

    "Animal":"Animal",

    "Plant":"Plant",

    "Food":"Food",

    "Environmental":"Environmental",

    "Genome":"Genome",

}

COUNTRY_MAP = {

    "USA":"United States",

    "US":"United States",

    "United States of America":"United States",

    "UK":"United Kingdom",

    "UAE":"United Arab Emirates",

}

SPECIES_MAP = {

    "human":"Homo sapiens",

    "mouse":"Mus musculus",

    "rat":"Rattus norvegicus",

    "cattle":"Bos taurus",

    "pig":"Sus scrofa",

    "chicken":"Gallus gallus",

}

def normalize(mapping, value):

    if not value:
        return value

    return mapping.get(value, value)
