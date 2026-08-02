from pathlib import Path
import json
import re

INPUT = Path("/mnt/g/My Drive/DATASETS/_metadata_standardized")

PROVIDER_RULES = {
    "WHO": ["who","wahis"],
    "FAO": ["fao","faostat","agrovoc"],
    "NCBI": ["ncbi","sra","srr","gca","gcf","genbank"],
    "GEO": ["geo","gse","gsm"],
    "ENA": ["ena","ebi"],
    "FDA": ["fdc"],
    "USDA": ["usda"],
}

KEYWORD_RULES = {
    "amr":["amr","antimicrobial","antibiotic","resistance"],
    "genome":["genome","genomic"],
    "microbiome":["microbiome","microbial"],
    "food":["food","fdc","foodex"],
    "livestock":["livestock","cattle","animal"],
    "plant":["plant","crop"],
    "virus":["virus","viral"],
    "bacteria":["bacteria","bacterial"],
}

OMICS_RULES = {
    "Genomics":["genome","assembly","gca","gcf"],
    "Transcriptomics":["rna","rnaseq","transcript","gse","gsm"],
    "Proteomics":["protein","proteome"],
    "Metabolomics":["metabol"],
    "Microbiome":["microbiome","16s"],
}

def infer_provider(name):

    n = name.lower()

    for provider, patterns in PROVIDER_RULES.items():

        if any(p in n for p in patterns):
            return provider

    return ""


def infer_keywords(name):

    n = name.lower()

    found = set()

    for keyword, patterns in KEYWORD_RULES.items():

        if any(p in n for p in patterns):
            found.add(keyword)

    return sorted(found)


def infer_omics(name):

    n = name.lower()

    found = []

    for omics, patterns in OMICS_RULES.items():

        if any(p in n for p in patterns):
            found.append(omics)

    return found


def infer_year(name):

    m = re.search(r"(19|20)\d{2}", name)

    if m:
        return int(m.group())

    return 0


count = 0

for file in sorted(INPUT.glob("GOHIF_DS_*.json")):

    with open(file, encoding="utf-8") as f:
        obj = json.load(f)

    name = obj["dataset_name"]

    obj["provider"] = infer_provider(name)

    obj["source"] = obj["provider"]

    obj["keywords"] = infer_keywords(name)

    obj["omics_type"] = infer_omics(name)

    obj["publication_year"] = infer_year(name)

    suffix = Path(name).suffix.lower()

    if suffix:
        obj["file_formats"] = [suffix.replace(".", "")]

    with open(file, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

    count += 1

print("=" * 70)
print("GOHIF Metadata Enrichment Complete")
print("=" * 70)
print("Datasets enriched:", count)
print("=" * 70)
