from pathlib import Path
import pandas as pd

ROOT = Path("datasets/global_amr/ResFinder/raw/resfinder_db")

records = []

for fasta in ROOT.glob("*.fsa"):

    # Skip duplicated master FASTA
    if fasta.name == "all.fsa":
        continue

    drug_class = fasta.stem

    gene = None
    seq = []

    with open(fasta) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):

                if gene is not None:

                    sequence = "".join(seq)

                    records.append({
                        "gene": gene,
                        "protein": "",
                        "pathogen": "multiple",
                        "drug_class": drug_class,
                        "resistance_mechanism": "AMR",
                        "sequence": sequence,
                        "sequence_length": len(sequence),
                        "source": "ResFinder"
                    })

                gene = line[1:].split()[0]
                seq = []

            else:

                seq.append(line)

    if gene is not None:

        sequence = "".join(seq)

        records.append({
            "gene": gene,
            "protein": "",
            "pathogen": "multiple",
            "drug_class": drug_class,
            "resistance_mechanism": "AMR",
            "sequence": sequence,
            "sequence_length": len(sequence),
            "source": "ResFinder"
        })

df = pd.DataFrame(records)

df = df.drop_duplicates(subset=["gene"])

df = df.sort_values(
    ["drug_class", "gene"]
).reset_index(drop=True)

df.to_csv(
    "analysis/large_scale/resfinder/gohif_resfinder_dataset.csv",
    index=False
)

print("=" * 80)
print("GOHIF RESFINDER PARSER v2 COMPLETE")
print("=" * 80)
print()

print("Unique genes:", len(df))
print("Drug classes:", df["drug_class"].nunique())
print("Shortest sequence:", df["sequence_length"].min())
print("Longest sequence:", df["sequence_length"].max())

print()
print(df.groupby("drug_class").size().sort_values(ascending=False))

print()
print(df.head(20).to_string(index=False))
