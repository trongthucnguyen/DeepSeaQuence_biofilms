This repository contains the processed data tables used to generate figures in the paper. Each dataset is linked to the corresponding figure(s) and analysis script(s).

Main Figures
* Figure 2
    * Data: MAG_phylum.csv
    * Script: Barplot_MAG_phylum.py
* Figures 5A, 6A
    * Data: MAG_summary.csv, BGC_class.csv
    * Script: Barplot_BGC_count.py
* Figures 5B, 6B
    * Data: BGC_expression.csv
    * Script: heatmap_metagenome_expression.py
* Figure 7
    * Data: BGC_expression.csv
    * Script: heatmap_BGC_product.py

Supplementary Figures
* Figures S1, S2
    * Data: relative_abundance.csv
    * Scripts: Bray_Curtis_boostrap.py, Sorensen.py
* Figures S3A, S3B
    * Data: BGC_abundance.csv
    * Scripts: stripplot_RiPP.py, stripplot_other.py
* Figure S3
    * Data: transcript_abundance.csv
    * Script: stripplot_transcript.py (or confirm if this belongs here)
* Figure S6A
    * Data: BGC_abundance.csv
    * Script: box_plots_gene.py
* Figure S6B
    * Data: transcript_abundance.csv
    * Script: box_plots_transcript.py

Notes
  All data files are in .csv format.
  Scripts are written in Python (.py).
  Each script generates the corresponding figure when run with its associated data file(s).

