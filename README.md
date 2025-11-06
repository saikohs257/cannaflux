# 🪙 CryptoLLM - Cryptocurrency Expert AI Assistant

A specialized language model focused on cryptocurrency knowledge, optimized to run on consumer GPUs with **6GB VRAM**.

## Features

- 🎯 **Cryptocurrency-Focused**: Specialized knowledge about blockchain, DeFi, NFTs, trading, and more
- 💾 **Memory Efficient**: Optimized for 6GB VRAM using 4-bit quantization
- 🚀 **Multiple Models**: Choose between Mistral 7B, Phi-2, TinyLlama, and more
- 💬 **Interactive Interfaces**: CLI chat and web-based Gradio UI
- 🔧 **Customizable**: Adjustable generation parameters and model options
- 📚 **Built-in Knowledge Base**: Cryptocurrency glossary, Q&A pairs, and example prompts
- 📈 **Trading Assistant**: Specialized mode for technical analysis and trade ideas
- 🎓 **Fine-tuning Support**: Train on your own trading strategies with LoRA/PEFT
- 💹 **Trading Knowledge**: Technical indicators, chart patterns, risk management

## Quick Start

### Prerequisites

- Python 3.8+
- CUDA-capable GPU with 6GB VRAM (or CPU for smaller models)
- 10GB+ free disk space for model downloads

### Installation

1. Clone the repository:
```bash
git clone https://github.com/saikohs257/cannaflux.git
cd cannaflux
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure settings (optional):
```bash
cp .env.example .env
# Edit .env with your preferences
```

## Usage

### 1. Interactive Chat (CLI)

Simple command-line chat interface:

```bash
python crypto_llm.py
```

With options:
```bash
python crypto_llm.py --model mistral-7b --bits 4
```

### 2. Web Interface (Gradio)

Launch the web UI for a better experience:

```bash
python web_interface.py
```

Then open your browser to `http://localhost:7860`

### 3. Single Question

Quick one-off questions:

```bash
python crypto_llm.py --prompt "What is Bitcoin?"
```

### 4. Python API

Use in your own scripts:

```python
from crypto_llm import CryptoLLM

# Initialize the model
llm = CryptoLLM(
    model_name="mistral-7b",
    quantization_bits=4,
    max_memory_gb=6,
)

# Generate a response
response = llm.generate(
    "Explain what DeFi is",
    max_new_tokens=512,
    temperature=0.7,
)

print(response)
```

## Supported Models

| Model | Size | 4-bit VRAM | 8-bit VRAM | Speed | Quality | Best For |
|-------|------|-----------|-----------|-------|---------|----------|
| **Mistral 7B** | 7B | ~4.5GB | ~7.5GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Recommended** - Best balance |
| **Phi-2** | 2.7B | ~2.0GB | ~3.0GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Fast responses |
| **TinyLlama** | 1.1B | ~1.0GB | ~1.5GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Low resource |
| **Zephyr 7B** | 7B | ~4.5GB | ~7.5GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Safe, helpful responses |
| **Llama 2 7B** | 7B | ~4.3GB | ~7.2GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | General purpose |

### Model Selection

Choose a model based on your needs:

```bash
# Recommended: Best quality for 6GB
python crypto_llm.py --model mistral-7b --bits 4

# Fastest: Quick responses
python crypto_llm.py --model phi-2 --bits 4

# Most efficient: Minimal resources
python crypto_llm.py --model tinyllama --bits 4
```

## Examples

The `examples/` directory contains sample scripts:

### Simple Question
```bash
python examples/simple_question.py
```

### Batch Processing
Process multiple questions efficiently:
```bash
python examples/batch_questions.py
```

### Model Comparison
Compare responses from different models:
```bash
python examples/compare_models.py
```

## 📈 Trading Features

### Trading Assistant

Specialized mode for cryptocurrency trading analysis:

