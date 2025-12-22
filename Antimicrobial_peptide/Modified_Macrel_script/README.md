# Long-read mapping (--longreads) in the modified Macrel

This modified Macrel version adds support for Nanopore long-read mapping to a reference AMP FASTA and computes counts and TPM per reference sequence using minimap2 + samtools.

## Command

Use the new command:
```
macrel longreads-abundance --fasta <reference_amps.faa[.gz]> --longreads <reads.fastq[.gz]> --output <outdir> --tag <sample_tag> -t <threads>
```

## Required inputs

--fasta

Reference protein FASTA of AMPs (.faa or .faa.gz).
Example: predicted AMP sequences from Macrel.

--longreads

Long-read FASTQ file (Nanopore reads).
Example: reads.fastq or reads.fastq.gz. 

--output

Output directory.



## What it does 

When you run longreads-abundance, the script performs these steps:

#### 1. Prepare reference FASTA

If --fasta ends with .gz, it is uncompressed into the temporary directory.

Otherwise, it is symlinked. 

#### 2. Map Nanopore reads to the reference with minimap2

Uses the preset: -x map-ont

Outputs SAM alignments. 

#### 3. Convert, sort, and index alignments with samtools

samtools view → BAM

samtools sort

samtools index 

#### 4. Count reads per reference

samtools idxstats produces per-reference mapped read counts.

#### 5. Compute TPM

Converts counts to RPK and TPM and writes a table to disk. 

## Example

```bash
macrel longreads-abundance \
  --fasta Data/Processed/AMP_sequences.faa.gz \
  --longreads Data/Raw/nanopore_reads.fastq.gz \
  --output Results/longread_abundance_sampleA 
```

### Dependencies (long-read mode)

Make sure these are available in your environment / PATH:

> minimap2
> samtools
> pandas 
