from dotenv import load_dotenv
import os

from whatsapp_bot import whatsapp_details
from telegram_bot import start, get_mails, talk_to_llm, search_mails, echo

from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram import Update


load_dotenv()

TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")



if __name__ == "__main__":
    # retrieve_mails()
    application = ApplicationBuilder().token(TELEGRAM_ACCESS_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("getmails", get_mails))
    application.add_handler(CommandHandler("talk", talk_to_llm))
    application.add_handler(CommandHandler("smail", search_mails))

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    
    application.run_polling()