from dotenv import load_dotenv
import os
import logging
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler


load_dotenv()

tg_token = os.getenv("TG_TOKEN")

keyboard = [
        [
            InlineKeyboardButton("Add Word", callback_data="add_word"),
            InlineKeyboardButton("Quiz", callback_data="quiz"),
        ]
    ]

reply_markup = InlineKeyboardMarkup(keyboard)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with two inline buttons attached."""
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    if query.data == "add_word":
        await query.message.reply_text("You chose Add Word.", reply_markup=reply_markup)
    elif query.data == "quiz":
        await query.message.reply_text("You chose Quiz.", reply_markup=reply_markup)

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(token=tg_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
