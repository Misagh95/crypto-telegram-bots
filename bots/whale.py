import os
from typing import List

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_URL = "https://api.etherscan.io/api"

WHALE_THRESHOLD_USD = 1_000_000
ETH_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"


async def whale(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ETHERSCAN_KEY:
        await update.message.reply_text(
            "Whale Alert needs ETHERSCAN_API_KEY. Get one at https://etherscan.io/myapikey"
        )
        return

    msg = await update.message.reply_text("🐋 Scanning for whale transactions...")

    try:
        eth_price_resp = requests.get(
            ETH_PRICE_URL, params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10
        )
        eth_price = eth_price_resp.json().get("ethereum", {}).get("usd", 3000)

        params = {
            "module": "account",
            "action": "txlist",
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": ETHERSCAN_KEY,
        }
        res = requests.get(ETHERSCAN_URL, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if data.get("status") != "1":
            await msg.edit_text("Error fetching transactions.")
            return

        lines = ["🐋 *Recent Large Transactions*\n"]
        count = 0
        for tx in data.get("result", []):
            if count >= 5:
                break
            value_eth = int(tx["value"]) / 1e18
            value_usd = value_eth * eth_price
            if value_usd < WHALE_THRESHOLD_USD:
                continue

            tx_hash = tx["hash"][:10] + "..." + tx["hash"][-6:]
            from_addr = tx["from"][:6] + "..." + tx["from"][-4:]
            to_addr = tx["to"][:6] + "..." + tx["to"][-4:] if tx["to"] else "N/A"

            lines.append(
                f"🔹 *${value_usd:,.0f}* ({value_eth:,.2f} ETH)\n"
                f"   From: `{from_addr}` → To: `{to_addr}`\n"
                f"   Tx: `{tx_hash}`\n"
            )
            count += 1

        if count == 0:
            lines.append("No whale transactions found in recent blocks.")

        await msg.edit_text("\n".join(lines), parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(f"Error: {e}")


def get_handlers() -> List[CommandHandler]:
    return [CommandHandler("whale", whale, filters.TEXT)]
