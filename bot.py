import re
import os
import json
import random
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
print(bot_token)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def set_channel():
    pass
    #TODO: Implement channel setting logic


async def set_template():
    pass
    #TODO: Implement template setting logic


async def configure_posting():
    pass
    #TODO: Implement auto-posting configuration logic


async def start_posting():
    pass
    #TODO: Implement auto-posting start logic



async def set_currency():
    pass
    #TODO: Implement currency setting logic



async def stop_posting():
    pass
    #TODO: Implement auto-posting stop logic


async def set_interval():
    pass
    #TODO: Implement posting interval setting logic



async def schedule_times():
    pass
    #TODO: Implement specific times scheduling logic






async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    
    keyboard = [
        [InlineKeyboardButton("📢 1. Set Target Channel", callback_data='set_channel')],
        [InlineKeyboardButton("📝 2. Create Text Template", callback_data='set_template')],
        [InlineKeyboardButton("🔧 3. Configure Auto-Posting", callback_data='configure_posting')]
        [InlineKeyboardButton("▶️ 3. Start Auto-Posting", callback_data='start_posting')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to the Price Auto-Poster Bot! 🤖\n\n"
        "Let's get you set up so I can post Gold and Euro prices directly to your channel.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    
    await query.answer()
    
    if query.data == 'set_channel':
        await query.edit_message_text(text="Please add me as an Administrator to your channel, then forward any message from that channel to me here.")

    
    elif query.data == 'set_template':
        await query.edit_message_text(text="Please type your template. Use {gold} and {euro} where you want the prices to appear.\n\nExample: 'Today's Gold is {gold}'")
        
    elif query.data == 'start_posting':
        await query.edit_message_text(text="✅ Auto-posting activated! I will now post updates to your channel.")
    elif query.data == 'configure_posting':
        await query.edit_message_text(text="Auto-posting Settings:")
        keyboard = [
            [InlineKeyboardButton("⏰ Set Posting Interval", callback_data='set_interval')],
            [InlineKeyboardButton("📅 Schedule Specific Times", callback_data='schedule_times')],
            [InlineKeyboardButton("⏹️ Stop Auto-Posting", callback_data='stop_posting')],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data='main_menu')],
            [InlineKeyboardButton("Set Currency", callback_data='set_currency')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.data == "main_menu":
            await query.edit_message_text(text="Welcome to the Price Auto-Poster Bot! 🤖\n\nLet's get you set up so I can post Gold and Euro prices directly to your channel.", reply_markup=reply_markup)
        elif query.data == "set_interval":
            await query.edit_message_text(text="Please enter the posting interval in minutes (e.g., 60 for hourly updates).")
        elif query.data == "schedule_times":
            await query.edit_message_text(text="Please enter the specific times you want the updates to be posted (e.g., 09:00, 12:00, 18:00).")
        elif query.data == "stop_posting":
            await query.edit_message_text(text="⏹️ Auto-posting stopped. You can reactivate it anytime from the settings.")
        elif query.data == "set_currency":
            await query.edit_message_text(text="Please enter the currency you want to track (e.g., USD, EUR).")
            courensy = await context.bot.wait_for('message', timeout=60)
            await query.edit_message_text(text=f"Currency set to {courensy.text}. I will now track {courensy.text} prices.")



if __name__ == '__main__':
    app = Application.builder().token(bot_token).build()

    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()