import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
file_path = "Predicted_MICs.csv"
df = pd.read_csv(file_path)
df.set_index("AMP_ID", inplace=True)

# Threshold for activity
threshold = 100

# Count how many AMPs are active against each pathogen
active_counts_per_pathogen = (df < threshold).sum(axis=0)

# --- Plot ---
plt.figure(figsize=(10, 6))
active_counts_per_pathogen.sort_values(ascending=False).plot(
    kind="bar", color="forestgreen"
)
plt.ylabel("Number of active AMPs")
plt.xlabel("Pathogen strain")
plt.title("Number of AMPs Active Against Each Pathogen")
plt.xticks(rotation=75, ha="right")
plt.tight_layout()

# Save as SVG (optional)
plt.savefig("AMPs_per_pathogen.svg", format="svg")

plt.show()

