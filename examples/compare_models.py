#!/usr/bin/env python3
"""
Example: Compare responses from different models
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_llm import CryptoLLM


def test_model(model_name, question):
    """Test a single model and return response with timing"""
    print(f"\nTesting model: {model_name}")
    print("-"*60)

    start_time = time.time()

    try:
        llm = CryptoLLM(
            model_name=model_name,
            quantization_bits=4,
            max_memory_gb=6,
        )

        load_time = time.time() - start_time

        gen_start = time.time()
        response = llm.generate(question, max_new_tokens=256)
        gen_time = time.time() - gen_start

        return {
            "model": model_name,
            "response": response,
            "load_time": load_time,
            "generation_time": gen_time,
            "success": True,
        }

    except Exception as e:
        return {
            "model": model_name,
            "error": str(e),
            "success": False,
        }


def main():
    """Compare different models"""
    question = "What is DeFi?"

    # Models to compare (adjust based on what you want to test)
    models = [
        "phi-2",          # Fastest
        "tinyllama",      # Most efficient
        "mistral-7b",     # Best quality
    ]

    print("="*60)
    print("Model Comparison")
    print("="*60)
    print(f"\nQuestion: {question}\n")

    results = []

    for model in models:
        result = test_model(model, question)
        results.append(result)

        if result["success"]:
            print(f"\nResponse: {result['response']}")
            print(f"\nLoad time: {result['load_time']:.2f}s")
            print(f"Generation time: {result['generation_time']:.2f}s")
        else:
            print(f"\nError: {result['error']}")

        print("\n" + "="*60)

    # Summary
    print("\nSummary:")
    print("-"*60)

    for result in results:
        if result["success"]:
            print(f"{result['model']:20s} | Load: {result['load_time']:6.2f}s | Gen: {result['generation_time']:6.2f}s")
        else:
            print(f"{result['model']:20s} | FAILED")


if __name__ == "__main__":
    main()
