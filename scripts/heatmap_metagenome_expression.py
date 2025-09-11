import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import to_hex

# Load and preprocess the dataset
df = pd.read_csv("BGC_expression.csv")
df.columns = df.columns.str.strip()

# Basic checks
required_cols = {"TPM", "class", "Phylum", "Domain", "Metagenome"}
missing = required_cols - set(df.columns)
if missing:
    raise KeyError(f"Missing required column(s): {', '.join(sorted(missing))}")

# Compute log10-TPM
df["Log_TPM"] = np.log10(df["TPM"])

# Color palette for BGC classes
unique_classes = df["class"].dropna().unique()
class_palette = sns.color_palette("Set2", len(unique_classes))
class_colors = {cls: to_hex(class_palette[i]) for i, cls in enumerate(unique_classes)}

# Color mapping for Phyla (separate palettes for Bacteria / Archaea to keep contrast)
bacterial_phyla = sorted(df[df["Domain"] == "Bacteria"]["Phylum"].dropna().unique())
archaeal_phyla = sorted(df[df["Domain"] == "Archaea"]["Phylum"].dropna().unique())

bacterial_palette = sns.color_palette("hls", len(bacterial_phyla))
archaeal_palette = sns.color_palette("Pastel2", len(archaeal_phyla))

phylum_colors = {}
for i, phylum in enumerate(bacterial_phyla):
    phylum_colors[phylum] = to_hex(bacterial_palette[i])
for i, phylum in enumerate(archaeal_phyla):
    phylum_colors[phylum] = to_hex(archaeal_palette[i])

# Color mapping for Metagenomes
metagenomes = sorted(df["Metagenome"].dropna().unique())
# Use a large cyclical palette to get distinct colors for many samples
meta_palette = sns.color_palette("plasma", max(1, min(20, len(metagenomes))))
# If >20 metagenomes, fall back to 'hls' to generate enough distinct hues
if len(metagenomes) > 20:
    meta_palette = sns.color_palette("hls", len(metagenomes))
metagenome_colors = {m: to_hex(meta_palette[i % len(meta_palette)]) for i, m in enumerate(metagenomes)}

# Define order of BGC classes (optional)
class_order = ["RiPP", "Polyketide", "NRP", "Other", "Hybrid", "Terpene"]
domains = ["Bacteria", "Archaea"]

# Loop over each domain
for domain in domains:
    subset = df[df["Domain"] == domain].copy()
    if subset.empty:
        continue

    # Pivot now keeps Metagenome as an extra dimension in the columns
    # Result columns: MultiIndex (class, Metagenome)
    pivot = subset.pivot_table(
        index="Phylum",
        columns=["class", "Metagenome"],
        values="Log_TPM",
        aggfunc="mean",
        fill_value=0
    )

    if pivot.empty:
        continue

    # Sort columns: first by desired class order, then by metagenome name
    classes_in_pivot = [c for c in class_order if c in pivot.columns.get_level_values(0)]
    # Build a sorted MultiIndex based on class order then metagenome alphabetical
    sorted_cols = []
    for cls in classes_in_pivot:
        metas_here = sorted(pivot.xs(cls, axis=1, level=0).columns)
        sorted_cols.extend([(cls, m) for m in metas_here])
    # If there are classes not in class_order, append them at the end
    remaining_classes = [c for c in pivot.columns.get_level_values(0).unique() if c not in classes_in_pivot]
    for cls in sorted(remaining_classes):
        metas_here = sorted(pivot.xs(cls, axis=1, level=0).columns)
        sorted_cols.extend([(cls, m) for m in metas_here])

    pivot = pivot[sorted_cols]

    # Row colors: one color per Phylum
    row_colors = [phylum_colors.get(p, "#CCCCCC") for p in pivot.index]

    # Column color bars:
    #   1) top bar for BGC class
    #   2) second bar for Metagenome
    col_classes = [c[0] for c in pivot.columns]
    col_metas = [c[1] for c in pivot.columns]
    col_colors = pd.DataFrame({
        "BGC class": [class_colors.get(c, "#999999") for c in col_classes],
        "Metagenome": [metagenome_colors.get(m, "#CCCCCC") for m in col_metas]
    }, index=pivot.columns)

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
        figsize=(14, 9)
    )

    # Legends
    # Create & pin Phylum legend
    phylum_legend_handles = [Patch(facecolor=c, label=p) for p, c in phylum_colors.items()]
    leg_phylum = g.ax_heatmap.legend(
        handles=phylum_legend_handles,
        title="Phylum",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0.,
        fontsize=8,
        title_fontsize=9
    )
    g.ax_heatmap.add_artist(leg_phylum)  # <- keep it

    # Now add BGC class legend (won’t erase the first)
    class_legend_handles = [Patch(facecolor=c, label=k) for k, c in class_colors.items()]
    g.ax_heatmap.legend(
        handles=class_legend_handles,
        title="BGC class",
        bbox_to_anchor=(0.5, 1.18),
        loc="lower center",
        borderaxespad=0.,
        ncol=4,
        fontsize=8,
        title_fontsize=9
    )

    # Metagenome legend stays on the column dendrogram axis
    meta_legend = [Patch(facecolor=color, label=m) for m, color in metagenome_colors.items()]
    g.ax_col_dendrogram.legend(
        handles=meta_legend,
        title="Metagenome",
        bbox_to_anchor=(1.02, 0.7),
        loc="upper left",
        borderaxespad=0.,
        ncol=2 if len(metagenomes) <= 12 else 3,
        fontsize=7,
        title_fontsize=9
    )

    plt.title(f"{domain} BGC Expression by Class × Metagenome")
    plt.savefig(f"{domain}_BGC_expression_by_metagenome.svg", format="svg", bbox_inches="tight")
    plt.show()

