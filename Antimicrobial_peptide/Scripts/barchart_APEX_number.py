import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = "Predicted_MICs.csv"
df = pd.read_csv(file_path)
df.set_index("AMP_ID", inplace=True)

# Define threshold for activity (MIC < 100)
threshold = 100

# Boolean mask for activity
active_mask = df < threshold

# Count how many pathogens each AMP inhibits
active_counts = active_mask.sum(axis=1)

# Distribution of AMPs (how many AMPs are active against 1, 2, ... pathogens)
distribution = active_counts.value_counts().sort_index()

# Keep only AMPs active against at least 1 pathogen
distribution_nonzero = distribution[distribution.index > 0]

# --- Plot ---
plt.figure(figsize=(8, 6))
plt.bar(distribution_nonzero.index, distribution_nonzero.values, color="gold")
plt.xlabel("Number of pathogens inhibited by APEX 1.1")
plt.ylabel("Number of AMPs")
plt.title("Distribution of AMPs by Spectrum of Activity")
plt.xticks(range(1, distribution_nonzero.index.max() + 1))
plt.tight_layout()
plt.savefig("AMP_distribution.svg", format="svg")
plt.show()

