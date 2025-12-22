from scipy.stats import wilcoxon
import pandas as pd

# Input CLP and CDP counts from inMAGs only
clp = [78, 116, 15, 59, 27, 32, 49, 93, 76]  
cdp = [55, 54, 5, 36, 15, 20, 33, 49, 50]    

# Wilcoxon signed-rank test
stat, p_value = wilcoxon(clp, cdp)
print(f"Wilcoxon p-value (CLP vs CDP): {p_value:.5f}")

