#!/usr/bin/env python3
"""
Prepare training data for crypto trading fine-tuning
Supports multiple data sources and formats
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict
from trading_knowledge import generate_trading_dataset, TRADING_QA_DATASET, RISK_MANAGEMENT_QA


def load_custom_data(file_path: str) -> List[Dict]:
    """Load custom training data from JSON/JSONL"""
    data = []
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.endswith('.jsonl'):
        with open(file_path, 'r') as f:
            for line in f:
                data.append(json.loads(line))
    else:
        with open(file_path, 'r') as f:
            loaded = json.load(f)
            if isinstance(loaded, list):
                data = loaded
            else:
                data = [loaded]

    return data


def format_alpaca_style(data: List[Dict]) -> List[Dict]:
    """Format data in Alpaca instruction style"""
    formatted = []

    for item in data:
        formatted_item = {}

        # Handle different input formats
        if 'instruction' in item:
            formatted_item['instruction'] = item['instruction']
            formatted_item['response'] = item.get('response', item.get('output', ''))
            formatted_item['input'] = item.get('input', '')
        elif 'question' in item:
            formatted_item['instruction'] = item['question']
            formatted_item['response'] = item['answer']
            formatted_item['input'] = ''
        elif 'prompt' in item:
            formatted_item['instruction'] = item['prompt']
            formatted_item['response'] = item.get('completion', item.get('response', ''))
            formatted_item['input'] = ''
        else:
            print(f"Warning: Skipping item with unknown format: {item.keys()}")
            continue

        formatted.append(formatted_item)

    return formatted


def create_market_analysis_dataset() -> List[Dict]:
    """Create dataset for market analysis training"""
    dataset = [
        {
            "instruction": "Analyze this market scenario: BTC is testing the 200-day MA after a 30% drop. Volume is increasing. What does this mean?",
            "response": "This is a critical moment that could signal a major reversal:\n\n**Bullish Signals:**\n- 200-day MA is a key long-term support level\n- Increasing volume shows strong interest at this level\n- After a 30% drop, many investors see value here\n\n**What to watch:**\n1. **Bounce confirmation**: Look for a strong daily close above the 200-MA\n2. **Volume**: Increasing buy volume would confirm demand\n3. **RSI**: Check if it's oversold (<30) for extra conviction\n4. **Market structure**: Is it making higher lows?\n\n**Trading approach:**\n- **Conservative**: Wait for confirmation (2-3 daily closes above 200-MA)\n- **Aggressive**: Small position here with tight stop below 200-MA\n- **Stop loss**: 3-5% below 200-MA\n- **Targets**: Previous resistance levels from the downtrend\n\n**Risk**: If 200-MA breaks with volume, expect further downside to next support.",
        },
        {
            "instruction": "How do I trade a bull flag pattern in cryptocurrency?",
            "response": "A **bull flag** is a continuation pattern that often leads to explosive moves:\n\n**Pattern Structure:**\n1. **Pole**: Sharp price increase (the flagpole)\n2. **Flag**: Consolidation/pullback in parallel channel\n3. **Breakout**: Price breaks above flag resistance\n\n**How to Trade It:**\n\n**Entry Points:**\n- **Aggressive**: Buy within the flag consolidation at support\n- **Conservative**: Wait for breakout above flag resistance with volume\n\n**Target Calculation:**\nMeasure the flagpole height and add it to the breakout point\n- If pole = 20%, target = breakout + 20%\n\n**Stop Loss:**\n- Below flag support (for entries in the flag)\n- Below breakout level (for breakout entries)\n- Typically 5-8% depending on volatility\n\n**Confirmation Signals:**\n✅ Increasing volume on breakout (crucial!)\n✅ Flag duration: 1-3 weeks ideal\n✅ Pole should be strong and nearly vertical\n✅ Flag should retrace 38-50% of pole\n\n**Example:**\n- BTC pumps from $40k to $48k (pole = $8k)\n- Consolidates in $45k-$47k range (flag)\n- Breaks above $47k with volume\n- Target: $47k + $8k = $55k\n\n**Failure Signs:**\n❌ Breakout without volume = false breakout\n❌ Flag lasts too long (>4 weeks)\n❌ Breaks below flag support = pattern invalidated",
        },
    ]
    return dataset


def create_risk_management_dataset() -> List[Dict]:
    """Create dataset focused on risk management"""
    dataset = [
        {
            "instruction": "I'm down 40% on a trade. Should I hold and wait for recovery or cut losses?",
            "response": "**Cut the loss immediately.** Here's why:\n\n**The Math Problem:**\n- Down 40% means you need +66% just to break even\n- Down 50% requires +100% to recover\n- The deeper the loss, the harder the recovery\n\n**Why Holding is Dangerous:**\n1. **Opportunity cost**: Capital is locked in a losing trade\n2. **Emotional damage**: Stress affects future decisions\n3. **No guarantee**: Price may never return\n4. **Averaging down**: Throwing good money after bad\n\n**What You Should Have Done:**\n- Set stop loss at 5-10% loss maximum\n- Exit when trade thesis is invalidated\n- Accept small losses as part of trading\n\n**What To Do Now:**\n1. **Exit immediately** - Don't wait for 'just a small bounce'\n2. **Take a break** - Clear your head\n3. **Review what went wrong** - Learn from it\n4. **Start fresh** with proper risk management\n\n**Key Principle:**\n'Cut losses short, let winners run' - not the opposite.\n\n**Going Forward:**\n- Never let a trade go -40%\n- Use hard stop losses (not mental)\n- Risk only 1-2% per trade\n- If you violate your rules, stop trading until you can follow them\n\nRecovering from -40% is possible, but starting fresh with discipline is often faster and healthier.",
        },
    ]
    return dataset


def merge_datasets(datasets: List[List[Dict]]) -> List[Dict]:
    """Merge multiple datasets"""
    merged = []
    for dataset in datasets:
        merged.extend(dataset)
    return merged


def validate_dataset(data: List[Dict]) -> bool:
    """Validate dataset format"""
    if not data:
        print("Error: Dataset is empty")
        return False

    required_fields = ['instruction', 'response']

    for i, item in enumerate(data):
        for field in required_fields:
            if field not in item or not item[field]:
                print(f"Error: Item {i} missing required field '{field}'")
                return False

    print(f"✓ Dataset validation passed: {len(data)} examples")
    return True


def split_dataset(data: List[Dict], train_ratio: float = 0.9):
    """Split dataset into train and validation sets"""
    import random

    random.shuffle(data)
    split_idx = int(len(data) * train_ratio)

    train_data = data[:split_idx]
    val_data = data[split_idx:]

    return train_data, val_data


def main():
    parser = argparse.ArgumentParser(description="Prepare crypto trading training data")
    parser.add_argument(
        "--output",
        type=str,
        default="./datasets/crypto_trading_data.json",
        help="Output file for training data",
    )
    parser.add_argument(
        "--custom-data",
        type=str,
        nargs="+",
        help="Additional custom data files to include",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Split into train and validation sets",
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.1,
        help="Validation set ratio (default: 0.1)",
    )

    args = parser.parse_args()

    print("="*60)
    print("Preparing Crypto Trading Training Data")
    print("="*60 + "\n")

    # Collect all datasets
    datasets = []

    # Built-in trading dataset
    print("Loading built-in trading knowledge...")
    datasets.append(TRADING_QA_DATASET)
    datasets.append(RISK_MANAGEMENT_QA)
    datasets.append(create_market_analysis_dataset())
    datasets.append(create_risk_management_dataset())

    # Custom data files
    if args.custom_data:
        for file_path in args.custom_data:
            print(f"Loading custom data from {file_path}...")
            try:
                custom_data = load_custom_data(file_path)
                datasets.append(custom_data)
                print(f"  Loaded {len(custom_data)} examples")
            except Exception as e:
                print(f"  Error loading {file_path}: {e}")

    # Merge all datasets
    print("\nMerging datasets...")
    merged_data = merge_datasets(datasets)

    # Format data
    print("Formatting data...")
    formatted_data = format_alpaca_style(merged_data)

    # Validate
    print("Validating dataset...")
    if not validate_dataset(formatted_data):
        return

    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Split if requested
    if args.split:
        print(f"\nSplitting dataset (train: {1-args.val_ratio:.0%}, val: {args.val_ratio:.0%})...")
        train_data, val_data = split_dataset(formatted_data, 1 - args.val_ratio)

        # Save train set
        train_file = output_path.parent / f"{output_path.stem}_train.json"
        with open(train_file, 'w') as f:
            json.dump(train_data, f, indent=2)
        print(f"  Train set: {len(train_data)} examples → {train_file}")

        # Save validation set
        val_file = output_path.parent / f"{output_path.stem}_val.json"
        with open(val_file, 'w') as f:
            json.dump(val_data, f, indent=2)
        print(f"  Validation set: {len(val_data)} examples → {val_file}")
    else:
        # Save combined dataset
        with open(output_path, 'w') as f:
            json.dump(formatted_data, f, indent=2)
        print(f"\nSaved {len(formatted_data)} examples to {output_path}")

    print("\n" + "="*60)
    print("Data Preparation Complete!")
    print("="*60)
    print(f"\nTo fine-tune the model, run:")
    if args.split:
        print(f"  python finetune.py --dataset {train_file}")
    else:
        print(f"  python finetune.py --dataset {output_path}")


if __name__ == "__main__":
    main()
