"""
Cryptocurrency trading knowledge base and datasets
"""

# Trading strategies and concepts
TRADING_STRATEGIES = {
    "trend_following": {
        "name": "Trend Following",
        "description": "Trading in the direction of the prevailing market trend",
        "indicators": ["Moving Averages", "MACD", "ADX"],
        "timeframes": ["4H", "1D", "1W"],
        "risk_level": "Medium",
    },
    "mean_reversion": {
        "name": "Mean Reversion",
        "description": "Trading based on price returning to average levels",
        "indicators": ["Bollinger Bands", "RSI", "Stochastic"],
        "timeframes": ["15m", "1H", "4H"],
        "risk_level": "Medium-High",
    },
    "breakout": {
        "name": "Breakout Trading",
        "description": "Trading price breaks through support/resistance levels",
        "indicators": ["Volume", "Support/Resistance", "ATR"],
        "timeframes": ["1H", "4H", "1D"],
        "risk_level": "High",
    },
    "scalping": {
        "name": "Scalping",
        "description": "Quick trades for small profits on short timeframes",
        "indicators": ["Level 2 Order Book", "Volume Profile", "EMA"],
        "timeframes": ["1m", "5m", "15m"],
        "risk_level": "Very High",
    },
    "swing_trading": {
        "name": "Swing Trading",
        "description": "Holding positions for days to weeks to capture swings",
        "indicators": ["Fibonacci", "Moving Averages", "RSI"],
        "timeframes": ["4H", "1D", "1W"],
        "risk_level": "Medium",
    },
}

# Technical indicators
TECHNICAL_INDICATORS = {
    "RSI": {
        "name": "Relative Strength Index",
        "type": "Momentum Oscillator",
        "range": "0-100",
        "overbought": 70,
        "oversold": 30,
        "use_case": "Identify overbought/oversold conditions",
    },
    "MACD": {
        "name": "Moving Average Convergence Divergence",
        "type": "Trend Momentum",
        "signals": ["Crossover", "Divergence", "Histogram"],
        "use_case": "Identify trend changes and momentum",
    },
    "Bollinger_Bands": {
        "name": "Bollinger Bands",
        "type": "Volatility",
        "components": ["Upper Band", "Middle Band (SMA)", "Lower Band"],
        "use_case": "Measure volatility and identify overbought/oversold",
    },
    "Volume": {
        "name": "Trading Volume",
        "type": "Volume Indicator",
        "use_case": "Confirm trends and breakouts",
    },
    "Fibonacci": {
        "name": "Fibonacci Retracement",
        "type": "Support/Resistance",
        "levels": ["23.6%", "38.2%", "50%", "61.8%", "78.6%"],
        "use_case": "Identify potential support/resistance levels",
    },
}

