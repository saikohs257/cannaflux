# Training Guide - Fine-tune CryptoLLM for Trading

This guide shows you how to **fine-tune** CryptoLLM on your own cryptocurrency trading data, making it learn your specific trading strategies and knowledge.

## 🎯 What is Fine-tuning?

Fine-tuning adapts a pre-trained model to your specific use case by training it on custom data. For crypto trading, this means:

- ✅ **Teaching it your trading strategies**
- ✅ **Learning from your market analysis**
- ✅ **Understanding your risk management rules**
- ✅ **Memorizing trading patterns you care about**

## 🔧 Two Types of Training

### 1. **Fine-tuning (LoRA/PEFT)** - What we support ✅
- Trains the model on text-based trading knowledge
- Learns to explain strategies, analyze markets, answer questions
- Memory-efficient, works on 6GB VRAM
- Best for: Trading education, strategy explanations, market analysis

### 2. **Reinforcement Learning** - For actual trading 🚀
- Trains model to make real trading decisions
- Learns from profit/loss feedback
- Requires market simulation environment
- Best for: Autonomous trading bots
- ⚠️ **Not included** - requires much more complex setup

**This guide covers #1 (Fine-tuning)** - teaching the LLM about trading concepts.

## 📊 Quick Start

### Step 1: Prepare Your Data

We've included example trading datasets. Generate them:

```bash
# Generate built-in trading dataset
python trading_knowledge.py

# Or prepare a complete dataset with train/validation split
python prepare_training_data.py --output datasets/my_trading_data.json --split
```

This creates training data in the correct format.

### Step 2: Fine-tune the Model

```bash
python finetune.py \
  --dataset datasets/crypto_trading_complete_train.json \
  --output ./my_trading_model \
  --epochs 3 \
  --batch-size 4
```

**This will:**
- Download the base model (first time only)
- Apply LoRA adapters for efficient training
- Train for 3 epochs
- Save the fine-tuned model

**Training time**: 30min - 2 hours depending on GPU and dataset size

### Step 3: Use Your Fine-tuned Model

```bash
# Interactive chat
python crypto_llm.py --model ./my_trading_model

# Trading assistant
python trading_assistant.py --model ./my_trading_model --finetuned

# Web interface
python web_interface.py
# Then select your model path in the UI
```

## 📝 Creating Training Data

### Format Requirements

Training data must be in JSON format with `instruction` and `response` fields:

```json
[
  {
    "instruction": "How do I trade a bull flag pattern?",
    "response": "A bull flag is a continuation pattern..."
  },
  {
    "instruction": "What's a good risk-reward ratio?",
    "response": "Aim for at least 1:2 or higher..."
  }
]
```

### Data Sources

**1. Your Own Trading Knowledge**
Create a file `my_data.json` with your strategies:

```json
[
  {
    "instruction": "Explain my EMA crossover strategy",
    "response": "This strategy uses 20 and 50 EMA crosses. When 20 crosses above 50, enter long..."
  },
  {
    "instruction": "What are my rules for position sizing?",
    "response": "Never risk more than 2% per trade. Calculate position size as..."
  }
]
```

**2. Trading Journals**
Convert your trading notes into Q&A format:

```json
{
  "instruction": "Why did the BTC trade on 2024-01-15 succeed?",
  "response": "The trade worked because we entered after a confirmed breakout with volume confirmation. The 3:1 RR setup gave us good profit potential..."
}
```

**3. Market Analysis**
Your technical analysis can become training data:

```json
{
  "instruction": "Analyze BTC consolidation between $40k-$42k",
  "response": "This is a bullish consolidation pattern. Volume is decreasing, indicating smart money accumulation. Watch for breakout above $42k with volume..."
}
```

**4. Web Scraping** (Advanced)
- Scrape crypto trading forums, Twitter, Reddit
- Clean and format into instruction-response pairs
- ⚠️ Verify quality - garbage in, garbage out!

### Use the Data Preparation Script

