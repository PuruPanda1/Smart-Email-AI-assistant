import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram import Update
import asyncio
from services import retrieve_mails, msg_llm, search_mail

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Bubbles, How can I help you today?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "🐢 *Hi! I'm Bubbles, your cute turtle assistant!*\n\n"
        "Here are the things I can do:\n\n"
        "🔹 `/getmails` — Get the latest mails\n"
        "🔹 `/smail <keyword>` — Search mails by keyword\n"
        "🔹 `/talk` — Talk to Bubbles (LLM)\n"
        "🔹 `/start` — Start the bot\n\n"
        "_Try one of these commands!_"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_message,
        parse_mode='Markdown'
    )

async def get_mails(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await retrieve_mails()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result)

async def talk_to_llm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        keyword = " ". join(context.args)
        result = msg_llm(keyword.strip()) # sending user_prompt only
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Bubbles, How can I help you today?")

async def search_mails(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        keyword = "".join(context.args)
        result = search_mail(keyword)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result, parse_mode='Markdown')
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="❌ Please provide a keyword! Usage: /smail <keyword>"
        )