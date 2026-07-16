# Crypto Telegram Bots

A collection of cryptocurrency Telegram bots — price alerts, Fear & Greed index, and news.

## Bots

| Command | Bot | Description |
|---------|-----|-------------|
| `/price bitcoin ethereum` | Price Alert | Real-time crypto prices from CoinGecko |
| `/alert bitcoin above 70000` | Price Alert | Check if price is above/below a target |
| `/fng` | Fear & Greed | Market sentiment index (last 7 days) |
| `/news 5` | News Aggregator | Latest crypto news |

## Setup

```bash
git clone https://github.com/Misagh95/crypto-telegram-bots.git
cd crypto-telegram-bots
pip install -r requirements.txt
```

Create a `.env` file:

```
TELEGRAM_BOT_TOKEN=your_token_here
```

Get the token from [@BotFather](https://t.me/BotFather) on Telegram.

## Run

```bash
python main.py
```

## API

- [CoinGecko](https://www.coingecko.com/en/api) — free, no key
- [Alternative.me](https://alternative.me/crypto/fear-and-greed-index) — free, no key
- [CryptoCompare](https://min-api.cryptocompare.com/) — free, no key (optional: NewsAPI)
