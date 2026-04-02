"""
Text Generation using HuggingFace Transformers
- Uses distilgpt2 model for lightweight text generation
- Supports custom prompts via command-line arguments
"""

import argparse
from transformers import pipeline

def generate_text(prompt, max_tokens=30, temperature=0.7):
    print(f"[INFO] Loading model: distilgpt2")
    generator = pipeline("text-generation", model="distilgpt2")

    print(f"[INFO] Generating text for prompt: '{prompt}'")
    result = generator(
        prompt,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=temperature
    )

    generated = result[0]["generated_text"]
    return generated

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate text using distilgpt2")
    parser.add_argument("--prompt", type=str, default="AI will change", help="Input prompt for generation")
    parser.add_argument("--max_tokens", type=int, default=30, help="Maximum new tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    args = parser.parse_args()

    output = generate_text(args.prompt, args.max_tokens, args.temperature)
    print(f"\n--- Generated Text ---\n{output}")
