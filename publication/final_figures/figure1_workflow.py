import matplotlib.pyplot as plt

steps=[
"ResFinder\n3212 genes",
"Normalization",
"UniProt",
"Structures\n(PDB+AF)",
"Prioritization",
"Network",
"Statistics",
"Therapeutic\nRanking"
]

fig,ax=plt.subplots(figsize=(15,3))

ax.set_xlim(0,len(steps))
ax.set_ylim(0,1)

for i,s in enumerate(steps):

    ax.text(i+0.5,0.5,s,
            ha="center",
            va="center",
            bbox=dict(boxstyle="round",fc="white"))

    if i<len(steps)-1:

        ax.annotate("",
                    (i+1.02,0.5),
                    (i+0.95,0.5),
                    arrowprops=dict(arrowstyle="->"))

ax.axis("off")

plt.savefig(
"publication/final_figures/Figure1_Workflow.png",
dpi=600,
bbox_inches="tight"
)
