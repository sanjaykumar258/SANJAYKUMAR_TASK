import json
import numpy as np
from itertools import combinations
from sentence_transformers import SentenceTransformer, util

class TextSimilarityAnalyzer:
    """
    A class to encapsulate the loading, embedding, and comparing of sentences
    using sentence-transformers.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        print(f"Loading model '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        self.sentences = []
        self.embeddings = None
        self.similarity_matrix = None

    def load_sentences(self, sentences: list):
        """Loads a list of sentences into the analyzer."""
        self.sentences = sentences
        print(f"Loaded {len(self.sentences)} sentences.")

    def compute_embeddings(self):
        """Generates embeddings for the loaded sentences and displays their details."""
        if not self.sentences:
            raise ValueError("No sentences loaded. Call load_sentences() first.")
            
        print("\nGenerating embeddings...")
        self.embeddings = self.model.encode(self.sentences)
        
        print("\n--- Embeddings Details ---")
        for sentence, emb in zip(self.sentences, self.embeddings):
            print(f"Sentence: '{sentence}'")
            print(f"Shape: {emb.shape}")
            print(f"First 5 values: {emb[:5]}")
            print("-" * 60)

    def compute_similarity_matrix(self):
        """Calculates and displays the cosine similarity matrix."""
        if self.embeddings is None:
            raise ValueError("Embeddings not computed. Call compute_embeddings() first.")
            
        print("\n--- Cosine Similarity Matrix ---")
        self.similarity_matrix = util.cos_sim(self.embeddings, self.embeddings).numpy()
        
        # Formatted printing of the matrix
        header_row = "    " + "".join([f"{i:>7}" for i in range(len(self.sentences))])
        print(header_row)
        for idx, row in enumerate(self.similarity_matrix):
            print(f"{idx:>2}  " + "".join([f"{val:>7.2f}" for val in row]))

    def display_similarity_extremes(self):
        """Finds and prints the most and least similar pairs of sentences."""
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not computed. Call compute_similarity_matrix() first.")

        # Extract only the unique pairs (upper triangle of the matrix without diagonal)
        indices = list(combinations(range(len(self.sentences)), 2))
        similarities = [self.similarity_matrix[i, j] for i, j in indices]

        max_idx = int(np.argmax(similarities))
        min_idx = int(np.argmin(similarities))

        print("\n--- Similarity Extremes ---")
        self._print_pair("Most similar pair", indices[max_idx], similarities[max_idx])
        self._print_pair("Least similar pair", indices[min_idx], similarities[min_idx])

    def _print_pair(self, title: str, pair_indices: tuple, similarity_score: float):
        """Helper method to neatly print a pair and its score."""
        print(f"{title}:")
        print(f" 1: '{self.sentences[pair_indices[0]]}'")
        print(f" 2: '{self.sentences[pair_indices[1]]}'")
        print(f" Similarity: {similarity_score:.4f}\n")

    def export_data(self, filename: str = 'sentence_embeddings.json'):
        """Saves the sentences and their corresponding embeddings to a JSON file."""
        if self.embeddings is None:
            raise ValueError("Embeddings not computed, nothing to export.")
            
        print(f"Saving output to {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "sentences": self.sentences,
                "embeddings": self.embeddings.tolist()
            }, f, indent=4)
        print("Process completed successfully.")


if __name__ == "__main__":
    # Define our dataset
    sentences_list = [
        "The James Webb Space Telescope captured stunning images of distant galaxies.",
        "Astronauts undergo rigorous training to prepare for extended missions in orbit.",
        "Learning to play the piano requires patience, practice, and a good sense of rhythm.",
        "The symphony orchestra delivered a powerful performance of Beethoven's Fifth.",
        "Exploring ancient ruins gives us a fascinating glimpse into past civilizations.",
        "Historians spend years studying primary sources to understand historical events.",
        "The vibrant street market was filled with the aroma of exotic spices.",
        "A robust cup of coffee is the perfect way to kickstart a busy morning."
    ]

    # Initialize the analyzer and run the pipeline
    analyzer = TextSimilarityAnalyzer()
    analyzer.load_sentences(sentences_list)
    analyzer.compute_embeddings()
    analyzer.compute_similarity_matrix()
    analyzer.display_similarity_extremes()
    analyzer.export_data()
