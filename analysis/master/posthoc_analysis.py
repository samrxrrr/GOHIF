import pandas as pd
from scipy.stats import mannwhitneyu
from itertools import combinations

df = pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

results=[]

groups=df.groupby("drug_class")

for (a,ga),(b,gb) in combinations(groups,2):

    u,p=mannwhitneyu(
        ga["GOHIF_priority_score"],
        gb["GOHIF_priority_score"],
        alternative="two-sided"
    )

    results.append([a,b,u,p])

out=pd.DataFrame(
    results,
    columns=[
        "DrugClass1",
        "DrugClass2",
        "U",
        "Pvalue"
    ]
)

out["AdjustedP"]=out["Pvalue"]*len(out)
out["AdjustedP"]=out["AdjustedP"].clip(upper=1)

out.to_csv(
"analysis/master/PostHoc_DrugClass.csv",
index=False
)

print("="*80)
print("POST-HOC DRUG CLASS COMPARISON")
print("="*80)
print(out.sort_values("AdjustedP").head(20))
