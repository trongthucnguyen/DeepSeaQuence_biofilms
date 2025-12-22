import pandas as pd
import numpy as np
from Bio.Align import PairwiseAligner

def make_aligner(mode: str = "global") -> PairwiseAligner:
    aligner = PairwiseAligner()
    aligner.mode = mode
    return aligner

def compute_similarity_matrix(sequences, aligner: PairwiseAligner) -> np.ndarray:
    sequences = list(sequences)
    n = len(sequences)
    sim = np.zeros((n, n), dtype=float)

    for i in range(n):
        sim[i, i] = aligner.align(sequences[i], sequences[i]).score
        for j in range(i + 1, n):
            score = aligner.align(sequences[i], sequences[j]).score
            sim[i, j] = score
            sim[j, i] = score  # symmetric
    return sim

def main():
    # Load data
    data = pd.read_csv("peptide_test.txt", sep="\t")
    print("Unique labels:", data["label"].unique())

    # Compute similarity matrix
    aligner = make_aligner(mode="global")
    similarity_matrix = compute_similarity_matrix(data["sequence"], aligner)

    # Save as TSV (with labels as row/column headers)
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=data["label"],
        columns=data["label"]
    )
    similarity_df.to_csv("similarity_matrix.tsv", sep="\t")

    # Optional print
    print("\nSimilarity Matrix (Pairwise Alignment Scores):")
    print(similarity_df.to_string())

    print("\nSaved: similarity_matrix.tsv")

if __name__ == "__main__":
    main()
