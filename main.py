import sys

from crypto_tracker.client import CoinGeckoClient
from crypto_tracker.cli import display_prices

DEFAULT_COINS = ["bitcoin", "ethereum", "tether", "ripple", "cardano",
                 "solana", "dogecoin", "polkadot", "litecoin", "chainlink"]


def main():
    coins = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_COINS

    client = CoinGeckoClient()
    try:
        prices = client.get_prices(coins)
        display_prices(prices)
    except Exception as e:
        print(f"Error fetching prices: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