# Trading dataset templates
TRADING_QA_DATASET = [
    {
        "instruction": "Analyze this BTC price action: Bitcoin is trading at $43,500 after a 15% pump from $38,000. RSI is at 78. What should traders do?",
        "response": "Bitcoin is showing strong momentum with a 15% rally, but the RSI at 78 indicates overbought conditions. This suggests:\n\n1. **Caution for new longs**: Entering now carries higher risk of a pullback\n2. **Take profit zones**: Traders with existing positions should consider taking partial profits\n3. **Watch for divergence**: If price makes new highs but RSI doesn't, it could signal weakening momentum\n4. **Wait for retracement**: Look for a pullback to support levels (previous resistance around $40,000-41,000)\n5. **Risk management**: Use tight stop losses if entering, as corrections are more likely in overbought conditions\n\nBest approach: Wait for consolidation or retracement to healthier RSI levels (50-60) before entering new positions.",
    },
    {
        "instruction": "What is a good risk-to-reward ratio for cryptocurrency trading?",
        "response": "A good risk-to-reward ratio for crypto trading is typically **1:2 or higher**, meaning you risk $1 to potentially make $2 or more. Here's why:\n\n**Minimum Standards:**\n- **Day trading/Scalping**: 1:1.5 to 1:2\n- **Swing trading**: 1:2 to 1:3\n- **Position trading**: 1:3 or higher\n\n**Why 1:2+ matters:**\n- Even with 40% win rate, you can be profitable\n- Compensates for the high volatility in crypto\n- Protects against inevitable losses\n\n**Example:**\n- Risk: $100 (stop loss)\n- Reward: $200+ (take profit)\n- If you win 4/10 trades: (4 × $200) - (6 × $100) = $200 profit\n\n**Key principle**: Never enter a trade unless the potential reward is at least 2x your risk. Higher is better, especially for less experienced traders.",
    },
    {
        "instruction": "Explain how to use MACD for crypto trading",
        "response": "MACD (Moving Average Convergence Divergence) is a powerful trend and momentum indicator. Here's how to use it:\n\n**Components:**\n1. **MACD Line**: 12-day EMA minus 26-day EMA\n2. **Signal Line**: 9-day EMA of MACD line\n3. **Histogram**: Difference between MACD and Signal lines\n\n**Trading Signals:**\n\n**1. Crossovers (Primary Signal)**\n- **Bullish**: MACD crosses above signal line → Consider buying\n- **Bearish**: MACD crosses below signal line → Consider selling\n\n**2. Zero Line Crosses**\n- Above zero = Uptrend\n- Below zero = Downtrend\n\n**3. Divergences (Strong Signal)**\n- **Bullish divergence**: Price makes lower low, MACD makes higher low → Potential reversal up\n- **Bearish divergence**: Price makes higher high, MACD makes lower high → Potential reversal down\n\n**4. Histogram**\n- Expanding = Strengthening trend\n- Contracting = Weakening trend\n\n**Crypto-Specific Tips:**\n- Works best on 4H and daily charts\n- Combine with volume for confirmation\n- Use shorter periods (e.g., 8-17-9) for faster signals on volatile crypto\n- Always confirm with price action and support/resistance",
    },
    {
        "instruction": "What's the difference between spot trading and futures trading in crypto?",
        "response": "**Spot Trading:**\n- You buy and own actual cryptocurrency\n- Pay full price upfront (e.g., $40,000 for 1 BTC)\n- Can only profit from price increases (go long)\n- No liquidation risk\n- Unlimited holding time\n- Lower risk, better for beginners\n- Example: Buy BTC at $40k, sell at $45k = $5k profit\n\n**Futures Trading:**\n- Trade contracts representing crypto (don't own the asset)\n- Use leverage (e.g., control $40,000 BTC with $4,000)\n- Can profit from up OR down movements (long/short)\n- Liquidation risk if price moves against you\n- Contracts have expiration dates (or perpetual)\n- Higher risk, requires experience\n- Example: 10x leverage, BTC moves 5% = 50% gain or loss\n\n**Key Differences:**\n\n| Aspect | Spot | Futures |\n|--------|------|--------|\n| Ownership | Yes | No |\n| Leverage | 1x | Up to 125x |\n| Direction | Long only | Long & Short |\n| Liquidation | No | Yes |\n| Risk | Lower | Much Higher |\n| Complexity | Simple | Complex |\n\n**Recommendation**: Start with spot trading to learn. Only use futures after mastering risk management and understanding leverage mechanics.",
    },
    {
        "instruction": "How do I identify support and resistance levels in crypto?",
        "response": "Support and resistance are price levels where buying/selling pressure historically concentrates. Here's how to identify them:\n\n**Support Levels (Price Floor):**\n1. **Previous lows**: Areas where price bounced up multiple times\n2. **Round numbers**: Psychological levels ($40,000, $50,000)\n3. **Moving averages**: 50-day, 200-day MA often act as support\n4. **Fibonacci retracements**: 38.2%, 50%, 61.8% levels\n5. **Volume shelves**: High volume areas on volume profile\n\n**Resistance Levels (Price Ceiling):**\n1. **Previous highs**: Where price was rejected downward\n2. **Round numbers**: Same as support\n3. **Previous support**: Once broken, old support becomes resistance\n4. **Trendlines**: Connecting higher highs\n\n**How to Draw Them:**\n1. Zoom out to daily/weekly charts\n2. Look for areas where price bounced 2-3+ times\n3. Draw horizontal lines at these levels\n4. Price doesn't need to be exact - use zones\n\n**Trading Strategy:**\n- **At Support**: Look for long entries, place stop loss just below\n- **At Resistance**: Look for short entries or take profits\n- **Breakouts**: When price breaks through, old resistance becomes new support (and vice versa)\n\n**Pro Tip**: The more times a level is tested, the stronger it becomes. But if it breaks, the move is usually powerful.",
    },
]

