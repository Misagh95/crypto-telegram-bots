from typing import List

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

FNG_URL = "https://api.alternative.me/fng/"


async def fng(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get(FNG_URL, params={"limit": 7}, timeout=10)
        res.raise_for_status()
        data = res.json()["data"]
    except (requests.RequestException, KeyError):
        await update.message.reply_text("Error fetching Fear & Greed Index.")
        return

    latest = data[0]
    value = latest["value"]
    classification = latest["value_classification"]

    emoji_map = {
        "Extreme Fear": "😱",
        "Fear": "😨",
        "Neutral": "😐",
        "Greed": "😊",
        "Extreme Greed": "🤑",
    }
    emoji = emoji_map.get(classification, "🤔")

    lines = [
        f"{emoji} *Fear & Greed Index*",
        f"Current: *{value}/100* — {classification}",
        "",
        "📊 *Last 7 Days:*",
    ]

    for entry in data:
        date = entry["timestamp"][:10]
        lines.append(f"  {date}: {entry['value']} ({entry['value_classification']})")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


def get_handlers() -> List[CommandHandler]:
    return [CommandHandler("fng", fng, filters.TEXT)]
