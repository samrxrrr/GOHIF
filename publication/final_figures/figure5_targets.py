import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(
"analysis/master/Top50_Therapeutic_Targets.csv"
).head(20)

plt.figure(figsize=(8,7))

plt.barh(
df["normalized_gene"],
df["GOHIF_priority_score"]
)

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
"publication/final_figures/Figure5_TopTargets.png",
dpi=600
)
