import pandas as pd
import matplotlib.pyplot as plt

# Load data 
summary_df = pd.read_csv("MAG_phylum.csv")  
bgc_df = pd.read_csv("BGC_class.csv")        

# Merge tables on MAG/genome_ID
merged_df = bgc_df.merge(summary_df, left_on="MAG", right_on="genome_ID")

# Count BGC classes per Phylum 
class_counts = (
    merged_df.groupby(['Domain_x', 'Phylum_x', 'class'])
    .size()
    .reset_index(name='BGC_count')
    .rename(columns={'Domain_x': 'Domain', 'Phylum_x': 'Phylum'})
)

# Count MAGs per Phylum
mag_counts = summary_df.groupby(['Domain', 'Phylum'])['genome_ID'].nunique().reset_index(name='MAG_count')

# Merge and normalize
normalized_df = class_counts.merge(mag_counts, on=['Domain', 'Phylum'])
normalized_df['normalized_count'] = normalized_df['BGC_count'] / normalized_df['MAG_count']

# Get all BGC classes
all_classes = sorted(normalized_df['class'].unique())

# Create a dictionary of MAG counts per phylum
phylum_mag_counts = summary_df.groupby('Phylum')['genome_ID'].nunique().to_dict()

# Plot function
def plot_stacked_bar(df, title, filename, all_classes, mag_count_dict):
    pivot_df = df.pivot_table(index='Phylum', columns='class', values='normalized_count', fill_value=0)

    # Add missing BGC classes
    for cls in all_classes:
        if cls not in pivot_df.columns:
            pivot_df[cls] = 0
    pivot_df = pivot_df[all_classes]  # enforce class order

    # Sort phyla by total normalized BGC count
    pivot_df['Total'] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values(by='Total', ascending=False)
    pivot_df = pivot_df.drop(columns='Total')

    # Plot
    ax = pivot_df.plot(kind='bar', stacked=True, figsize=(12, 6), legend=True)
    plt.ylabel('Normalized BGC Count')
    plt.title(title)
    plt.tight_layout()

    # Bold labels for phyla with only one MAG
    labels = ax.get_xticklabels()
    for label in labels:
        phylum = label.get_text()
        if mag_count_dict.get(phylum, 0) == 1:
            label.set_fontweight('bold')
    ax.set_xticklabels(labels, rotation=45, ha='right')

    # Add legend
    plt.legend(
        title='BGC Class',
        loc='upper right',
        bbox_to_anchor=(1, 1),
        borderaxespad=0.,
        frameon=True,
        fontsize='small',
        title_fontsize='medium'
    )

    # Save as SVG
    plt.savefig(filename, format='svg')
    plt.close()

# Split and plot for Bacteria and Archaea
bacteria_df = normalized_df[normalized_df['Domain'] == 'Bacteria']
archaea_df = normalized_df[normalized_df['Domain'] == 'Archaea']

plot_stacked_bar(bacteria_df, "Bacteria",
                 "bacteria_bgc_normalized.svg", all_classes, phylum_mag_counts)

plot_stacked_bar(archaea_df, "Archaea",
                 "archaea_bgc_normalized.svg", all_classes, phylum_mag_counts)

