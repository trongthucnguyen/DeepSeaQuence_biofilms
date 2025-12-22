import pandas as pd
import scikit_posthocs as sp
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv("expressed_AMP.csv")

# Perform Dunn's test with Holm correction
dunn = sp.posthoc_dunn(df, val_col='log (TPM)', group_col='Metagenome', p_adjust='holm')

# Display the result matrix
print("Dunn's test results (adjusted p-values):")
print(dunn.round(4))

# Optional: highlight samples that significantly differ from the rest
# For example, sample M39 differs significantly from most others if its row/column has many p < 0.05

