#!/usr/bin/env python3
"""
Example: Process multiple cryptocurrency questions in batch
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_llm import CryptoLLM
from crypto_knowledge import get_prompts_by_category


def main():
    """Batch question processing example"""
    print("Initializing CryptoLLM for batch processing...\n")

    # Initialize model
    llm = CryptoLLM(
        model_name="mistral-7b",
        quantization_bits=4,
    )

    # Get questions from a category
    category = "basics"
    questions = get_prompts_by_category(category)[:3]  # First 3 questions

    print(f"\nProcessing {len(questions)} questions from '{category}' category:\n")
    print("="*60)

    results = []

    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] {question}")
        print("-"*60)

        response = llm.generate(
            question,
            max_new_tokens=256,
            temperature=0.7,
        )

        print(f"Answer: {response}\n")

        results.append({
            "question": question,
            "answer": response,
        })

    # Summary
    print("\n" + "="*60)
    print("Batch processing complete!")
    print(f"Processed {len(results)} questions")
    print("="*60)


if __name__ == "__main__":
    main()
