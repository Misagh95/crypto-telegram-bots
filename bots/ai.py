import os
from typing import List

from openai import OpenAI
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = (
    "You are a cryptocurrency expert assistant. Answer questions about crypto, "
    "blockchain, DeFi, trading, and market analysis. Be concise and accurate."
)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text(
            "AI assistant is not configured. Set OPENAI_API_KEY in .env"
        )
        return

    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("Usage: /ask <your question>")
        return

    msg = await update.message.reply_text("🤔 Thinking...")

    try:
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            max_tokens=500,
            timeout=30,
        )
        answer = res.choices[0].message.content
        await msg.edit_text(f"🤖 *AI Assistant*\n\n{answer}", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"Error: {e}")


def get_handlers() -> List[CommandHandler]:
    return [CommandHandler("ask", ask, filters.TEXT)]
