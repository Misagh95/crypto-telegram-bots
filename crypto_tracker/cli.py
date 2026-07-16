from typing import List

from rich.console import Console
from rich.table import Table

from crypto_tracker.client import CoinPrice

console = Console()


def display_prices(prices: List[CoinPrice], currency: str = "USD"):
    table = Table(title=f"Cryptocurrency Prices ({currency})")

    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Symbol", style="yellow")
    table.add_column(f"Price ({currency})", justify="right")
    table.add_column("Market Cap", justify="right")
    table.add_column("24h Change", justify="right")

    for coin in prices:
        price_str = f"${coin.current_price:,.2f}" if coin.current_price else "N/A"

        cap_str = f"${coin.market_cap:,.0f}" if coin.market_cap else "N/A"

        if coin.price_change_percent_24h is not None:
            change_str = f"{coin.price_change_percent_24h:+.2f}%"
            change_style = "green" if coin.price_change_percent_24h >= 0 else "red"
        else:
            change_str = "N/A"
            change_style = "white"

        table.add_row(
            coin.name,
            coin.symbol,
            price_str,
            cap_str,
            f"[{change_style}]{change_str}[/{change_style}]",
        )

    console.print(table)
