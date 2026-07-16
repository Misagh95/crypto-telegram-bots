import json
import os
from typing import Dict, List

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

DATA_FILE = "portfolio.json"


def _load_portfolio() -> Dict[str, float]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}


def _save_portfolio(data: Dict[str, float]):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    portfolio_data = _load_portfolio()

    if not portfolio_data:
        await update.message.reply_text(
            "Your portfolio is empty.\n"
            "Add coins: /add <coin_id> <amount>\n"
            "Example: /add bitcoin 0.5"
        )
        return

    ids = ",".join(portfolio_data.keys())
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": ids, "vs_currencies": "usd"},
            timeout=10,
        )
        res.raise_for_status()
        prices = res.json()
    except requests.RequestException:
        await update.message.reply_text("Error fetching prices.")
        return

    total = 0
    lines = ["💼 *Your Portfolio*\n"]
    for coin_id, amount in sorted(portfolio_data.items()):
        price = prices.get(coin_id, {}).get("usd", 0)
        value = amount * price
        total += value
        lines.append(
            f"• *{coin_id.title()}*: {amount} — `${value:,.2f}`"
        )

    lines.append(f"\n💰 *Total: ${total:,.2f}*")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /add <coin_id> <amount>\nExample: /add bitcoin 0.5")
        return

    coin_id = args[0].lower()
    try:
        amount = float(args[1])
    except ValueError:
        await update.message.reply_text("Invalid amount.")
        return

    portfolio_data = _load_portfolio()
    portfolio_data[coin_id] = portfolio_data.get(coin_id, 0) + amount
    _save_portfolio(portfolio_data)

    await update.message.reply_text(
        f"✅ Added {amount} {coin_id.title()} to your portfolio."
    )


async def remove_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /remove <coin_id>\nExample: /remove bitcoin")
        return

    coin_id = args[0].lower()
    portfolio_data = _load_portfolio()

    if coin_id not in portfolio_data:
        await update.message.reply_text(f"{coin_id.title()} not in your portfolio.")
        return

    del portfolio_data[coin_id]
    _save_portfolio(portfolio_data)
    await update.message.reply_text(f"✅ Removed {coin_id.title()} from portfolio.")


def get_handlers() -> List[CommandHandler]:
    return [
        CommandHandler("portfolio", portfolio, filters.TEXT),
        CommandHandler("add", add_coin, filters.TEXT),
        CommandHandler("remove", remove_coin, filters.TEXT),
    ]
