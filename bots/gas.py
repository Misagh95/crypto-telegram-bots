from typing import List

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

ETHERSCAN_URL = "https://api.etherscan.io/api"
ETHERSCAN_KEY = None


async def gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⛽ Fetching gas prices...")

    try:
        if ETHERSCAN_KEY:
            params = {
                "module": "gastracker",
                "action": "gasoracle",
                "apikey": ETHERSCAN_KEY,
            }
            res = requests.get(ETHERSCAN_URL, params=params, timeout=10)
            res.raise_for_status()
            data = res.json().get("result", {})

            if data:
                safe = data.get("SafeGasPrice", "?")
                propose = data.get("ProposeGasPrice", "?")
                fast = data.get("FastGasPrice", "?")
                lines = [
                    "⛽ *Ethereum Gas Fees*\n",
                    f"🐢 Safe: `{safe} Gwei`",
                    f"🚶 Normal: `{propose} Gwei`",
                    f"🚀 Fast: `{fast} Gwei`",
                ]
                await msg.edit_text("\n".join(lines), parse_mode="Markdown")
                return

        res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"},
            timeout=10,
        )
        eth_price = res.json().get("ethereum", {}).get("usd", "?")

        res = requests.get(
            "https://ethgasstation.info/api/ethgasAPI.json",
            timeout=10
        )
        res.raise_for_status()
        data = res.json()
        safe = data.get("safeLow", data.get("safeLow", 10)) / 10
        propose = data.get("average", data.get("average", 20)) / 10
        fast = data.get("fast", data.get("fast", 30)) / 10

        lines = [
            "⛽ *Ethereum Gas Fees*\n",
            f"🐢 Safe: `{safe:.1f} Gwei`",
            f"🚶 Normal: `{propose:.1f} Gwei`",
            f"🚀 Fast: `{fast:.1f} Gwei`",
            f"\nETH: `${eth_price}`",
        ]
        await msg.edit_text("\n".join(lines), parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(f"Error fetching gas: {e}")


def get_handlers() -> List[CommandHandler]:
    return [CommandHandler("gas", gas, filters.TEXT)]
