import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load CSV
df = pd.read_csv("expressed_AMP.csv")

# Clean column name for consistency
df.columns = df.columns.str.strip()

# Group by Domain, Phylum, and Metagenome to compute mean log(TPM)
grouped = df.groupby(["Domain", "Phylum", "Metagenome"])["log (TPM)"].mean().reset_index()

# Pivot: rows = (Domain, Phylum), columns = Metagenome
heatmap_data = grouped.pivot_table(index=["Domain", "Phylum"], columns="Metagenome", values="log (TPM)", fill_value=0)

# Sort rows
heatmap_data = heatmap_data.sort_index()

# Color by domain
domain_colors = {"Bacteria": "#008b8b", "Archaea": "#702963"}
row_colors = pd.Series([domain_colors[dom] for dom, phy in heatmap_data.index], index=heatmap_data.index)

# Y-axis labels = Phylum only
ytick_labels = [phy for dom, phy in heatmap_data.index]

# Plot using clustermap
g = sns.clustermap(
    heatmap_data,
    cmap="YlGnBu",
    annot=True,
    fmt=".2f",
    row_colors=row_colors,
    col_cluster=False,
    row_cluster=False,
    linewidths=0.5,
    yticklabels=ytick_labels,
    figsize=(20, 15)
)

# Legend for domain
handles = [
    Patch(facecolor=domain_colors["Bacteria"], edgecolor='k', label="Bacteria"),
    Patch(facecolor=domain_colors["Archaea"], edgecolor='k', label="Archaea")
]
g.ax_row_dendrogram.legend(
    handles=handles,
    title="Domain",
    loc='center right',
    bbox_to_anchor=(1, 0.8)
)

g.cax.set_title("log(TPM)", fontsize=12)

# Axis labels and title
g.ax_heatmap.set_title("Mean Expression (log TPM) of Expressed AMPs by Phylum")
g.ax_heatmap.set_xlabel("Metagenome")
g.ax_heatmap.set_ylabel("Phylum")

# Save as SVG
plt.savefig("expressed_AMP_logTPM_heatmap.svg", format="svg", bbox_inches='tight')

# Show plot
plt.show()

