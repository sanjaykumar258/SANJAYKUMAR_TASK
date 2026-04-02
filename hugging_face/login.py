"""
HuggingFace Hub Authentication
- Logs in to HuggingFace Hub using token-based authentication
- Supports both interactive and token-based login
"""

import os
from huggingface_hub import login

def huggingface_login():
    token = os.environ.get("HF_TOKEN")

    if token:
        print("[INFO] Using HF_TOKEN from environment variable...")
        login(token=token)
        print("[SUCCESS] Logged in via environment token.")
    else:
        print("[INFO] No HF_TOKEN found. Launching interactive login...")
        login()
        print("[SUCCESS] Logged in interactively.")

if __name__ == "__main__":
    huggingface_login()
