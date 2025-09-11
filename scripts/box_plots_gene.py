import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("BGC_abundance.csv") 

# Melt the dataframe to long format
tpm_cols = [col for col in df.columns if 'lg(GPM)' in col]
df_melted = df.melt(id_vars=['class'], value_vars=tpm_cols,
                    var_name='Sample', value_name='GPM')

# Drop NaN or zero values to clean up the plots
df_melted = df_melted[df_melted['GPM'] > 0]

# Filter to only include the desired 6 classes
classes_of_interest = ['Hybrid', 'NRP', 'Other', 'Polyketide', 'RiPP', 'Terpene']
df_melted = df_melted[df_melted['class'].isin(classes_of_interest)]

class_colors = {
    'Hybrid': 'tomato',
    'NRP': 'chocolate',
    'Other': 'bisque',
    'Polyketide': 'forestgreen',
    'RiPP': 'turquoise',
    'Terpene': 'plum'
}

# Calculate IQR for each class
for cls in classes_of_interest:
    class_data = df_melted[df_melted['class'] == cls]['GPM']
    q1 = class_data.quantile(0.25)
    q3 = class_data.quantile(0.75)
    iqr = q3 - q1
    print(f"{cls}: Q1 = {q1:.2f}, Q3 = {q3:.2f}, IQR = {iqr:.2f}")

# Create the boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(
	data=df_melted, 
	x='class', 
	y='GPM', 
	hue='class',
	palette=class_colors, 
	order=classes_of_interest, 
	dodge=False,
	legend=False
)

plt.title('Gene abundance of BGC')
plt.ylabel('Gene abundance (lgGPM)')
plt.xlabel('BGC Class')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("bgc_class_boxplot.svg", format="svg")
plt.show()


