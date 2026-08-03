import pandas as pd

df=pd.read_csv(
"analysis/large_scale/resfinder/resfinder_sequences.csv"
)

out=pd.DataFrame({

"gene":df["gene"],

"protein":"",

"pathogen":"multiple",

"drug_class":df["drug_class"],

"resistance_mechanism":"AMR",

"sequence":df["sequence"],

"sequence_length":df["length"],

"source":"ResFinder"

})

out.to_csv(
"analysis/large_scale/resfinder/gohif_resfinder_dataset.csv",
index=False
)

print("="*80)
print("GOHIF MASTER DATASET CREATED")
print("="*80)

print(out.head(10).to_string(index=False))
