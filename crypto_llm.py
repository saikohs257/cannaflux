#!/usr/bin/env python3
"""
CryptoLLM - A cryptocurrency-focused language model optimized for 6GB VRAM
"""

import os
import torch
from typing import Optional, Dict, Any
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    GenerationConfig,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CryptoLLM:
    """
    Cryptocurrency-focused LLM with memory-efficient quantization
    """

    # Recommended models that fit in 6GB VRAM with 4-bit quantization
    SUPPORTED_MODELS = {
        "mistral-7b": "mistralai/Mistral-7B-Instruct-v0.2",
        "phi-2": "microsoft/phi-2",
        "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "llama2-7b": "meta-llama/Llama-2-7b-chat-hf",
        "zephyr-7b": "HuggingFaceH4/zephyr-7b-beta",
    }

    def __init__(
        self,
        model_name: str = None,
        quantization_bits: int = 4,
        max_memory_gb: int = 6,
        device: str = "auto",
    ):
        """
        Initialize the CryptoLLM

        Args:
            model_name: Hugging Face model identifier or key from SUPPORTED_MODELS
            quantization_bits: Bit precision for quantization (4 or 8)
            max_memory_gb: Maximum VRAM to use in GB
            device: Device to use ('cuda', 'cpu', or 'auto')
        """
        self.model_name = model_name or os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2")

        # If model_name is a key in SUPPORTED_MODELS, use the full path
        if self.model_name in self.SUPPORTED_MODELS:
            self.model_name = self.SUPPORTED_MODELS[self.model_name]

        self.quantization_bits = int(os.getenv("QUANTIZATION_BITS", quantization_bits))
        self.max_memory_gb = int(os.getenv("MAX_MEMORY_GB", max_memory_gb))
        self.device = os.getenv("DEVICE", device)

        # Cryptocurrency system prompt
        self.system_prompt = """You are a cryptocurrency expert AI assistant. You have deep knowledge about:
- Blockchain technology and consensus mechanisms
- Bitcoin, Ethereum, and major altcoins
- DeFi (Decentralized Finance) protocols and applications
- NFTs and digital assets
- Cryptocurrency trading, technical analysis, and market dynamics
- Smart contracts and Web3 development
- Tokenomics and cryptocurrency economics
- Security best practices and wallet management

Provide accurate, detailed, and up-to-date information about cryptocurrency topics. Always remind users to do their own research (DYOR) and never give financial advice."""

        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        """Load the model with quantization configuration"""
        print(f"Loading model: {self.model_name}")
        print(f"Quantization: {self.quantization_bits}-bit")
        print(f"Max VRAM: {self.max_memory_gb}GB")

        # Configure quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=(self.quantization_bits == 4),
            load_in_8bit=(self.quantization_bits == 8),
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )

        # Set pad token if not exists
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load model with quantization
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            max_memory={0: f"{self.max_memory_gb}GB"},
            low_cpu_mem_usage=True,
        )

        print("Model loaded successfully!")
        self._print_model_info()

    def _print_model_info(self):
        """Print model information and memory usage"""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1024**3
            reserved = torch.cuda.memory_reserved(0) / 1024**3
            print(f"GPU Memory - Allocated: {allocated:.2f}GB, Reserved: {reserved:.2f}GB")

    def _format_prompt(self, user_message: str, conversation_history: list = None) -> str:
        """
        Format the prompt with system message and conversation history

        Args:
            user_message: The user's question or prompt
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]

        Returns:
            Formatted prompt string
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        # Try to use chat template if available
        if hasattr(self.tokenizer, "apply_chat_template"):
            try:
                prompt = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                return prompt
            except Exception:
                pass

        # Fallback to manual formatting
        formatted = f"{self.system_prompt}\n\n"
        if conversation_history:
            for msg in conversation_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                formatted += f"{role}: {msg['content']}\n\n"
        formatted += f"User: {user_message}\n\nAssistant:"

        return formatted

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = None,
        temperature: float = None,
        top_p: float = None,
        top_k: int = None,
        conversation_history: list = None,
        **kwargs
    ) -> str:
        """
        Generate a response to the given prompt

        Args:
            prompt: User's input prompt
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (higher = more random)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            conversation_history: Previous conversation messages
            **kwargs: Additional generation parameters

        Returns:
            Generated response text
        """
        # Get parameters from env or use defaults
        max_new_tokens = max_new_tokens or int(os.getenv("MAX_NEW_TOKENS", 512))
        temperature = temperature or float(os.getenv("TEMPERATURE", 0.7))
        top_p = top_p or float(os.getenv("TOP_P", 0.9))
        top_k = top_k or int(os.getenv("TOP_K", 50))

        # Format prompt with system message
        formatted_prompt = self._format_prompt(prompt, conversation_history)

        # Tokenize
        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048,
        ).to(self.model.device)

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                **kwargs
            )

        # Decode and extract only the generated text
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Try to extract only the assistant's response
        if "Assistant:" in full_response:
            response = full_response.split("Assistant:")[-1].strip()
        else:
            # Fallback: remove the input prompt
            response = full_response[len(formatted_prompt):].strip()

        return response

    def chat(self):
        """Interactive chat session"""
        print("\n" + "="*60)
        print("CryptoLLM - Cryptocurrency Expert Assistant")
        print("="*60)
        print("Type 'quit' or 'exit' to end the conversation")
        print("Type 'clear' to reset conversation history")
        print("="*60 + "\n")

        conversation_history = []

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break

                if user_input.lower() == 'clear':
                    conversation_history = []
                    print("Conversation history cleared!")
                    continue

                # Generate response
                response = self.generate(user_input, conversation_history=conversation_history)

                # Update conversation history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})

                print(f"\nAssistant: {response}")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                continue


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="CryptoLLM - Cryptocurrency Expert Assistant")
    parser.add_argument(
        "--model",
        type=str,
        help="Model name or key (mistral-7b, phi-2, tinyllama, etc.)",
    )
    parser.add_argument(
        "--bits",
        type=int,
        choices=[4, 8],
        help="Quantization bits (4 or 8)",
    )
    parser.add_argument(
        "--max-memory",
        type=int,
        help="Maximum VRAM in GB",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Single prompt to generate (non-interactive mode)",
    )

    args = parser.parse_args()

    # Initialize model
    llm = CryptoLLM(
        model_name=args.model,
        quantization_bits=args.bits or 4,
        max_memory_gb=args.max_memory or 6,
    )

    # Single prompt mode or interactive chat
    if args.prompt:
        response = llm.generate(args.prompt)
        print(f"\nResponse: {response}")
    else:
        llm.chat()


if __name__ == "__main__":
    main()
