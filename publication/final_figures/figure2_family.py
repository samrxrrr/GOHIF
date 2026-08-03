import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(
"analysis/master/Protein_Family_Diversity.csv"
)

df=df.head(15)

plt.figure(figsize=(8,6))

plt.barh(df["Family"],df["Proteins"])

plt.gca().invert_yaxis()

plt.xlabel("Proteins")

plt.tight_layout()

plt.savefig(
"publication/final_figures/Figure2_ProteinFamily.png",
dpi=600
)
