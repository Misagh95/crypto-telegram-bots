from typing import List

import feedparser
import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
]

NEWSAPI_URL = "https://newsapi.org/v2/everything"
NEWSAPI_KEY = None


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = 5
    if context.args:
        try:
            limit = min(int(context.args[0]), 10)
        except ValueError:
            pass

    articles = []

    if NEWSAPI_KEY:
        try:
            params = {
                "q": "cryptocurrency",
                "sortBy": "publishedAt",
                "pageSize": limit,
                "apiKey": NEWSAPI_KEY,
            }
            res = requests.get(NEWSAPI_URL, params=params, timeout=10)
            res.raise_for_status()
            articles = res.json().get("articles", [])
        except requests.RequestException:
            pass

    if not articles:
        for source, url in FEEDS:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:limit]:
                    articles.append({
                        "title": entry.title,
                        "url": entry.link,
                        "source": source,
                    })
            except Exception:
                continue

    if not articles:
        await update.message.reply_text("No news found.")
        return

    lines = ["📰 *Latest Crypto News*\n"]
    for i, article in enumerate(articles[:limit], 1):
        title = article.get("title", "Untitled")
        url = article.get("url", "")
        source = article.get("source", "Unknown")
        lines.append(f"{i}. [{title}]({url})\n   — {source}")

    await update.message.reply_text(
        "\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True
    )


def get_handlers() -> List[CommandHandler]:
    return [CommandHandler("news", news, filters.TEXT)]