# Market analysis templates
MARKET_ANALYSIS_PROMPTS = [
    "Analyze current market conditions for BTC",
    "What are the key resistance levels for Ethereum?",
    "Explain the current trend for Solana",
    "What indicators suggest a bullish reversal?",
    "How to identify a bear trap vs real reversal?",
    "What volume patterns indicate accumulation?",
    "Explain how to use order book analysis",
    "What are signs of market manipulation?",
    "How to trade during high volatility?",
    "What timeframe is best for swing trading?",
]

# Risk management templates
RISK_MANAGEMENT_QA = [
    {
        "question": "What percentage of portfolio should I risk per trade?",
        "answer": "**The 1-2% Rule**: Never risk more than 1-2% of your total portfolio on a single trade.\n\n**Why?**\n- Protects you from devastating losses\n- Allows you to survive many losing trades\n- Prevents emotional decision-making\n\n**Example with $10,000 portfolio:**\n- 1% risk = $100 per trade\n- 2% risk = $200 per trade\n- Even with 10 losing trades at 2%, you'd only lose 20%\n- But you only need a few winners at 1:2 R:R to recover\n\n**Position Sizing Formula:**\nPosition Size = (Account Size × Risk %) / (Entry Price - Stop Loss Price)\n\n**Aggressive traders**: 2-3% (higher risk)\n**Conservative traders**: 0.5-1% (safer)\n**Beginners**: Start with 0.5% until consistent\n\nRemember: Surviving in crypto trading is more important than getting rich quickly. Proper risk management keeps you in the game.",
    },
    {
        "question": "How do I set stop losses effectively?",
        "answer": "**Stop Loss Strategies:**\n\n**1. Technical-Based Stops:**\n- Below support levels (for longs)\n- Above resistance levels (for shorts)\n- Below/above key moving averages\n- Outside Bollinger Bands\n- Beyond recent swing high/low\n\n**2. Percentage-Based Stops:**\n- Fixed % below entry (e.g., 5-10% for crypto)\n- Based on average volatility (ATR)\n\n**3. Time-Based Stops:**\n- Exit if trade doesn't work within X hours/days\n- Prevents capital being tied up in dead trades\n\n**Best Practices:**\n\n✅ **Always set stop loss BEFORE entering trade**\n✅ **Place stop beyond noise** - give trade room to breathe\n✅ **Use wider stops in crypto** due to high volatility\n✅ **Don't move stops further away** (only toward profit)\n✅ **Use mental stops on CEX** to avoid stop hunting\n\n❌ **Don't set stops at obvious levels** (just below round numbers)\n❌ **Don't remove stops hoping price recovers**\n❌ **Don't use tight stops in volatile conditions**\n\n**Example for BTC Long:**\n- Entry: $42,000\n- Support: $40,500\n- Stop Loss: $40,200 (just below support with buffer)\n- Risk: $1,800 per BTC\n- Position size based on 2% portfolio risk",
    },
]

def generate_trading_dataset(output_file: str = "trading_dataset.json"):
    """Generate a complete training dataset for crypto trading"""
    import json

    dataset = []

    # Add Q&A pairs
    dataset.extend(TRADING_QA_DATASET)

    # Add risk management Q&A
    dataset.extend(RISK_MANAGEMENT_QA)

    # Add strategy explanations
    for strategy_id, strategy in TRADING_STRATEGIES.items():
        dataset.append({
            "instruction": f"Explain the {strategy['name']} trading strategy",
            "response": f"{strategy['name']}: {strategy['description']}\n\nKey indicators: {', '.join(strategy['indicators'])}\nBest timeframes: {', '.join(strategy['timeframes'])}\nRisk level: {strategy['risk_level']}\n\nThis strategy works well for traders who can monitor these timeframes and are comfortable with {strategy['risk_level'].lower()} risk levels."
        })

    # Add indicator explanations
    for indicator_id, indicator in TECHNICAL_INDICATORS.items():
        dataset.append({
            "instruction": f"What is {indicator['name']} and how do I use it?",
            "response": f"{indicator['name']} ({indicator_id})\n\nType: {indicator['type']}\nUse case: {indicator['use_case']}\n\nThis is a {indicator['type'].lower()} indicator commonly used in technical analysis."
        })

    # Save to file
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"Generated {len(dataset)} training examples")
    print(f"Saved to: {output_file}")

    return dataset


if __name__ == "__main__":
    generate_trading_dataset()
