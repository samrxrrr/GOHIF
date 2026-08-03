import pandas as pd

df=pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

print("="*80)
print("GOHIF DATASET STATISTICS")
print("="*80)

print()

print(df.describe())

print()

print("Unique proteins :",len(df))

print("Drug classes :",df.drug_class.nunique())

print("Mechanisms :",df.Resistance_mechanism.nunique())

print("Experimental :",sum(df.structure_status=="Experimental (PDB)"))

print("AlphaFold :",sum(df.structure_status=="AlphaFold Candidate"))

print()

print(df.groupby("drug_class").size())

print()

print(df.groupby("Resistance_mechanism").size())
