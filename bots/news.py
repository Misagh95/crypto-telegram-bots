import os
from typing import List

import feedparser
import requests
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
]

NEWSAPI_URL = "https://newsapi.org/v2/everything"
NEWSAPI_KEY = None
TRANSLATOR = GoogleTranslator(source="en", target="fa")


def _get_articles(limit: int) -> list:
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

    return articles[:limit]


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = 5
    if context.args:
        try:
            limit = min(int(context.args[0]), 10)
        except ValueError:
            pass

    articles = _get_articles(limit)

    if not articles:
        await update.message.reply_text("No news found.")
        return

    lines = ["📰 *Latest Crypto News*\n"]
    for i, article in enumerate(articles, 1):
        title = article.get("title", "Untitled")
        url = article.get("url", "")
        source = article.get("source", "Unknown")
        lines.append(f"{i}. [{title}]({url})\n   — {source}")

    await update.message.reply_text(
        "\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True
    )


async def fnews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = 5
    if context.args:
        try:
            limit = min(int(context.args[0]), 10)
        except ValueError:
            pass

    articles = _get_articles(limit)

    if not articles:
        await update.message.reply_text("خبری یافت نشد.")
        return

    lines = ["📰 *آخرین اخبار کریپتو* 🆕\n"]
    for i, article in enumerate(articles, 1):
        title = article.get("title", "بدون عنوان")
        url = article.get("url", "")
        source = article.get("source", "ناشناس")
        try:
            title_fa = TRANSLATOR.translate(title)
        except Exception:
            title_fa = title
        lines.append(f"🔹 *{title_fa}*")
        lines.append(f"   📎 [مشاهده مطلب]({url}) — {source}\n")

    await update.message.reply_text(
        "\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True
    )


def get_handlers() -> List[CommandHandler]:
    return [
        CommandHandler("news", news, filters.TEXT),
        CommandHandler("fnews", fnews, filters.TEXT),
    ]
