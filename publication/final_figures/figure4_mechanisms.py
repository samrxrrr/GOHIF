import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(
"analysis/master/Resistance_Mechanism_Landscape.csv"
)

plt.figure(figsize=(8,5))

plt.bar(
df["Resistance_mechanism"],
df["Proteins"]
)

plt.xticks(rotation=45,ha="right")

plt.tight_layout()

plt.savefig(
"publication/final_figures/Figure4_Mechanisms.png",
dpi=600
)
