# HuggingFace NLP Tasks

This project demonstrates core NLP capabilities using HuggingFace Transformers — including **authentication**, **text generation**, and **sentiment analysis**.

---

## 📁 Project Structure

```
huggingface/
├── login.py        # HuggingFace Hub authentication
├── generation.py   # Text generation using distilgpt2
├── sentiment.py    # Sentiment analysis using DistilBERT
└── README.md
```

---

## ⚙️ Installation

```bash
pip install transformers huggingface_hub torch
```

---

## 🔐 1. Login — `login.py`

Authenticates with the HuggingFace Hub. Supports both **environment variable** and **interactive** login.

```bash
# Option A: Set token as environment variable
set HF_TOKEN=your_token_here
python login.py

# Option B: Interactive login (browser-based prompt)
python login.py
```

---

## ✍️ 2. Text Generation — `generation.py`

Generates text using the **distilgpt2** model.

```bash
# Default prompt
python generation.py

# Custom prompt
python generation.py --prompt "The future of technology" --max_tokens 50 --temperature 0.9
```

### Arguments

| Argument        | Type  | Default            | Description                    |
|-----------------|-------|--------------------|--------------------------------|
| `--prompt`      | str   | `"AI will change"` | Input prompt for generation    |
| `--max_tokens`  | int   | `30`               | Maximum new tokens to generate |
| `--temperature` | float | `0.7`              | Sampling temperature           |

### Sample Output

```
[INFO] Loading model: distilgpt2
[INFO] Generating text for prompt: 'AI will change'

--- Generated Text ---
AI will change the nature of the public's trust in government.
```

---

## 📊 3. Sentiment Analysis — `sentiment.py`

Classifies text sentiment (POSITIVE / NEGATIVE) using **DistilBERT** fine-tuned on the SST-2 dataset.

```bash
# Single sentence
python sentiment.py

# Multiple sentences
python sentiment.py --texts "This product is amazing!" "Terrible experience, never again."
```

### Arguments

| Argument  | Type     | Default                        | Description                     |
|-----------|----------|--------------------------------|---------------------------------|
| `--texts` | str list | `["This product is amazing!"]` | One or more sentences to analyze |

### Sample Output

```
[INFO] Loading model: distilbert-base-uncased-finetuned-sst-2-english

--- Sentiment Analysis Results ---
  Text : This product is amazing!
  Label: POSITIVE (confidence: 0.9999)

  Text : Terrible experience, never again.
  Label: NEGATIVE (confidence: 0.9998)
```

---

## 🧰 Tech Stack

- **Python 3.8+**
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [HuggingFace Hub](https://huggingface.co/docs/huggingface_hub)
- **Models Used:**
  - [`distilgpt2`](https://huggingface.co/distilgpt2) — Text generation
  - [`distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) — Sentiment analysis
