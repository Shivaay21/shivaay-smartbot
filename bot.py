import os
import logging
import wikipedia
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Hello! I'm Shivaay, your friendly AI helper.\n\n"
        "Ask me anything, and I'll try to find the answer.\n\n"
        "Developed with ❤️ by Shivaay."
    )
    await update.message.reply_text(welcome_message)

def wiki_summary(query):
    wikipedia.set_lang("en")
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except wikipedia.DisambiguationError as e:
        options = ", ".join(e.options[:5])
        return f"Your question is ambiguous. Did you mean one of these? {options}"
    except wikipedia.PageError:
        return None
    except Exception as e:
        return f"Sorry, something went wrong: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    user = update.effective_user
    user_name = user.username if user.username else f"{user.first_name} {user.last_name or ''}".strip()
    user_id = user.id

    logger.info(f"Received question from {user_name} (ID: {user_id}): {user_input}")

    answer = wiki_summary(user_input)

    if answer is None:
        search_url = f"https://duckduckgo.com/?q={user_input.replace(' ', '+')}"
        answer = (
            "Sorry, I couldn't find an answer on Wikipedia.\n"
            f"You can try searching here:\n{search_url}"
        )

    await update.message.reply_text(answer)
    logger.info(f"Replied to {user_name} (ID: {user_id})")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
 