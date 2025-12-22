import pandas as pd
from scipy.stats import wilcoxon
import numpy as np

# Input data
data = {
    "Sample": ["M24", "M24_unbinned", "M25", "M25_unbinned", "M26", "M26_unbinned",
               "M33", "M33_unbinned", "M36", "M36_unbinned", "M37", "M37_unbinned",
               "M38", "M38_unbinned", "M39", "M39_unbinned", "M42", "M42_unbinned"],
    "Total_AMP": [133, 247, 170, 285, 20, 48, 95, 343, 42, 61, 52, 311, 82, 270, 142, 416, 126, 89],
    "CLP": [78, 151, 116, 185, 15, 34, 59, 200, 27, 43, 32, 183, 49, 188, 93, 269, 76, 59],
    "CDP": [55, 95, 54, 98, 5, 14, 36, 142, 15, 18, 20, 125, 33, 79, 49, 145, 50, 30]
}

df = pd.DataFrame(data)

# Separate inMAG and unbinned rows
inMAG_df = df[~df['Sample'].str.contains('unbinned')].reset_index(drop=True)
unbinned_df = df[df['Sample'].str.contains('unbinned')].reset_index(drop=True)

# Function to run Wilcoxon test
def compare_paired(name, col):
    x = inMAG_df[col]
    y = unbinned_df[col]

    # Wilcoxon signed-rank test (non-parametric)
    try:
        w_stat, w_p = wilcoxon(x, y)
    except ValueError:
        w_p = np.nan

    return {
        "Measure": name,
        "Wilcoxon_p": w_p
    }

# Run comparisons
results = [
    compare_paired("Total AMP", "Total_AMP"),
    compare_paired("CLP", "CLP"),
    compare_paired("CDP", "CDP"),
]

# CLP/CDP ratio comparison
inMAG_ratio = inMAG_df["CLP"] / inMAG_df["CDP"]
unbinned_ratio = unbinned_df["CLP"] / unbinned_df["CDP"]

try:
    w_ratio_p = wilcoxon(inMAG_ratio, unbinned_ratio)[1]
except ValueError:
    w_ratio_p = np.nan

results.append({
    "Measure": "CLP/CDP ratio",
    "Wilcoxon_p": w_ratio_p
})

# Convert results to DataFrame and print
results_df = pd.DataFrame(results)
print(results_df)