```bash
# Combine multiple data sources
python prepare_training_data.py \
  --custom-data my_strategies.json trading_journal.json market_analysis.json \
  --output datasets/combined_data.json \
  --split
```

This will:
- Merge all your data sources
- Add built-in trading knowledge
- Format everything correctly
- Split into train (90%) and validation (10%)

## 🎓 Training Options

### Basic Training

```bash
python finetune.py --dataset datasets/my_data.json
```

### Advanced Training

```bash
python finetune.py \
  --model mistralai/Mistral-7B-Instruct-v0.2 \
  --dataset datasets/trading_data.json \
  --output ./crypto_trader_v1 \
  --epochs 5 \
  --batch-size 4 \
  --learning-rate 2e-4 \
  --bits 4
```

**Parameters explained:**

- `--model`: Base model to fine-tune (default: Mistral 7B)
- `--dataset`: Your training data file
- `--output`: Where to save fine-tuned model
- `--epochs`: Number of training passes (3-5 recommended)
- `--batch-size`: Samples per batch (4 for 6GB VRAM)
- `--learning-rate`: How fast to learn (2e-4 is safe)
- `--bits`: Quantization (4 for 6GB VRAM)

### Different Base Models

```bash
# Fastest training - Phi-2
python finetune.py --model microsoft/phi-2 --dataset my_data.json

# Best quality - Mistral 7B (recommended)
python finetune.py --model mistralai/Mistral-7B-Instruct-v0.2 --dataset my_data.json

# Most efficient - TinyLlama
python finetune.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --dataset my_data.json
```

## 📈 Monitoring Training

During training, you'll see:

```
Epoch 1/3
Training... 100%
Loss: 0.85 -> 0.42

Epoch 2/3
Training... 100%
Loss: 0.42 -> 0.28

Saving model to ./my_trading_model
```

**Good signs:**
- ✅ Loss steadily decreasing
- ✅ No crashes or errors
- ✅ Completion within expected time

**Warning signs:**
- ❌ Loss increasing or not changing
- ❌ Out of memory errors
- ❌ Taking way too long

### If Training Fails

**Out of Memory:**
```bash
# Reduce batch size
python finetune.py --dataset my_data.json --batch-size 2

# Or use smaller model
python finetune.py --model phi-2 --dataset my_data.json
```

**Loss not decreasing:**
- Check data quality
- Try different learning rate (1e-4 or 3e-4)
- Increase epochs
- Ensure data format is correct

## 🎯 What Can You Teach It?

### Trading Strategies
```json
{
  "instruction": "Explain the Bollinger Bands squeeze strategy",
  "response": "The squeeze happens when bands tighten due to low volatility. It precedes explosive moves. When bands squeeze tight, prepare for breakout. Enter when price breaks upper/lower band with volume confirmation..."
}
```

### Risk Management
```json
{
  "instruction": "How should I size my positions?",
  "response": "Use the formula: Position Size = (Account × Risk%) / (Entry - Stop). For a $10k account risking 2%, that's $200. If entry is $100 and stop is $95, position = $200 / $5 = 40 units..."
}
```

### Market Analysis
```json
{
  "instruction": "How do you identify market tops?",
  "response": "Look for: 1) Extreme greed in sentiment, 2) Parabolic price action, 3) Volume divergence, 4) Everyone talking about crypto, 5) Your barber giving you trading advice..."
}
```

### Crypto-Specific Knowledge
```json
{
  "instruction": "What are funding rates and how to trade them?",
  "response": "Funding rates are periodic payments between long/short traders. Positive rate (longs pay shorts) = bullish sentiment, negative = bearish. Extreme rates (>0.1%) often precede reversals..."
}
```

## 📊 Training Data Quality

### Good Training Data
✅ Clear, specific questions
✅ Detailed, accurate responses
✅ Consistent formatting
✅ Diverse examples (not repetitive)
✅ Correct information

### Bad Training Data
❌ Vague questions
❌ Short, unhelpful responses
❌ Inconsistent format
❌ Duplicates
❌ False information

