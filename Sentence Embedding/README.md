# Sentence Embeddings Analyzer

A simple, beautifully structured object-oriented Python pipeline for generating and analyzing text embeddings using the Hugging Face `sentence-transformers` library.

## Overview

This project provides a robust class `TextSimilarityAnalyzer` inside `sentence_embeddings_analyzer.py` that takes a list of sentences, calculates their embedding vectors, and matches them to discover exactly how similar they are. 

It accomplishes the following:
1. Loads an optimized local language model (`all-MiniLM-L6-v2` by default).
2. Generates sentence embeddings utilizing the model.
3. Computes the cosine similarity matrix for the inputted sentences cleanly with `sentence-transformers`.
4. Leverages `numpy` to find and display the absolute *most similar* and *least similar* sentence pairings from the dataset.
5. Exports the parsed sentences and generated embedding vectors securely to a standardized `sentence_embeddings.json` output file.

## Prerequisites

Ensure you have the required dependencies installed before running the program:

```bash
pip install sentence-transformers numpy
```
*(Note: Installing `sentence-transformers` automatically installs PyTorch and Transformers).*

## Usage

You can run the analyzer directly through Python:

```bash
python sentence_embeddings_analyzer.py
```

### Extending the Sentences

The project is easily extensible due to the Object-Oriented structure. Inside `sentence_embeddings_analyzer.py`, locate the `if __name__ == "__main__":` block at the bottom of the script, and confidently replace or add to the `sentences_list` with any textual data you wish to analyze!

## Output 

Upon execution, the script will:
- Print the detailed matrix outputs directly to the console.
- Output detailed text properties containing the highest and lowest similarity matches.
- Save `sentence_embeddings.json` in your current directory, cataloging the data for further integrations or uses!
