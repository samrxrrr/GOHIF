import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(
"analysis/final_dataset/structure_coverage_summary.csv"
)

plt.figure(figsize=(5,5))

plt.pie(
df["Proteins"],
labels=df["structure_status"],
autopct="%1.1f%%"
)

plt.savefig(
"publication/final_figures/Figure3_StructureCoverage.png",
dpi=600
)
