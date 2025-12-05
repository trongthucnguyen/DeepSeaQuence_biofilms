# README – Modified BiG-MAP.map Script (Minimap2 Integration)

## 1) Overview

This repository contains a modified version of the BiG-MAP.map module from the BiG-MAP pipeline. This modified script was developed based on the original BiG-MAP v1.0.0 release.
The modification integrates Minimap2 to enable long-read mapping of Oxford Nanopore sequencing data.

## 2) Requirements

To use this modified script, you must first install the official BiG-MAP pipeline:

🔗 BiG-MAP GitHub: https://github.com/medema-group/BiG-MAP

You must also have Minimap2 installed and accessible in your $PATH.

How to Use This Modified Script

Install BiG-MAP from the official repository.

Locate the BiG-MAP.map file inside the BiG-MAP installation directory.

Add this modified version to the same folder.

Run BiG-MAP as usual, but use the Minimap2-enabled script to map Nanopore reads.

Example command to activate Minimap2 mapping
```
conda activate BiG-MAP_process
python Modified_BiG-MAP.map.py --longreads -U [samples] -F [family] -O [outdir] -b [metadata] [Options*]
```


## 3) Citation

If you use this modified script in your work, please cite the following:

#### Original BiG-MAP Pipeline

Andreu V. P., Augustijn H. E., van den Berg K., van der Hooft J. J. J., Fischbach M. A., Medema M. H. BiG-MAP: an Automated Pipeline To Profile Metabolic Gene Cluster Abundance and Expression in Microbiomes.
mSystems (2021).

https://doi.org/10.1128/msystems.00937-21

#### Modification Minimap2 Long-Read Mapping

Nguyen T.T., Steen I.H., Stokke R. Remarkable biosynthetic capacity of Arctic hydrothermal biofilms (2025).

https://doi.org/10.21203/rs.3.rs-7619139/v1

***
### License

This modified script follows the terms of the MIT License of the original BiG-MAP codebase:

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the conditions stated in the original license.
