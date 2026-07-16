from dataclasses import dataclass
from typing import List, Optional

import requests

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


@dataclass
class CoinPrice:
    name: str
    symbol: str
    current_price: Optional[float]
    market_cap: Optional[float]
    price_change_24h: Optional[float]
    price_change_percent_24h: Optional[float]


class CoinGeckoClient:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def get_prices(self, coins: List[str], currency: str = "usd") -> List[CoinPrice]:
        ids = ",".join(coins).lower()
        url = f"{COINGECKO_BASE}/coins/markets"
        params = {
            "vs_currency": currency,
            "ids": ids,
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h",
        }

        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        return [
            CoinPrice(
                name=item["name"],
                symbol=item["symbol"].upper(),
                current_price=item["current_price"],
                market_cap=item["market_cap"],
                price_change_24h=item["price_change_24h"],
                price_change_percent_24h=item["price_change_percentage_24h"],
            )
            for item in response.json()
        ]
