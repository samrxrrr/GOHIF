from pathlib import Path
import pandas as pd

ROOT=Path("datasets/amr_large")

OUTPUT=[]

def read_table(f):

    if f.suffix.lower()==".csv":
        return pd.read_csv(f)

    if f.suffix.lower() in [".tsv",".txt"]:
        return pd.read_csv(f,sep="\t")

    return None

for database in ROOT.iterdir():

    if not database.is_dir():
        continue

    for f in database.glob("*"):

        df=read_table(f)

        if df is None:
            continue

        df.columns=[str(c).strip() for c in df.columns]

        lower={c.lower():c for c in df.columns}

        def pick(names):

            for n in names:

                if n.lower() in lower:
                    return df[lower[n.lower()]]

            return ""

        out=pd.DataFrame({

            "database":database.name,

            "gene":pick([
                "gene",
                "amr_gene",
                "gene_symbol",
                "gene_name"
            ]),

            "protein":pick([
                "protein",
                "protein_name"
            ]),

            "pathogen":pick([
                "pathogen",
                "organism",
                "species"
            ]),

            "drug_class":pick([
                "drug_class",
                "drug",
                "antibiotic_class"
            ]),

            "resistance_mechanism":pick([
                "mechanism",
                "resistance_mechanism"
            ])

        })

        OUTPUT.append(out)

if OUTPUT:

    master=pd.concat(
        OUTPUT,
        ignore_index=True
    )

else:

    master=pd.DataFrame(columns=[
        "database",
        "gene",
        "protein",
        "pathogen",
        "drug_class",
        "resistance_mechanism"
    ])

master.to_csv(
"analysis/large_scale/results/master_amr_dataset.csv",
index=False
)

print("="*80)
print("GOHIF UNIVERSAL IMPORT COMPLETE")
print("="*80)
print(master.head(20).to_string(index=False))
print()
print("TOTAL RECORDS:",len(master))