```bash
# Interactive trading assistant
python trading_assistant.py

# Analyze a specific coin
python trading_assistant.py --analyze BTC

# Generate trade idea
python trading_assistant.py --trade ETH
```

**Features:**
- Technical analysis with support/resistance levels
- Trade setup generation (entry, stop loss, take profit)
- Risk management calculations
- Indicator explanations
- Strategy recommendations

### Fine-tuning for Trading

**Train the model on YOUR trading strategies!**

```bash
# Step 1: Generate example dataset
python trading_knowledge.py

# Step 2: Prepare your training data
python prepare_training_data.py --output datasets/my_trades.json --split

# Step 3: Fine-tune the model
python finetune.py --dataset datasets/my_trades_train.json --output ./my_trading_model

# Step 4: Use your custom model
python trading_assistant.py --model ./my_trading_model --finetuned
```

**What you can teach it:**
- ✅ Your trading strategies and rules
- ✅ Market analysis techniques
- ✅ Risk management principles
- ✅ Pattern recognition
- ✅ Your trading journal insights

**See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for complete fine-tuning instructions.**

### Can It Learn to Trade Autonomously?

**Fine-tuning teaches it ABOUT trading** (explaining strategies, analyzing markets).

**For autonomous trading**, you would need:
- Reinforcement learning (not just fine-tuning)
- Live market data integration
- Order execution system
- Extensive backtesting

Our fine-tuning creates an **AI trading mentor**, not an autonomous trading bot.

## Knowledge Base

CryptoLLM covers a wide range of cryptocurrency topics:

### Core Topics

- **Blockchain Basics**: Bitcoin, Ethereum, consensus mechanisms
- **DeFi**: DEXs, liquidity pools, yield farming, lending protocols
- **NFTs**: Standards, marketplaces, use cases
- **Trading**: Technical analysis, market dynamics, order types
- **Security**: Wallets, private keys, best practices
- **Development**: Smart contracts, Web3, dApp development
- **Economics**: Tokenomics, market cap, supply dynamics

### Example Questions

```python
from crypto_knowledge import CRYPTO_PROMPTS

# Get questions by category
basics = CRYPTO_PROMPTS["basics"]
defi = CRYPTO_PROMPTS["defi"]
trading = CRYPTO_PROMPTS["trading"]
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# Model Configuration
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
QUANTIZATION_BITS=4
MAX_MEMORY_GB=6
DEVICE=cuda

# Generation Parameters
MAX_NEW_TOKENS=512
TEMPERATURE=0.7
TOP_P=0.9
TOP_K=50

# Server Configuration (for web interface)
HOST=0.0.0.0
PORT=7860
```

### Generation Parameters

- **Temperature** (0.1-1.5): Higher = more creative, Lower = more focused
  - Use 0.3-0.5 for factual answers
  - Use 0.7-1.0 for creative explanations

- **Max Tokens** (128-1024): Maximum length of response
  - 256: Short answers
  - 512: Standard responses (recommended)
  - 1024: Long, detailed explanations

- **Top P** (0.1-1.0): Nucleus sampling
  - 0.9: Good balance (recommended)
  - Lower: More focused on likely words

- **Top K** (1-100): Limits vocabulary per step
  - 50: Good default
  - Higher: More diverse vocabulary

## Performance Tips

### Optimize for 6GB VRAM

1. **Use 4-bit quantization** for 7B models
2. **Close other GPU applications** before running
3. **Reduce max_new_tokens** if you hit OOM errors
4. **Use smaller models** (Phi-2, TinyLlama) if needed

### Speed vs Quality Trade-offs

```python
# Fastest (lower quality)
llm = CryptoLLM(model_name="tinyllama", quantization_bits=4)

# Balanced (recommended)
llm = CryptoLLM(model_name="mistral-7b", quantization_bits=4)

# Highest quality (requires 8GB VRAM)
llm = CryptoLLM(model_name="mistral-7b", quantization_bits=8)
```

### Batch Processing

For multiple questions, reuse the same model instance:

