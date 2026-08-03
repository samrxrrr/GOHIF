import pandas as pd

df=pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

def fam(x):

    x=str(x)

    for s in [
        "OXA",
        "CTX-M",
        "TEM",
        "SHV",
        "NDM",
        "IMP",
        "VIM",
        "KPC",
        "AAC",
        "APH",
        "ANT",
        "ERM",
        "TET",
        "QNR",
        "MCR",
        "CMY",
        "FOX"
    ]:
        if x.upper().startswith(s):
            return s

    return "OTHER"

df["Family"]=df.normalized_gene.apply(fam)

atlas=(
df.groupby("Family")
.agg(
Proteins=("Family","size"),
MeanPriority=("GOHIF_priority_score","mean"),
Structures=("pdb_count","sum")
)
.sort_values("Proteins",ascending=False)
)

atlas.to_csv(
"analysis/master/Protein_Family_Diversity.csv"
)

print(atlas)
