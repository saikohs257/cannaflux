#!/usr/bin/env python3
"""
Fine-tuning script for CryptoLLM using LoRA/PEFT
Train the model on custom cryptocurrency trading data
"""

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from trl import SFTTrainer
import argparse


class CryptoFineTuner:
    """Fine-tune LLM for cryptocurrency trading"""

    def __init__(
        self,
        model_name: str = "mistralai/Mistral-7B-Instruct-v0.2",
        dataset_path: str = None,
        output_dir: str = "./crypto_trading_model",
        quantization_bits: int = 4,
    ):
        self.model_name = model_name
        self.dataset_path = dataset_path
        self.output_dir = output_dir
        self.quantization_bits = quantization_bits

        self.model = None
        self.tokenizer = None
        self.peft_model = None

    def load_model(self):
        """Load base model with quantization"""
        print(f"Loading base model: {self.model_name}")

        # Quantization config
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=(self.quantization_bits == 4),
            load_in_8bit=(self.quantization_bits == 8),
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print("Model loaded successfully!")

    def prepare_for_training(self):
        """Prepare model for k-bit training"""
        print("Preparing model for training...")

        self.model = prepare_model_for_kbit_training(self.model)

        # LoRA configuration
        lora_config = LoraConfig(
            r=16,  # LoRA rank
            lora_alpha=32,  # LoRA alpha
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        )

        # Get PEFT model
        self.peft_model = get_peft_model(self.model, lora_config)
        self.peft_model.print_trainable_parameters()

    def load_dataset(self):
        """Load and prepare training dataset"""
        print(f"Loading dataset from: {self.dataset_path}")

        if self.dataset_path.endswith('.json') or self.dataset_path.endswith('.jsonl'):
            dataset = load_dataset('json', data_files=self.dataset_path, split='train')
        elif os.path.isdir(self.dataset_path):
            dataset = load_dataset(self.dataset_path, split='train')
        else:
            raise ValueError(f"Unsupported dataset format: {self.dataset_path}")

        print(f"Dataset loaded: {len(dataset)} examples")
        return dataset

    def format_instruction(self, sample):
        """Format training samples as instructions"""
        if "instruction" in sample and "response" in sample:
            return f"""### Instruction:
{sample['instruction']}

### Response:
{sample['response']}"""
        elif "question" in sample and "answer" in sample:
            return f"""### Question:
{sample['question']}

### Answer:
{sample['answer']}"""
        elif "text" in sample:
            return sample["text"]
        else:
            raise ValueError("Dataset must contain 'instruction'/'response' or 'question'/'answer' or 'text' fields")

    def train(
        self,
        num_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 2e-4,
        max_seq_length: int = 2048,
    ):
        """Train the model"""
        print("\n" + "="*60)
        print("Starting Fine-Tuning")
        print("="*60 + "\n")

        # Load dataset
        dataset = self.load_dataset()

        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=learning_rate,
            fp16=True,
            save_strategy="epoch",
            logging_steps=10,
            optim="paged_adamw_8bit",
            warmup_ratio=0.05,
            lr_scheduler_type="cosine",
            save_total_limit=2,
            report_to="none",
        )

        # Create trainer
        trainer = SFTTrainer(
            model=self.peft_model,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            args=training_args,
            max_seq_length=max_seq_length,
            formatting_func=self.format_instruction,
            packing=False,
        )

        # Train
        print("Training started...")
        trainer.train()

        # Save model
        print(f"\nSaving model to {self.output_dir}")
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)

        print("\n" + "="*60)
        print("Training Complete!")
        print("="*60)
        print(f"\nModel saved to: {self.output_dir}")
        print(f"To use the fine-tuned model:")
        print(f'  python crypto_llm.py --model {self.output_dir}')

    def run(self, **training_kwargs):
        """Run the complete fine-tuning process"""
        self.load_model()
        self.prepare_for_training()
        self.train(**training_kwargs)


def main():
    parser = argparse.ArgumentParser(
        description="Fine-tune CryptoLLM on trading data"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="mistralai/Mistral-7B-Instruct-v0.2",
        help="Base model to fine-tune",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to training dataset (JSON/JSONL file or directory)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./crypto_trading_model",
        help="Output directory for fine-tuned model",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Training batch size",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-4,
        help="Learning rate",
    )
    parser.add_argument(
        "--bits",
        type=int,
        choices=[4, 8],
        default=4,
        help="Quantization bits",
    )

    args = parser.parse_args()

    # Create fine-tuner
    finetuner = CryptoFineTuner(
        model_name=args.model,
        dataset_path=args.dataset,
        output_dir=args.output,
        quantization_bits=args.bits,
    )

    # Run training
    finetuner.run(
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
    )


if __name__ == "__main__":
    main()
