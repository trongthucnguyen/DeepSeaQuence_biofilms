import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("AMP_length.csv")
possible_sample_cols = [c for c in df.columns if "sample" in c.lower()]
possible_length_cols = [c for c in df.columns if "length" in c.lower()]

if not possible_sample_cols or not possible_length_cols:
    raise ValueError("Could not detect 'Sample' or 'Length' columns. Please rename manually.")

sample_col = possible_sample_cols[0]
length_col = possible_length_cols[0]

# Sort samples for a consistent order
samples = sorted(df[sample_col].unique())

# Create color palette
palette = sns.color_palette("Paired", len(samples))

# Prepare data grouped by sample
data_to_plot = [df[df[sample_col] == s][length_col] for s in samples]

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))

# Draw the boxplots
box = ax.boxplot(
    data_to_plot,
    patch_artist=True,     
    labels=samples,
    showfliers=True,       
    flierprops=dict(marker='o', markersize=5, markerfacecolor='lightgray', alpha=0.6),
    medianprops=dict(color='white', linewidth=1.5),
    whiskerprops=dict(color='gray', linewidth=1.2),
    capprops=dict(color='gray', linewidth=1.2)
)

for patch, color in zip(box['boxes'], palette):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
    patch.set_edgecolor('gray')

ax.set_ylabel("AMP Length", fontsize=12)
ax.set_xlabel("Sample", fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(alpha=0.3, linestyle='--')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# Save as SVG 
plt.savefig("AMP_length_boxplot.svg", format='svg')
plt.show()
print("Figure saved as 'AMP_length_boxplot_Set3.svg'")

