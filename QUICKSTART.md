# Quick Start Guide

Get up and running with CryptoLLM in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- 6GB VRAM GPU (NVIDIA with CUDA) or CPU
- 10GB free disk space

## Installation

### Linux/Mac

```bash
# Clone the repository
git clone https://github.com/saikohs257/cannaflux.git
cd cannaflux

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

### Windows

```bash
# Clone the repository
git clone https://github.com/saikohs257/cannaflux.git
cd cannaflux

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
```

## First Run

### Option 1: Interactive Chat (Recommended)

```bash
python crypto_llm.py
```

This will:
1. Download the model (first time only, ~4-14GB)
2. Load it with 4-bit quantization
3. Start an interactive chat session

Example session:
```
You: What is Bitcoin?
Assistant: Bitcoin is a decentralized digital currency...

You: How does mining work?
Assistant: Bitcoin mining is the process...

You: quit
```

### Option 2: Web Interface

```bash
python web_interface.py
```

Then open your browser to: http://localhost:7860

### Option 3: Single Question

```bash
python crypto_llm.py --prompt "What is DeFi?"
```

## Choose Your Model

Different models for different needs:

### Best Quality (Recommended for 6GB VRAM)
```bash
python crypto_llm.py --model mistral-7b --bits 4
```

### Fastest Response
```bash
python crypto_llm.py --model phi-2 --bits 4
```

### Most Memory Efficient
```bash
python crypto_llm.py --model tinyllama --bits 4
```

## Common Commands

### Start interactive chat
```bash
python crypto_llm.py
```

### Ask a quick question
```bash
python crypto_llm.py --prompt "Explain smart contracts"
```

### Launch web UI
```bash
python web_interface.py
```

### Run examples
```bash
python examples/simple_question.py
python examples/batch_questions.py
python examples/compare_models.py
```

## Configuration

Edit `.env` to customize:

```env
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
QUANTIZATION_BITS=4
MAX_MEMORY_GB=6
MAX_NEW_TOKENS=512
TEMPERATURE=0.7
```

## Troubleshooting

### Out of Memory Error
```bash
# Use smaller model
python crypto_llm.py --model phi-2

# Or reduce max tokens
python crypto_llm.py --prompt "What is Bitcoin?" --max-tokens 256
```

### Slow Download
Model downloads can take time (4-14GB). First run will be slower while downloading.

### Import Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Try different models to find your favorite
3. Explore the example scripts in `examples/`
4. Customize generation parameters
5. Build your own crypto AI applications!

## Getting Help

- Check [README.md](README.md) for full documentation
- Review [models_config.json](models_config.json) for model details
- Open an issue on GitHub for bugs or questions

Happy learning about crypto! 🚀
