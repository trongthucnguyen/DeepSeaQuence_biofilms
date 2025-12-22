import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load data
sim_matrix = pd.read_csv('similarity_matrix.tsv', sep='\t', index_col=0)
meta = pd.read_csv('peptide_test.txt', sep='\t')

# Normalize similarity matrix
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
sim_matrix_scaled = scaler.fit_transform(sim_matrix.values)

# UMAP embedding
umap_model = umap.UMAP(
    random_state=42,
    n_neighbors=20,
    min_dist=0.1,
    spread=10.0,
    metric='precomputed'
)
embedding = umap_model.fit_transform(sim_matrix_scaled)

# Merge UMAP coords with meta
meta['UMAP1'] = embedding[:, 0]
meta['UMAP2'] = embedding[:, 1]

# Plot
plt.figure(figsize=(15, 15))

palette = {label: plt.colormaps['tab20'](i / len(meta['label'].unique()))
           for i, label in enumerate(meta['label'].unique())}

labels_with_contours = ['inMAGs', 'APD3']
for label in labels_with_contours:
    subset = meta[meta['label'] == label]
    if not subset.empty:
        sns.kdeplot(
            x=subset['UMAP1'], y=subset['UMAP2'],
            fill=True, color=palette[label], alpha=0.3, levels=20,
	    bw_adjust=0.3	
        )

for label in meta['label'].unique():
    subset = meta[meta['label'] == label]
    
    # Assign marker styles
    if label == 'APD3':
        marker = 'd'      # Diamond
        size = 30         # Smaller
    elif label == 'inMAGs':
        marker = 'o'      # Circle
        size = 80         # Bigger
    elif label in ['Nisin', 'Gramicidin', 'Daptomycin', 'Defensin', 'Penetratin']:
        marker = '*'      # Square
        size = 60         # Small
    else:
        marker = 'o'
        size = 60

    plt.scatter(
        subset['UMAP1'], subset['UMAP2'],
        label=label, color=palette[label],
        edgecolor='black', s=size, alpha=0.8, marker=marker
    )


plt.legend(title="Labels", loc='upper right')
plt.title("UMAP of Peptides")
plt.xlabel("UMAP1")
plt.ylabel("UMAP2")
plt.tight_layout()
plt.savefig("UMAP_plot.png")
plt.show()
meta[['label', 'sequence', 'UMAP1', 'UMAP2']].to_csv("UMAP_coordinates.tsv", sep="\t", index=False)

