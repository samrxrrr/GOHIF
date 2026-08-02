import pandas as pd
import re


input_file="analysis/structure_discovery/docking/results/vina_execution_results.csv"

output_file="analysis/structure_discovery/docking/results/vina_scores.csv"


df=pd.read_csv(input_file)


scores=[]


for _,row in df.iterrows():

    text=row["result"]

    match=re.search(
        r"REMARK VINA RESULT:\s+(-?\d+\.\d+)",
        text
    )

    score=float(match.group(1)) if match else None


    scores.append({

        "target_id":row["target_id"],
        "ligand_id":row["ligand_id"],
        "compound":row["compound"],
        "binding_affinity_kcal_mol":score,
        "status":row["status"]

    })


out=pd.DataFrame(scores)


out=out.sort_values(
    "binding_affinity_kcal_mol"
)


out.to_csv(
    output_file,
    index=False
)


print("="*80)
print("GOHIF VINA SCORE EXTRACTION COMPLETE")
print("="*80)

print(out.to_string(index=False))

