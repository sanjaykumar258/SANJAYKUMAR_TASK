import argparse
from transformers import pipeline
from datasets import load_dataset

def run_sentiment_on_dataset(num_samples=5):
    print("[INFO] Loading dataset: imdb")
    # Using a small slice of imdb to save time
    dataset = load_dataset("imdb", split=f"test[:{num_samples}]")
    texts = [sample["text"][:200] + "..." for sample in dataset] # truncate to avoid large outputs
    
    print("[INFO] Loading model: distilbert-base-uncased-finetuned-sst-2-english")
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    results = classifier(texts)
    print("\n--- Sentiment Analysis Results on IMDB Dataset ---")
    for text, result in zip(texts, results):
        print(f"  Text : {text}")
        print(f"  Label: {result['label']} (confidence: {result['score']:.4f})")
        print()

def run_generation_on_dataset(num_samples=3):
    print("[INFO] Loading dataset: ag_news")
    # Using a small slice of ag_news to save time
    dataset = load_dataset("ag_news", split=f"test[:{num_samples}]")
    prompts = [sample["text"][:50] + "..." for sample in dataset]

    print("[INFO] Loading model: distilgpt2")
    generator = pipeline("text-generation", model="distilgpt2")

    print("\n--- Text Generation Results on AG News Dataset ---")
    for prompt in prompts:
        print(f"\n[Prompt]: {prompt}")
        result = generator(prompt, max_new_tokens=30, do_sample=True, temperature=0.7, pad_token_id=50256)
        print(f"[Generated]: {result[0]['generated_text']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run HF models on huggingface datasets")
    parser.add_argument("--task", type=str, choices=["sentiment", "generation", "both"], default="both", help="Task to run")
    parser.add_argument("--samples", type=int, default=3, help="Number of dataset samples to evaluate")
    args = parser.parse_args()

    if args.task in ["sentiment", "both"]:
        run_sentiment_on_dataset(args.samples)
    if args.task in ["generation", "both"]:
        run_generation_on_dataset(args.samples)
