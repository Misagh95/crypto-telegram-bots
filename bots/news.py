import os
from typing import List

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

CRYPTOCOMPARE_URL = "https://min-api.cryptocompare.com/data/v2/news/"
NEWSAPI_URL = "https://newsapi.org/v2/everything"


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = 5
    if context.args:
        try:
            limit = min(int(context.args[0]), 10)
        except ValueError:
            pass

    newsapi_key = os.getenv("NEWSAPI_KEY")
    if newsapi_key:
        params = {
            "q": "cryptocurrency",
            "sortBy": "publishedAt",
            "pageSize": limit,
            "apiKey": newsapi_key,
        }
        try:
            res = requests.get(NEWSAPI_URL, params=params, timeout=10)
            res.raise_for_status()
            articles = res.json().get("articles", [])
        except requests.RequestException:
            articles = []
    else:
        articles = []
        try:
            res = requests.get(CRYPTOCOMPARE_URL, params={"lang": "EN"}, timeout=10)
            res.raise_for_status()
            items = res.json().get("Data", [])[:limit]
            articles = [
                {
                    "title": item["title"],
                    "url": item["url"],
                    "source": item.get("source", "CryptoCompare"),
                }
                for item in items
            ]
        except requests.RequestException:
            await update.message.reply_text("Error fetching news.")
            return

    if not articles:
        await update.message.reply_text("No news found.")
        return

    lines = ["📰 *Latest Crypto News*\n"]
    for i, article in enumerate(articles, 1):
        title = article.get("title", "Untitled")
        url = article.get("url", "")
        source = article.get("source", article.get("source_name", "Unknown"))
        lines.append(f"{i}. [{title}]({url})\n   — {source}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown",
                                    disable_web_page_preview=True)


def get_handlers() -> List[CommandHandler]:
    return [CommandHandler("news", news, filters.TEXT)]
