#!/usr/bin/env python3
"""
Cryptocurrency Trading Assistant
Specialized interface for trading analysis and signals
"""

from crypto_llm import CryptoLLM
from trading_knowledge import TRADING_STRATEGIES, TECHNICAL_INDICATORS
import argparse


class TradingAssistant:
    """AI-powered cryptocurrency trading assistant"""

    def __init__(self, model_name: str = None, use_finetuned: bool = False):
        """
        Initialize trading assistant

        Args:
            model_name: Base model or path to fine-tuned model
            use_finetuned: If True, assumes model_name is a fine-tuned model path
        """
        if use_finetuned and model_name:
            print(f"Loading fine-tuned trading model from: {model_name}")
        elif model_name:
            print(f"Loading base model: {model_name}")
        else:
            print("Loading default model for trading...")

        self.llm = CryptoLLM(
            model_name=model_name or "mistral-7b",
            quantization_bits=4,
        )

        # Trading-specific system prompt
        self.llm.system_prompt = """You are an expert cryptocurrency trading assistant with deep knowledge of:

- Technical analysis (chart patterns, indicators, price action)
- Risk management and position sizing
- Trading strategies (scalping, swing trading, trend following, etc.)
- Market psychology and sentiment analysis
- Crypto-specific trading concepts (funding rates, liquidations, etc.)

Provide practical, actionable trading advice. Always emphasize risk management.
IMPORTANT: Remind users this is educational only, not financial advice.
Always include proper stop losses and risk-reward ratios in trade ideas."""

    def analyze_market(self, coin: str, timeframe: str = "1D") -> str:
        """Get market analysis for a specific coin"""
        prompt = f"Provide a technical analysis for {coin} on the {timeframe} timeframe. Include key support/resistance levels, trend direction, and any notable patterns or indicators."

        return self.llm.generate(prompt, max_new_tokens=512)

    def get_trade_idea(self, coin: str, bias: str = "neutral") -> str:
        """Generate trade idea with entry, stop loss, and take profit"""
        prompt = f"Generate a trading plan for {coin} with a {bias} bias. Include:\n1. Entry price zone\n2. Stop loss level\n3. Take profit targets\n4. Risk-reward ratio\n5. Key invalidation levels\n\nProvide a complete trade setup."

        return self.llm.generate(prompt, max_new_tokens=512)

    def explain_indicator(self, indicator: str) -> str:
        """Explain how to use a technical indicator"""
        # Check if we have built-in info
        if indicator.upper() in TECHNICAL_INDICATORS:
            info = TECHNICAL_INDICATORS[indicator.upper()]
            context = f"Explain how to use {info['name']} for cryptocurrency trading in detail."
        else:
            context = f"Explain how to use {indicator} indicator for cryptocurrency trading."

        return self.llm.generate(context, max_new_tokens=512)

    def risk_check(self, entry: float, stop: float, position_size: float, account_size: float) -> str:
        """Check if a trade has proper risk management"""
        risk_amount = abs(entry - stop) * position_size
        risk_percent = (risk_amount / account_size) * 100

        prompt = f"""Evaluate this trade's risk management:
- Entry: ${entry}
- Stop Loss: ${stop}
- Position Size: {position_size} units
- Total Account: ${account_size}
- Risk Amount: ${risk_amount:.2f}
- Risk %: {risk_percent:.2f}%

Is this appropriate? Provide feedback on the risk management."""

        return self.llm.generate(prompt, max_new_tokens=256)

    def interactive_mode(self):
        """Run interactive trading assistant"""
        print("\n" + "="*60)
        print("Crypto Trading Assistant")
        print("="*60)
        print("Commands:")
        print("  analyze <COIN> - Market analysis")
        print("  trade <COIN> - Generate trade idea")
        print("  explain <INDICATOR> - Explain indicator")
        print("  strategies - List trading strategies")
        print("  quit - Exit")
        print("="*60 + "\n")

        while True:
            try:
                user_input = input("\n🔍 Trading Assistant: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit']:
                    print("Good luck with your trades!")
                    break

                # Parse commands
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()

                if command == "analyze" and len(parts) > 1:
                    coin = parts[1].upper()
                    print(f"\n📊 Analyzing {coin}...\n")
                    analysis = self.analyze_market(coin)
                    print(analysis)

                elif command == "trade" and len(parts) > 1:
                    coin = parts[1].upper()
                    print(f"\n💡 Generating trade idea for {coin}...\n")
                    trade = self.get_trade_idea(coin)
                    print(trade)

                elif command == "explain" and len(parts) > 1:
                    indicator = parts[1]
                    print(f"\n📖 Explaining {indicator}...\n")
                    explanation = self.explain_indicator(indicator)
                    print(explanation)

                elif command == "strategies":
                    print("\n📋 Available Trading Strategies:\n")
                    for name, info in TRADING_STRATEGIES.items():
                        print(f"• {info['name']}: {info['description']}")
                        print(f"  Risk: {info['risk_level']}\n")

                else:
                    # General question
                    print("\n💬 Assistant:\n")
                    response = self.llm.generate(user_input, max_new_tokens=512)
                    print(response)

            except KeyboardInterrupt:
                print("\n\nGood luck with your trades!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Crypto Trading Assistant")
    parser.add_argument(
        "--model",
        type=str,
        help="Model name or path to fine-tuned model",
    )
    parser.add_argument(
        "--finetuned",
        action="store_true",
        help="Use a fine-tuned model from local path",
    )
    parser.add_argument(
        "--analyze",
        type=str,
        help="Analyze a specific coin (e.g., BTC, ETH)",
    )
    parser.add_argument(
        "--trade",
        type=str,
        help="Generate trade idea for a coin",
    )

    args = parser.parse_args()

    # Initialize assistant
    assistant = TradingAssistant(
        model_name=args.model,
        use_finetuned=args.finetuned,
    )

    # Handle one-off commands
    if args.analyze:
        print(f"\n📊 Analyzing {args.analyze}...\n")
        analysis = assistant.analyze_market(args.analyze)
        print(analysis)
        return

    if args.trade:
        print(f"\n💡 Generating trade idea for {args.trade}...\n")
        trade = assistant.get_trade_idea(args.trade)
        print(trade)
        return

    # Interactive mode
    assistant.interactive_mode()


if __name__ == "__main__":
    main()
