import pandas as pd
import networkx as nx
from upsetplot import UpSet, from_indicators
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('upset_table.csv', sep=',')

# Create a graph of BGC interactions
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row['source'], row['target'])

# Find connected components (clusters)
components = list(nx.connected_components(G))
bgc_to_cluster = {
    bgc: f'cluster_{i}' for i, comp in enumerate(components) for bgc in comp
}

# Create BGC to metagenome mapping
source_df = df[['source', 'source_metagenome']].copy()
target_df = df[['target', 'target_metagenome']].copy()
source_df.columns = ['bgc', 'metagenome']
target_df.columns = ['bgc', 'metagenome']
bgc_meta = pd.concat([source_df, target_df], ignore_index=True).drop_duplicates()
bgc_meta['cluster'] = bgc_meta['bgc'].map(bgc_to_cluster)

# Build binary matrix of cluster vs metagenome
cluster_meta = pd.crosstab(bgc_meta['cluster'], bgc_meta['metagenome']).astype(bool)
print(cluster_meta)
cluster_meta.to_csv("cluster_metagenome_matrix.csv")

# Prepare data for UpSet plot
upset_data = from_indicators(cluster_meta.columns.tolist(), cluster_meta)

# Plot
fig = plt.figure(figsize=(10, 6))
upset = UpSet(upset_data, subset_size='count', show_counts=True)
upset.plot(fig=fig)

# Save plot
plt.savefig("upset_plot.svg", format='svg')
plt.show()

