import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#----------------------
# Load and filter data
#----------------------

df = pd.read_csv("BGC_abundance.csv")
ripp_df = df[df['class'] == 'Other'].copy()

#----------------------
# Melt the GPM columns
#----------------------

gpm_columns = [col for col in ripp_df.columns if 'lg(GPM)' in col]
melted = ripp_df.melt(id_vars=['Predicted product'], 
                      value_vars=gpm_columns,
                      var_name='Metagenome', 
                      value_name='log10_GPM')

#-------------------------------
# Remove zero or missing values
#-------------------------------

melted = melted[melted['log10_GPM'] > 0]

#----------------------------------------
# Set color palette by Predicted product
#----------------------------------------
palette = sns.color_palette("Set2", melted['Predicted product'].nunique())

#-----------
#Plot strip
#-----------

plt.figure(figsize=(10, 6))

sns.stripplot(
    x='Predicted product', 
    y='log10_GPM', 
    data=melted, 
    jitter=True, 
    size=4, 
    hue='Predicted product', 
    dodge=False, 
    palette=palette,
    legend=False
)

plt.ylabel('Gene abundance (GPM)')
plt.xlabel('Other Products')
plt.title('Abundance of BGC Products')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("Other_product_gene.svg", format='svg')
plt.show()
