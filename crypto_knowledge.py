"""
Cryptocurrency knowledge base and example prompts
"""

# Example questions for testing the crypto LLM
CRYPTO_PROMPTS = {
    "basics": [
        "What is Bitcoin and how does it work?",
        "Explain blockchain technology in simple terms",
        "What is the difference between Bitcoin and Ethereum?",
        "What are private keys and public keys in cryptocurrency?",
        "How does cryptocurrency mining work?",
    ],
    "defi": [
        "What is DeFi and how does it differ from traditional finance?",
        "Explain what a liquidity pool is",
        "What are smart contracts and how are they used in DeFi?",
        "What is yield farming and how does it work?",
        "Explain impermanent loss in liquidity provision",
    ],
    "trading": [
        "What is technical analysis in cryptocurrency trading?",
        "Explain the difference between market orders and limit orders",
        "What are support and resistance levels?",
        "What is a stop loss and why is it important?",
        "Explain what market capitalization means for cryptocurrencies",
    ],
    "advanced": [
        "How does Ethereum's proof-of-stake consensus mechanism work?",
        "What is Layer 2 scaling and why is it needed?",
        "Explain zero-knowledge proofs in blockchain",
        "What is MEV (Miner Extractable Value)?",
        "How do cross-chain bridges work?",
    ],
    "security": [
        "What are the best practices for securing cryptocurrency?",
        "Explain the difference between hot wallets and cold wallets",
        "What is a hardware wallet and how does it work?",
        "How can I protect myself from crypto scams?",
        "What is two-factor authentication and why should I use it?",
    ],
    "nft": [
        "What are NFTs and how do they work?",
        "Explain the different NFT standards (ERC-721, ERC-1155)",
        "What gives NFTs their value?",
        "How do NFT marketplaces work?",
        "What are the use cases for NFTs beyond digital art?",
    ],
}

# Cryptocurrency glossary for context enhancement
CRYPTO_GLOSSARY = {
    "Bitcoin (BTC)": "The first and largest cryptocurrency by market cap, created by Satoshi Nakamoto in 2009",
    "Ethereum (ETH)": "A blockchain platform with smart contract functionality, the second-largest cryptocurrency",
    "Blockchain": "A distributed ledger technology that records transactions across multiple computers",
    "DeFi": "Decentralized Finance - financial services built on blockchain without intermediaries",
    "Smart Contract": "Self-executing contracts with terms directly written into code",
    "Proof of Work (PoW)": "A consensus mechanism requiring computational work to validate transactions",
    "Proof of Stake (PoS)": "A consensus mechanism where validators stake tokens to secure the network",
    "Altcoin": "Any cryptocurrency other than Bitcoin",
    "Stablecoin": "Cryptocurrencies designed to maintain a stable value, usually pegged to fiat currency",
    "Wallet": "Software or hardware used to store private keys and interact with blockchains",
    "Private Key": "A secret cryptographic key that allows access to cryptocurrency holdings",
    "Public Key": "A cryptographic key that can be shared publicly to receive cryptocurrency",
    "Hash Rate": "The computational power used in mining and processing blockchain transactions",
    "Mining": "The process of validating transactions and adding them to the blockchain",
    "Gas": "Transaction fees paid to execute operations on Ethereum and similar blockchains",
    "Liquidity Pool": "A collection of tokens locked in a smart contract to facilitate trading",
    "Yield Farming": "Earning rewards by providing liquidity or staking tokens in DeFi protocols",
    "NFT": "Non-Fungible Token - a unique digital asset on a blockchain",
    "DAO": "Decentralized Autonomous Organization - an organization governed by smart contracts",
    "Layer 2": "Scaling solutions built on top of blockchain networks to improve speed and reduce costs",
    "Cold Storage": "Keeping cryptocurrency offline to prevent hacking",
    "Hot Wallet": "An online wallet connected to the internet for easy access",
    "Market Cap": "Total value of a cryptocurrency (price × circulating supply)",
    "Tokenomics": "The economics of a cryptocurrency token, including supply, distribution, and utility",
    "Consensus Mechanism": "The method by which a blockchain network agrees on the state of the ledger",
}

