from typing import List

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Crypto Telegram Bots*\n\n"
        "Available commands:\n\n"
        "*💰 Price Alert Bot*\n"
        "  /price bitcoin ethereum — Get current prices\n"
        "  /alert bitcoin above 70000 — Set price alert\n\n"
        "*😱 Fear & Greed Bot*\n"
        "  /fng — Show Fear & Greed Index\n\n"
        "*📰 News Bot*\n"
        "  /news 5 — Latest crypto news\n\n"
        "Source: https://github.com/Misagh95/crypto-telegram-bots",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


def get_handlers() -> List[CommandHandler]:
    return [
        CommandHandler("start", start, filters.TEXT),
        CommandHandler("help", help_cmd, filters.TEXT),
    ]
