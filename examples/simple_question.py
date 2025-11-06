#!/usr/bin/env python3
"""
Simple example: Ask a single cryptocurrency question
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_llm import CryptoLLM


def main():
    """Simple single-question example"""
    print("Initializing CryptoLLM...")
    print("This may take a minute the first time as the model downloads.\n")

    # Initialize with default settings (Mistral 7B, 4-bit quantization)
    llm = CryptoLLM(
        model_name="mistral-7b",  # Can also use full path: "mistralai/Mistral-7B-Instruct-v0.2"
        quantization_bits=4,
        max_memory_gb=6,
    )

    # Ask a question
    question = "What is Bitcoin and how does it work?"
    print(f"\nQuestion: {question}\n")
    print("Generating answer...\n")

    response = llm.generate(
        question,
        max_new_tokens=512,
        temperature=0.7,
    )

    print(f"Answer: {response}\n")


if __name__ == "__main__":
    main()