# Cryptocurrency project information (major coins)
MAJOR_CRYPTOCURRENCIES = {
    "Bitcoin": {
        "symbol": "BTC",
        "launch_year": 2009,
        "consensus": "Proof of Work",
        "use_case": "Store of value, digital currency",
        "max_supply": "21 million",
        "features": ["First cryptocurrency", "Most secure network", "Digital gold"],
    },
    "Ethereum": {
        "symbol": "ETH",
        "launch_year": 2015,
        "consensus": "Proof of Stake (after The Merge)",
        "use_case": "Smart contract platform, DeFi, NFTs",
        "max_supply": "No hard cap",
        "features": ["Smart contracts", "EVM", "Largest DeFi ecosystem"],
    },
    "Binance Coin": {
        "symbol": "BNB",
        "launch_year": 2017,
        "consensus": "Proof of Staked Authority",
        "use_case": "Exchange utility token, BNB Chain",
        "max_supply": "No hard cap (burns reduce supply)",
        "features": ["Exchange token", "Fast transactions", "Low fees"],
    },
    "Cardano": {
        "symbol": "ADA",
        "launch_year": 2017,
        "consensus": "Proof of Stake (Ouroboros)",
        "use_case": "Smart contract platform",
        "max_supply": "45 billion",
        "features": ["Research-driven", "Peer-reviewed", "Sustainability"],
    },
    "Solana": {
        "symbol": "SOL",
        "launch_year": 2020,
        "consensus": "Proof of History + Proof of Stake",
        "use_case": "High-performance blockchain for DeFi and NFTs",
        "max_supply": "No hard cap",
        "features": ["High throughput", "Low fees", "Fast finality"],
    },
    "Polkadot": {
        "symbol": "DOT",
        "launch_year": 2020,
        "consensus": "Nominated Proof of Stake",
        "use_case": "Cross-chain interoperability",
        "max_supply": "No hard cap",
        "features": ["Parachains", "Interoperability", "Shared security"],
    },
}

# Common cryptocurrency questions and answers for RAG
CRYPTO_QA_PAIRS = [
    {
        "question": "What is the difference between centralized and decentralized exchanges?",
        "answer": "Centralized exchanges (CEX) like Coinbase are operated by a company that controls user funds and order matching. Decentralized exchanges (DEX) like Uniswap allow peer-to-peer trading directly from users' wallets using smart contracts, giving users full control of their funds.",
    },
    {
        "question": "What is gas in Ethereum?",
        "answer": "Gas is the fee required to execute transactions and smart contracts on Ethereum. It's measured in gwei (1 gwei = 0.000000001 ETH). Gas prices vary based on network congestion - when many people are using Ethereum, gas prices increase.",
    },
    {
        "question": "What is a bull market vs bear market?",
        "answer": "A bull market is a period of rising prices and positive sentiment, where investors expect prices to continue going up. A bear market is the opposite - a period of falling prices and negative sentiment. These terms come from how the animals attack: bulls thrust upward with their horns, bears swipe downward with their paws.",
    },
    {
        "question": "What is staking?",
        "answer": "Staking is the process of locking up cryptocurrency to support a blockchain network's operations and security. In return, stakers earn rewards, similar to earning interest. It's used in Proof of Stake blockchains like Ethereum 2.0, Cardano, and Solana.",
    },
    {
        "question": "What is a rug pull?",
        "answer": "A rug pull is a scam where cryptocurrency developers abandon a project and run away with investors' funds. This often happens with new tokens where developers have control over liquidity pools. They suddenly remove all liquidity, leaving investors with worthless tokens.",
    },
]


def get_prompts_by_category(category: str) -> list:
    """Get example prompts by category"""
    return CRYPTO_PROMPTS.get(category, [])


def get_all_prompts() -> list:
    """Get all example prompts"""
    all_prompts = []
    for prompts in CRYPTO_PROMPTS.values():
        all_prompts.extend(prompts)
    return all_prompts


def get_crypto_info(coin_name: str) -> dict:
    """Get information about a major cryptocurrency"""
    return MAJOR_CRYPTOCURRENCIES.get(coin_name, None)


def search_glossary(term: str) -> str:
    """Search the cryptocurrency glossary"""
    # Case-insensitive search
    for key, value in CRYPTO_GLOSSARY.items():
        if term.lower() in key.lower():
            return f"{key}: {value}"
    return None
