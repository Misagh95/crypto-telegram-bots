from typing import List

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Crypto Telegram Bot*\n\n"
        "*💰 Price* — `/price bitcoin eth`\n"
        "*⚠️ Alert* — `/alert bitcoin above 70000`\n"
        "*😱 Fear & Greed* — `/fng`\n"
        "*📰 News* — `/news 5` (EN) | `/fnews 5` (فارسی)\n"
        "*🐋 Whale Alert* — `/whale`\n"
        "*⛽ Gas Fee* — `/gas`\n"
        "*💼 Portfolio* — `/add bitcoin 0.5` → `/portfolio`\n"
        "*🤖 AI Assistant* — `/ask What is Ethereum?`\n\n"
        "[GitHub](https://github.com/Misagh95/crypto-telegram-bots)",
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
