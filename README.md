# Crypto Telegram Bot

Multi-feature cryptocurrency Telegram bot.

## Commands

| Command | Description |
|---------|-------------|
| `/price bitcoin eth` | Real-time prices |
| `/alert bitcoin above 70000` | Price alert |
| `/fng` | Fear & Greed Index |
| `/news 5` | Latest crypto news (EN) |
| `/fnews 5` | آخرین اخبار کریپتو (فارسی) |
| `/whale` | Recent whale transactions |
| `/gas` | Ethereum gas fees |
| `/add bitcoin 0.5` | Add coin to portfolio |
| `/remove bitcoin` | Remove coin from portfolio |
| `/portfolio` | View your portfolio |
| `/ask What is DeFi?` | AI assistant (needs OpenAI key) |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys
python main.py
```

## APIs

- [CoinGecko](https://www.coingecko.com/en/api) — prices (free tier)
- [Etherscan](https://etherscan.io/myapikey) — whale alerts & gas (free)
- [OpenAI](https://platform.openai.com/api-keys) — AI assistant (paid)
