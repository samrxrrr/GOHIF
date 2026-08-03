import pandas as pd
import re

INPUT="analysis/large_scale/uniprot/gohif_resfinder_annotated.csv"
OUTPUT="analysis/large_scale/qc/high_confidence_annotations.csv"
REPORT="analysis/large_scale/qc/annotation_qc_report.csv"

df=pd.read_csv(INPUT)

def extract_name(x):
    if pd.isna(x):
        return ""
    return str(x).lower()

df["protein_text"]=df["protein_name"].apply(extract_name)
df["gene_text"]=df["normalized_gene"].astype(str).str.lower()

GOOD_PATTERNS=[
"beta-lactamase",
"aminoglycoside",
"acetyltransferase",
"phosphoethanolamine",
"efflux",
"tet",
"fos",
"erm",
"mph",
"cat",
"qnr",
"dhps",
"dihydropteroate",
"dihydrofolate",
"rifampin",
"rifampicin",
"transferase",
"methyltransferase",
"oxidoreductase"
]

BAD_PATTERNS=[
"groel",
"groes",
"chaperonin",
"vitellogenin",
"ribosomal",
"histone",
"actin",
"tubulin",
"photosystem",
"flagellin"
]

def classify(row):

    text=row["protein_text"]

    if text=="":
        return "missing"

    for b in BAD_PATTERNS:
        if b in text:
            return "reject"

    for g in GOOD_PATTERNS:
        if g in text:
            return "accept"

    return "review"

df["qc_status"]=df.apply(classify,axis=1)

accepted=df[df["qc_status"]=="accept"].copy()

accepted.to_csv(
OUTPUT,
index=False
)

report=pd.DataFrame({

"Metric":[
"Total annotated",
"Accepted",
"Rejected",
"Manual review"
],

"Value":[
len(df),
(df["qc_status"]=="accept").sum(),
(df["qc_status"]=="reject").sum(),
(df["qc_status"]=="review").sum()
]

})

report.to_csv(
REPORT,
index=False
)

print("="*80)
print("GOHIF ANNOTATION QC COMPLETE")
print("="*80)

print(report.to_string(index=False))

print()

print("="*80)
print("Rejected Examples")
print("="*80)

print(
df[
df["qc_status"]=="reject"
][[
"normalized_gene",
"protein_name"
]].head(20).to_string(index=False)
)
