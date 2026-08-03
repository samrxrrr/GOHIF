import pandas as pd

INPUT="analysis/large_scale/uniprot/gohif_resfinder_annotated.csv"
OUTPUT="analysis/large_scale/qc/high_confidence_amr_proteins.csv"
REPORT="analysis/large_scale/qc/amr_classifier_report.csv"

df=pd.read_csv(INPUT)

def protein_text(x):
    if pd.isna(x):
        return ""
    return str(x).lower()

df["protein_text"]=df["protein_name"].apply(protein_text)

ACCEPT=[
"beta-lactamase",
"aminoglycoside",
"acetyltransferase",
"phosphotransferase",
"nucleotidyltransferase",
"methyltransferase",
"erm",
"msr",
"vga",
"abc-f",
"ribosomal protection",
"efflux",
"mfs",
"rnd",
"smr",
"mate",
"transporter",
"tet",
"fos",
"cat",
"mph",
"qnr",
"mcr",
"ndm",
"oxa",
"kpc",
"vim",
"imp",
"ctx-m",
"tem",
"shv",
"dfr",
"dihydrofolate",
"dihydropteroate",
"penicillin-binding",
"glycopeptide",
"macrolide",
"rifampin",
"rifampicin",
"chloramphenicol",
"multidrug",
"resistance protein",
"resistance enzyme"
]

REJECT=[
"actin",
"tubulin",
"histone",
"vitellogenin",
"photosystem",
"chloroplast",
"rubisco",
"groel",
"groes",
"flagellin",
"keratin",
"hemoglobin",
"myosin"
]

def classify(text):

    if text=="":
        return "missing"

    for bad in REJECT:
        if bad in text:
            return "reject"

    for good in ACCEPT:
        if good in text:
            return "accept"

    return "review"

df["qc_status"]=df["protein_text"].apply(classify)

accepted=df[df["qc_status"]=="accept"].copy()
review=df[df["qc_status"]=="review"].copy()
rejected=df[df["qc_status"]=="reject"].copy()

accepted.to_csv(
OUTPUT,
index=False
)

report=pd.DataFrame({
"Metric":[
"Total records",
"Accepted",
"Rejected",
"Review required",
"Acceptance rate (%)"
],
"Value":[
len(df),
len(accepted),
len(rejected),
len(review),
round(len(accepted)/len(df)*100,2)
]
})

report.to_csv(
REPORT,index=False)

print("="*80)
print("GOHIF AMR CLASSIFIER V2 COMPLETE")
print("="*80)
print(report.to_string(index=False))

print("\nAccepted examples\n")
print(
accepted[
["normalized_gene","accession"]
].head(20).to_string(index=False)
)

print("\nRejected examples\n")
print(
rejected[
["normalized_gene","protein_name"]
].head(10).to_string(index=False)
)