### Example - Good vs Bad

**❌ Bad:**
```json
{
  "instruction": "trading",
  "response": "use stops"
}
```

**✅ Good:**
```json
{
  "instruction": "What are the key principles of successful day trading in cryptocurrency?",
  "response": "Successful crypto day trading requires: 1) Strict risk management - never risk more than 1-2% per trade, 2) Clear entry/exit rules based on technical analysis, 3) Emotional discipline to follow your plan, 4) Understanding of market structure and liquidity, 5) Proper position sizing based on volatility..."
}
```

## 🚀 Advanced: Can It Learn to Trade Autonomously?

**Short answer: Not with just fine-tuning.**

**What fine-tuning teaches:**
- Explaining trading concepts ✅
- Analyzing chart patterns ✅
- Discussing strategies ✅
- Answering trading questions ✅

**What it DOESN'T teach:**
- Making real-time trading decisions ❌
- Learning from profit/loss ❌
- Adapting to live markets ❌
- Executing trades autonomously ❌

### For Autonomous Trading, You Need:

**1. Reinforcement Learning (RL)**
- Model learns from rewards (profit) and penalties (loss)
- Requires simulation environment
- Much more complex than fine-tuning
- Not included in this project (yet!)

**2. Live Market Integration**
- Real-time data feeds
- Exchange API connections
- Order execution system
- Risk management guardrails

**3. Backtesting Framework**
- Historical market simulation
- Performance metrics
- Strategy validation

### Our Recommendation:

**Start with fine-tuning** to create a smart trading assistant that:
- Answers your trading questions
- Explains strategies clearly
- Helps with analysis
- Serves as your "AI trading mentor"

**Then later**, if you want autonomous trading:
- Use the fine-tuned model as a component
- Build RL training on top
- Add proper backtesting
- Start with paper trading
- Only use real money after extensive testing

## 📚 Example Workflows

### Workflow 1: Learn Your Trading Style

1. Keep a trading journal for 1-2 months
2. Convert successful trades to Q&A format
3. Add your analysis for each trade
4. Fine-tune model on your journal
5. Now you have an AI that thinks like you!

### Workflow 2: Strategy Encyclopedia

1. Collect trading strategies you like
2. Document each strategy in detail
3. Create instruction-response pairs
4. Fine-tune model
5. Use it to quickly recall strategies

### Workflow 3: Market Analysis Assistant

1. Gather your technical analysis notes
2. Format as market scenario Q&A
3. Add pattern recognition examples
4. Fine-tune model
5. Use for analyzing new market situations

## 🎓 Learning Resources

**Fine-tuning Basics:**
- [Hugging Face PEFT Docs](https://huggingface.co/docs/peft)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

**Trading Knowledge:**
- Add your favorite trading education resources
- Document what works for YOU
- That's what makes your model unique!

**Reinforcement Learning (for autonomous trading):**
- [Stable Baselines3](https://stable-baselines3.readthedocs.io/)
- [OpenAI Gym](https://www.gymlibrary.dev/)
- Note: Much more advanced, separate project

## ⚠️ Important Disclaimers

1. **Not Financial Advice**: This tool is for education only
2. **No Guarantees**: Past performance doesn't predict future results
3. **Risk Management**: Always use stop losses and proper position sizing
4. **Start Small**: Test thoroughly before using real capital
5. **Keep Learning**: Markets change, keep updating your knowledge

## 🤝 Contributing Training Data

Want to share your datasets? Consider:
- Anonymizing personal trade details
- Removing specific prices/dates
- Keeping strategies generic enough to be useful to others
- Contributing back to help the community!

---

**Ready to train?** Start with the built-in dataset, then add your own knowledge!

```bash
# Generate sample dataset
python prepare_training_data.py --output datasets/starter.json --split

# Fine-tune
python finetune.py --dataset datasets/starter_train.json

# Test it
python trading_assistant.py --model ./crypto_trading_model --finetuned
```

Happy training! 🚀
