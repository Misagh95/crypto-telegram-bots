import os
from typing import List

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from . import coins

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
CG_API_KEY = os.getenv("COINGECKO_API_KEY")


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        coins_list = ", ".join(coins.DEFAULT_COINS[:5])
        await update.message.reply_text(
            f"Usage: /price <coin1> <coin2> ...\n"
            f"Example: /price bitcoin ethereum solana\n\n"
            f"Default: {coins_list}"
        )
        return

    ids = ",".join(c.lower() for c in args)
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}
    if CG_API_KEY:
        params["x_cg_demo_api_key"] = CG_API_KEY

    try:
        res = requests.get(COINGECKO_URL, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if not data:
            await update.message.reply_text("No data found for those coins.")
            return

        lines = []
        for coin_id, info in data.items():
            price_usd = info.get("usd", "N/A")
            change = info.get("usd_24h_change")
            change_str = f"{change:+.2f}%" if change else "N/A"
            icon = "🟢" if change and change >= 0 else "🔴"
            lines.append(f"{icon} *{coin_id.title()}*: ${price_usd:,} ({change_str})")

        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    except requests.RequestException:
        await update.message.reply_text("Error fetching prices. Try again later.")


async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text(
            "Usage: /alert <coin> <above|below> <price>\n"
            "Example: /alert bitcoin above 70000"
        )
        return

    coin = args[0].lower()
    direction = args[1].lower()
    try:
        target = float(args[2])
    except ValueError:
        await update.message.reply_text("Invalid price.")
        return

    if direction not in ("above", "below"):
        await update.message.reply_text("Use 'above' or 'below'.")
        return

    params = {"ids": coin, "vs_currencies": "usd"}
    if CG_API_KEY:
        params["x_cg_demo_api_key"] = CG_API_KEY
    try:
        res = requests.get(COINGECKO_URL, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if coin not in data:
            await update.message.reply_text(f"Coin '{coin}' not found.")
            return

        price_usd = data[coin]["usd"]
        triggered = (
            (direction == "above" and price_usd > target)
            or (direction == "below" and price_usd < target)
        )

        if triggered:
            await update.message.reply_text(
                f"*⚠️ Alert Triggered!*\n"
                f"{coin.title()} is ${price_usd:,.2f} ({direction} ${target:,.2f})",
                parse_mode="Markdown",
            )
        else:
            await update.message.reply_text(
                f"{coin.title()} is ${price_usd:,.2f}. "
                f"Not {direction} ${target:,.2f} yet."
            )

    except requests.RequestException:
        await update.message.reply_text("Error fetching price.")


def get_handlers() -> List[CommandHandler]:
    return [
        CommandHandler("price", price, filters.TEXT),
        CommandHandler("alert", alert, filters.TEXT),
    ]
