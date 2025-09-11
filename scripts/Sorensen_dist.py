import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------
# Load presence/absence data
# ------------------------
df = pd.read_csv("relative_abundance.csv")
df = df[~df["Order"].isin(["unclassified", "unknown", "nan"])] 
sample_cols = ['M24', 'M25', 'M26', 'M36', 'M37', 'M38', 'M39', 'M33', 'M42']
print(df["Order"].unique())

# Aggregate to Order level
order_abund = df.groupby("Order")[sample_cols].sum()

# Convert to presence/absence
presence_absence = (order_abund > 0).astype(int)
samples = presence_absence.columns.tolist()

# ------------------------
# Calculate Sørensen similarity and permutation p-values
# ------------------------
n = len(samples)
sorensen_matrix = pd.DataFrame(np.zeros((n, n)), index=samples, columns=samples)
pval_matrix = pd.DataFrame(np.ones((n, n)), index=samples, columns=samples)
n_perm = 1000

for i in range(n):
    for j in range(i, n):
        a = presence_absence[samples[i]]
        b = presence_absence[samples[j]]

        shared = np.sum((a + b) == 2)
        total = np.sum(a) + np.sum(b)
        sorensen_score = (2 * shared) / total if total > 0 else 0
        sorensen_matrix.iloc[i, j] = sorensen_score
        sorensen_matrix.iloc[j, i] = sorensen_score

        # Permutation test
        null_dist = []
        for _ in range(n_perm):
            np.random.shuffle(b.values)
            shared_perm = np.sum((a + b) == 2)
            total_perm = np.sum(a) + np.sum(b)
            score_perm = (2 * shared_perm) / total_perm if total_perm > 0 else 0
            null_dist.append(score_perm)
        p_val = np.mean([s >= sorensen_score for s in null_dist])
        pval_matrix.iloc[i, j] = p_val
        pval_matrix.iloc[j, i] = p_val

# ------------------------
# Save similarity and p-value matrices
# ------------------------
sorensen_matrix.to_csv("sorensen_similarity.csv")
pval_matrix.to_csv("sorensen_pvalues.csv")

# ------------------------
# Convert similarity to dissimilarity
# ------------------------
sorensen_dissimilarity = 1 - sorensen_matrix
sorensen_dissimilarity.to_csv("sorensen_dissimilarity.csv")

# ------------------------
# Print data tables
# ------------------------

print("Sørensen Similarity Matrix:\n", sorensen_matrix.round(3))
print("Permutation Test P-values:\n", pval_matrix.round(3))
print("Sørensen Dissimilarity Matrix:\n", sorensen_dissimilarity.round(3))

# ------------------------
# Plot heatmap of dissimilarity
# ------------------------
plt.figure(figsize=(8, 6))
sns.heatmap(sorensen_dissimilarity, cmap="coolwarm", annot=False)
plt.title("Sørensen Dissimilarity Heatmap")
plt.tight_layout()
plt.savefig("sorensen_dissimilarity_heatmap.svg", format='svg')
plt.show()

