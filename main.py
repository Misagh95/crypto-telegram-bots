import os
import sys
import logging

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bots import ai, fear_greed, gas, news, portfolio, price_alert, start, whale

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

load_dotenv()


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_token_here":
        print("ERROR: TELEGRAM_BOT_TOKEN not set in .env file")
        sys.exit(1)

    app = ApplicationBuilder().token(token).build()

    for module in [start, price_alert, fear_greed, news, whale, gas, portfolio, ai]:
        for handler in module.get_handlers():
            app.add_handler(handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
