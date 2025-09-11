import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import to_hex

# Load and preprocess the dataset

df = pd.read_csv("BGC_expression.csv")
df.columns = df.columns.str.strip()

# Check and compute log10-TPM 

if "TPM" not in df.columns:
    raise KeyError("TPM column not found in dataset.")

df["Log_TPM"] = np.log10(df["TPM"])

# Define color palettes for BGC classes

product_palette_map = {
    "RiPP": sns.color_palette("Blues", 8),
    "Polyketide": sns.color_palette("Oranges", 8),
    "NRP": sns.color_palette("Greens", 8),
    "Other": sns.color_palette("Reds", 8),
    "Terpene": sns.color_palette("grey", 8),
    "Hybrid": sns.color_palette("Purples", 8),
}

product_class_colors = {}
product_class_map = {}
class_index = {k: 0 for k in product_palette_map.keys()}

for _, row in df.iterrows():
    product = row["Predicted product"]
    bgc_class = row["class"]
    product_class_map[product] = bgc_class
    if product not in product_class_colors:
        palette = product_palette_map.get(bgc_class, sns.color_palette("hsv", 8))
        product_class_colors[product] = to_hex(palette[class_index[bgc_class] % len(palette)])
        class_index[bgc_class] += 1

# Color mapping for phyla

# Sort phyla alphabetically
bacterial_phyla = sorted(df[df["Domain"] == "Bacteria"]["Phylum"].dropna().unique())
archaeal_phyla = sorted(df[df["Domain"] == "Archaea"]["Phylum"].dropna().unique())

# Generate enough colors for all phyla dynamically
bacterial_palette = sns.color_palette("hls", len(bacterial_phyla))
archaeal_palette = sns.color_palette("Pastel2", len(archaeal_phyla))

# Assign colors to phyla
phylum_colors = {}
for i, phylum in enumerate(bacterial_phyla):
    phylum_colors[phylum] = to_hex(bacterial_palette[i])
for i, phylum in enumerate(archaeal_phyla):
    phylum_colors[phylum] = to_hex(archaeal_palette[i])

# Define order of BGC classes for consistent column sorting

class_order = ["RiPP", "Polyketide", "NRP", "Other", "Hybrid", "Terpene"]
domains = ["Bacteria", "Archaea"]

# Loop over each domain

for domain in domains:
    subset = df[df["Domain"] == domain]

    # Create pivot table: average Log_TPM for each phylum × predicted product
    pivot = subset.pivot_table(
        index="Phylum",
        columns="Predicted product",
        values="Log_TPM",
        aggfunc="mean",
        fill_value=0
    )

    if pivot.empty:
        continue
    # Sort columns (predicted products) by predefined BGC class order
    sorted_columns = []
    for cls in class_order:
        cls_products = [col for col in pivot.columns if product_class_map.get(col) == cls]
        sorted_columns.extend(sorted(cls_products))
    pivot = pivot[sorted_columns]

    # Prepare colors for rows and columns
    row_colors = [phylum_colors.get(p, "#CCCCCC") for p in pivot.index]
    col_colors = [product_class_colors.get(p, "#999999") for p in pivot.columns]
    
    # Plot heatmap
    sns.set(style="white")
    g = sns.clustermap(
        pivot,
        row_cluster=False,
        col_cluster=False,
        row_colors=row_colors,
        col_colors=col_colors,
        cmap="viridis",
        xticklabels=False,
        yticklabels=False,
        figsize=(12, 8),
        dendrogram_ratio=(.1, .2),
        colors_ratio=(0.05, 0.05),
        cbar_kws={'label': 'lg(TPM)'},
        cbar_pos=(-2, 0.3, 0.02, 0.4)
    )
    
    # Adjust figure layout
    g.fig.subplots_adjust(left=0.4, right=0.85, top=0.9, bottom=0.1)

    # Create legend for phylum colors
    phylum_legend = [Patch(facecolor=phylum_colors[p], label=p) for p in pivot.index if p in phylum_colors]

    # Create grouped legend for predicted products
    grouped_legend = []
    for class_group in class_order:
        handles = [
            Patch(facecolor=product_class_colors[product], label=product)
            for product in pivot.columns
            if product_class_map.get(product) == class_group
        ]
        grouped_legend.extend(handles)

    # Add legends to the figure 
    g.ax_heatmap.legend(
        handles=phylum_legend,
        title="Phyla",
        bbox_to_anchor=(1.1, 1),
        loc="upper left",
        borderaxespad=0.
    )

    g.ax_col_dendrogram.legend(
        handles=grouped_legend,
        title="BGC Products",
        bbox_to_anchor=(0.5, 1.25),
        loc="lower center",
        borderaxespad=0.,
        ncol=3
    )
    
    # Save the figures
    filename = f"bgc_expression_heatmap_{domain.lower()}.svg"
    g.savefig(filename, format='svg', bbox_inches='tight', pad_inches=0.4)
    plt.close(g.fig)
    print(f"Saved: {filename}")
