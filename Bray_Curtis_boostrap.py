import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from skbio.stats.distance import DistanceMatrix
from skbio.stats.ordination import pcoa
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load and aggregate data
# -------------------------------
df = pd.read_csv("relative_abundance.csv") 
sample_cols = ['M24', 'M25', 'M26', 'M36', 'M37',
               'M38', 'M39', 'M33', 'M42']

# Aggregate by order and transpose
order_abund = df.groupby("Order")[sample_cols].sum()
df_abund = order_abund.T  # samples as rows

# -------------------------------
# Bootstrap Bray-Curtis with 95% CI
# -------------------------------
def bootstrap_bray_curtis(df, n_boot=1000, sample_size=None):
    dist_matrices = []
    for _ in range(n_boot):
        df_boot = df.sample(n=sample_size or df.shape[1], replace=True, axis=1)
        bc_dist = pdist(df_boot.values, metric='braycurtis')
        dist_matrices.append(bc_dist)

    dist_array = np.array(dist_matrices)
    ci_lower = np.percentile(dist_array, 2.5, axis=0)
    ci_upper = np.percentile(dist_array, 97.5, axis=0)
    dist_mean = np.mean(dist_array, axis=0)

    return dist_mean, ci_lower, ci_upper, squareform(dist_mean)

# Run bootstrap
mean_dist, ci_low, ci_up, mean_matrix = bootstrap_bray_curtis(df_abund)
samples = df_abund.index.tolist()

# Convert to DataFrames
mean_df = pd.DataFrame(mean_matrix, index=samples, columns=samples)
low_df = pd.DataFrame(squareform(ci_low), index=samples, columns=samples)
up_df = pd.DataFrame(squareform(ci_up), index=samples, columns=samples)

# Print summary
print("Mean Bray-Curtis Distance Matrix:\n", mean_df.round(3))
print("Lower 95% CI Matrix:\n", low_df.round(3))
print("Upper 95% CI Matrix:\n", up_df.round(3))

# Save to CSV
mean_df.to_csv("braycurtis_bootstrap_mean.csv")
low_df.to_csv("braycurtis_bootstrap_lowerCI.csv")
up_df.to_csv("braycurtis_bootstrap_upperCI.csv")

# -------------------------------
# PCoA
# -------------------------------
bray_dm = DistanceMatrix(mean_matrix.copy(), ids=samples)
ordination = pcoa(bray_dm)
pcoa_df = ordination.samples
pcoa_df['Sample'] = pcoa_df.index

# -------------------------------
# Data visualization
# -------------------------------
# Assign a color label to each sample
sample_colors = {
    'M24': 'salmon',
    'M25': 'sandybrown',
    'M26': 'navajowhite',
    'M36': 'olive',
    'M37': 'palegreen',
    'M38': 'aquamarine',
    'M39': 'skyblue',
    'M33': 'slateblue',
    'M42': 'plum'
}

# Add color info to the DataFrame
pcoa_df['Color'] = pcoa_df['Sample'].map(sample_colors)


plt.figure(figsize=(8, 6))

# Use seaborn to handle color and legend automatically
sns.scatterplot(
    data=pcoa_df,
    x='PC1',
    y='PC2',
    hue='Sample',          
    palette=sample_colors, 
    s=100
)

# Add text labels next to each point
for i in range(len(pcoa_df)):
    plt.text(
        pcoa_df['PC1'].iloc[i] + 0.01,
        pcoa_df['PC2'].iloc[i],
        pcoa_df['Sample'].iloc[i],
        fontsize=9
    )

plt.xlabel(f"PC1 ({ordination.proportion_explained.iloc[0]*100:.2f}%)")
plt.ylabel(f"PC2 ({ordination.proportion_explained.iloc[1]*100:.2f}%)")
plt.title("PCoA")
plt.grid(True)
plt.legend(title='Sample', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("PCoA_Bray_Curtis.svg", format='svg')
plt.show()

