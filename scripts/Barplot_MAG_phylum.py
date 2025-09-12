import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data

df = pd.read_csv("MAG_phylum.csv", sep=",")

# Count MAGs per Metagenome & Phylum

counts = df.groupby(["Domain", "Metagenome", "Phylum"]).size().reset_index(name="Count")

# Prepare data for plotting

bacteria_df = counts[counts["Domain"] == "Bacteria"]
archaea_df = counts[counts["Domain"] == "Archaea"]

# Pivot tables for stacked bar plotting
bacteria_pivot = bacteria_df.pivot(index="Metagenome", columns="Phylum", values="Count").fillna(0)
archaea_pivot = archaea_df.pivot(index="Metagenome", columns="Phylum", values="Count").fillna(0)

# Plot function

def plot_stacked_bar(data, title, palette, output_file):
    fig, ax = plt.subplots(figsize=(12, 7)) 
    data.plot(kind="bar", stacked=True, ax=ax, color=palette)

    ax.set_title(title, fontsize=16)
    ax.set_ylabel("MAG count", fontsize=12)
    ax.set_xlabel("Metagenome", fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    ax.legend(title="Phylum", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_file, format="svg", bbox_inches='tight')  # ensures legend isn't cut
    plt.close()

# Define color palettes

bacteria_palette = (sns.color_palette("tab20b", 20) + sns.color_palette("tab20c", 20) + sns.color_palette("Pastel1", 9))[:len(bacteria_pivot.columns)]
archaea_palette = sns.color_palette("Paired", n_colors=len(archaea_pivot.columns))

# Plot data

if not bacteria_pivot.empty:
    plot_stacked_bar(bacteria_pivot, "Bacteria Phylum Distribution", bacteria_palette, "bacteria_stacked_bar.svg")

if not archaea_pivot.empty:
    plot_stacked_bar(archaea_pivot, "Archaea Phylum Distribution", archaea_palette, "archaea_stacked_bar.svg")

print("SVG plots saved")