```python
llm = CryptoLLM(model_name="mistral-7b")

for question in questions:
    response = llm.generate(question)
    # Process response
```

## Troubleshooting

### Out of Memory (OOM) Errors

1. Use 4-bit quantization instead of 8-bit
2. Reduce `max_new_tokens` to 256 or less
3. Switch to a smaller model (Phi-2 or TinyLlama)
4. Close other GPU applications
5. Try CPU mode (slower): `DEVICE=cpu`

### Model Download Issues

Models are downloaded from HuggingFace on first use:

- **Mistral 7B**: ~14GB download
- **Phi-2**: ~5.5GB download
- **TinyLlama**: ~2.2GB download

Ensure you have enough disk space and a stable internet connection.

### Slow Generation

- First generation is slower (model loading)
- Subsequent generations are faster
- Use smaller models for faster responses
- Reduce `max_new_tokens`

## Architecture

```
cannaflux/
├── crypto_llm.py                    # Main LLM class and CLI
├── crypto_knowledge.py              # General crypto knowledge base
├── trading_knowledge.py             # Trading-specific knowledge and datasets
├── web_interface.py                 # Gradio web UI
├── trading_assistant.py             # Trading-focused interface
├── finetune.py                      # Fine-tuning script (LoRA/PEFT)
├── prepare_training_data.py         # Dataset preparation tool
├── models_config.json               # Model specifications
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── setup.sh                         # Setup script
├── README.md                        # Main documentation
├── TRAINING_GUIDE.md                # Fine-tuning guide
├── QUICKSTART.md                    # Quick start guide
├── LICENSE                          # MIT license
├── examples/                        # Example scripts
│   ├── simple_question.py
│   ├── batch_questions.py
│   └── compare_models.py
└── datasets/                        # Training datasets
    ├── crypto_trading_complete_train.json
    └── crypto_trading_complete_val.json
```

## Advanced Usage

### Custom System Prompt

```python
llm = CryptoLLM(model_name="mistral-7b")
llm.system_prompt = "You are a Bitcoin maximalist..."
```

### Conversation History

```python
history = [
    {"role": "user", "content": "What is Bitcoin?"},
    {"role": "assistant", "content": "Bitcoin is..."},
]

response = llm.generate(
    "Tell me more about mining",
    conversation_history=history
)
```

### Fine-tuning (Advanced)

Train the model on your own cryptocurrency trading data:

```bash
# Prepare your training dataset
python prepare_training_data.py \
  --custom-data my_strategies.json \
  --output datasets/my_data.json \
  --split

# Fine-tune the model
python finetune.py \
  --dataset datasets/my_data_train.json \
  --output ./my_custom_model \
  --epochs 3

# Use your fine-tuned model
python crypto_llm.py --model ./my_custom_model
```

**See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for complete instructions on:**
- Creating training datasets
- Fine-tuning parameters
- Best practices
- Trading-specific fine-tuning
- Autonomous trading considerations

## Contributing

Contributions are welcome! Areas for improvement:

- Additional cryptocurrency knowledge and datasets
- Trading strategies and technical analysis examples
- Fine-tuning datasets for different trading styles
- Support for more models
- API server implementation
- Reinforcement learning for autonomous trading
- Mobile/web deployment guides

## Disclaimer

⚠️ **Important**: This AI assistant provides educational information only.

- Always do your own research (DYOR)
- Never treat AI responses as financial advice
- Cryptocurrency investments carry significant risk
- Verify critical information from official sources
- The AI may make mistakes or provide outdated information

## License

MIT License - See LICENSE file for details

## Resources

- [HuggingFace Models](https://huggingface.co/models)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [Quantization Guide](https://huggingface.co/docs/transformers/main_classes/quantization)
- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Ethereum Documentation](https://ethereum.org/en/developers/docs/)

## Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing issues for solutions
- Contribute improvements via pull requests

---

Built with ❤️ for the crypto community
