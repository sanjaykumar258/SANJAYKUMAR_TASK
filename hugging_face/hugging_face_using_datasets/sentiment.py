"""
Sentiment Analysis using HuggingFace Transformers
- Uses DistilBERT fine-tuned on SST-2 for sentiment classification
- Supports analyzing multiple sentences
"""

import argparse
from transformers import pipeline

def analyze_sentiment(texts):
    print("[INFO] Loading model: distilbert-base-uncased-finetuned-sst-2-english")
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    results = classifier(texts)
    return results

def display_results(texts, results):
    print("\n--- Sentiment Analysis Results ---")
    for text, result in zip(texts, results):
        label = result["label"]
        score = result["score"]
        print(f"  Text : {text}")
        print(f"  Label: {label} (confidence: {score:.4f})")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze sentiment of text")
    parser.add_argument(
        "--texts",
        nargs="+",
        default=["This product is amazing!"],
        help="One or more sentences to analyze"
    )
    args = parser.parse_args()

    results = analyze_sentiment(args.texts)
    display_results(args.texts, results)
