import pandas as pd
from scipy.stats import kruskal
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("expressed_AMP.csv")

# Kruskal-Wallis test
groups = [group["log (TPM)"].values for name, group in df.groupby("Metagenome")]
stat, p = kruskal(*groups)
print(f"Kruskal-Wallis H-statistic: {stat:.3f}, p-value: {p:.3e}")

# Custom color palette
palette = sns.color_palette("Set2", n_colors=df["Metagenome"].nunique())

# Plot
plt.figure(figsize=(8, 7))
ax = sns.boxplot(x="Metagenome", y="log (TPM)", hue="Metagenome", data=df, palette=palette, legend=False)

# Annotate p-value inside plot using data coordinates
y_max = df["log (TPM)"].max()
text = f"Kruskal–Wallis H = {stat:.2f}, p = {p:.2e}"
ax.text(x=0.5, y=y_max * 1.05, s=text, ha="center", fontsize=12)

# Labels and layout
plt.xlabel("Sample", fontsize=12)
plt.ylabel("log(TPM)", fontsize=12)
plt.xticks(rotation=45)
plt.subplots_adjust(top=0.88)
plt.savefig("AMP_expression_plot.svg", format="svg", dpi=300)
plt.show()

