# FAISS Vector Database Exploration

This repository contains an exploratory Python implementation of Vector Databases using Meta's **FAISS** (Facebook AI Similarity Search) library and Hugging Face's **Sentence Transformers**. 

## Features & Implemented Tasks

The singular explore script (`faiss_explorer.py`) covers four primary tasks:

1. **Basic Vector Search (`IndexFlatL2`)**: Generates random high-dimensional embeddings and performs a basic k-nearest neighbors search based on the Euclidean (L2) distance.
2. **Semantic Similarity Search**: Uses the `all-MiniLM-L6-v2` transformer model to encode natural language phrases into dense vectors, and successfully returns the most semantically relevant phrases to a given query.
3. **Context-Aware Document Retrieval**: An implementation of an intelligent metadata-filtered pipeline. Documents are stored with their respective context (e.g., "History", "Science") and FAISS is used to perform a nearest-neighbor semantic search that respects strict contextual boundaries.
4. **Near-Duplicate Detection Engine**: Automatically flags and aggregates duplicate or near-duplicate phrases by encoding a dataset and using an L2 distance threshold to group sentences that are semantically identical.

## Prerequisites

This script requires Python 3.x and relies on the following major libraries:
- `faiss-cpu`
- `sentence-transformers`
- `numpy`

## Installation

It is recommended to run this project inside a Python virtual environment.

1. **Create and Activate a Virtual Environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate   # On Windows
   # source venv/bin/activate # On Unix/MacOS
   ```

2. **Install the Dependencies:**
   ```powershell
   pip install faiss-cpu sentence-transformers numpy
   ```

## Usage

To execute the exploration script and view the output for all four tasks, simply run:

```powershell
python faiss_explorer.py
```

*Note: The first time you run the script, `sentence-transformers` will automatically download and cache the weights for the `all-MiniLM-L6-v2` model from the Hugging Face Hub.*
