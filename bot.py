import re
import os
import json
import random
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes, 
    ConversationHandler, 
    MessageHandler, 
    filters, 
    CallbackQueryHandler
)
from database import get_user_settings, update_user_setting, set_active_status
from getData import get_exchange_rates

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Conversation states
SET_CHANNEL, SET_TEMPLATE, SET_INTERVAL, SET_CURRENCY, SET_SCHEDULE = range(5)

async def post_update(context: ContextTypes.DEFAULT_TYPE):
    """Background task to fetch prices and post to active channels."""
    job = context.job
    user_id = job.user_id
    settings = get_user_settings(user_id)
    
    if not settings['is_active'] or not settings['channel_id']:
        return

    # Fetch rates (Using USD as base for demo, can be dynamic)
    rates = get_exchange_rates("USD")
    if not rates:
        logging.error("Could not fetch rates for auto-posting.")
        return

    # Prepare data for template
    # Note: Using placeholders for gold as it's not in the simple API yet
    gold_price = "N/A" # TODO: Implement gold price source
    euro_price = rates.get("EUR", "N/A")
    
    try:
        message = settings['template'].format(gold=gold_price, euro=euro_price)
        await context.bot.send_message(chat_id=settings['channel_id'], text=message)
        logging.info(f"Posted update for user {user_id} to channel {settings['channel_id']}")
    except Exception as e:
        logging.error(f"Failed to post update: {e}")

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def start_posting_job(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Schedule the auto-posting job for a specific user."""
    settings = get_user_settings(user_id)
    interval = settings['interval'] * 60 # Convert minutes to seconds
    
    remove_job_if_exists(str(user_id), context)
    context.job_queue.run_repeating(post_update, interval=interval, first=10, user_id=user_id, name=str(user_id))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main menu with settings buttons."""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)

    keyboard = [
        [InlineKeyboardButton("📢 1. Set Target Channel", callback_data='set_channel')],
        [InlineKeyboardButton("📝 2. Create Text Template", callback_data='set_template')],
        [InlineKeyboardButton("🔧 3. Configure Auto-Posting", callback_data='configure_posting')],
        [InlineKeyboardButton("▶️ 4. Start Auto-Posting", callback_data='start_posting')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = (
        "Welcome to the Price Auto-Poster Bot! 🤖\n\n"
        f"Current Currency: {settings['currency']}\n"
        f"Current Channel: {settings['channel_id'] or 'Not Set'}\n"
        f"Auto-Posting: {'✅ Active' if settings['is_active'] else '❌ Inactive'}\n\n"
        "Let's get you set up so I can post Gold and Euro prices directly to your channel."
    )

    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle main menu button clicks."""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'set_channel':
        await query.edit_message_text(text="Please forward any message from your channel to me here, or type the Channel ID (e.g., -100123456789).")
        return SET_CHANNEL

    elif query.data == 'set_template':
        await query.edit_message_text(text="Please type your template. Use {gold} and {euro} where you want the prices to appear.\n\nExample: 'Today's Gold is {gold} and Euro is {euro}'")
        return SET_TEMPLATE

    elif query.data == 'start_posting':
        settings = get_user_settings(user_id)
        if not settings['channel_id']:
            await query.edit_message_text(text="❌ Error: Target channel not set! Please set the channel first.")
            return ConversationHandler.END
        
        set_active_status(user_id, True)
        await start_posting_job(user_id, context)
        await query.edit_message_text(text=f"✅ Auto-posting activated! I will now post every {settings['interval']} minutes.")
        return ConversationHandler.END

    elif query.data == 'configure_posting':
        keyboard = [
            [InlineKeyboardButton("⏰ Set Posting Interval", callback_data='set_interval')],
            [InlineKeyboardButton("📅 Schedule Specific Times", callback_data='schedule_times')],
            [InlineKeyboardButton("⏹️ Stop Auto-Posting", callback_data='stop_posting')],
            [InlineKeyboardButton("💱 Set Currency", callback_data='set_currency')],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Auto-posting Settings:", reply_markup=reply_markup)
        return ConversationHandler.END # We return END here because the buttons will trigger their own handlers

    return ConversationHandler.END

async def settings_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle settings menu button clicks."""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "main_menu":
        await start(update, context)
        return ConversationHandler.END
    elif query.data == "set_interval":
        await query.edit_message_text(text="Please enter the posting interval in minutes (e.g., 60 for hourly updates).")
        return SET_INTERVAL
    elif query.data == "schedule_times":
        await query.edit_message_text(text="Please enter the specific times you want the updates to be posted (e.g., 09:00, 12:00, 18:00).")
        return SET_SCHEDULE
    elif query.data == "stop_posting":
        set_active_status(user_id, False)
        remove_job_if_exists(str(user_id), context)
        await query.edit_message_text(text="⏹️ Auto-posting stopped. Background tasks have been cleared.")
        return ConversationHandler.END
    elif query.data == "set_currency":
        await query.edit_message_text(text="Please enter the currency you want to track (e.g., USD, EUR).")
        return SET_CURRENCY

    return ConversationHandler.END

# Input handlers for Conversation
async def save_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    channel_id = None

    if update.message.forward_from_chat:
        channel_id = update.message.forward_from_chat.id
    else:
        channel_id = update.message.text

    update_user_setting(user_id, "channel_id", str(channel_id))
    await update.message.reply_text(f"✅ Target channel set to: {channel_id}")
    await start(update, context)
    return ConversationHandler.END

async def save_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    template = update.message.text
    update_user_setting(user_id, "template", template)
    await update.message.reply_text("✅ Template saved successfully!")
    await start(update, context)
    return ConversationHandler.END

async def save_interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    try:
        interval = int(update.message.text)
        update_user_setting(user_id, "interval", interval)
        await update.message.reply_text(f"✅ Interval set to {interval} minutes.")
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number for the interval.")
    await start(update, context)
    return ConversationHandler.END

async def save_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    currency = update.message.text.upper()
    update_user_setting(user_id, "currency", currency)
    await update.message.reply_text(f"✅ Currency set to {currency}.")
    await start(update, context)
    return ConversationHandler.END

async def save_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    schedule = update.message.text
    update_user_setting(user_id, "schedule_times", schedule)
    await update.message.reply_text(f"✅ Schedule set to: {schedule}")
    await start(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = Application.builder().token(bot_token).build()

    # Create conversation handler for settings
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_handler, pattern='^(set_channel|set_template|start_posting|configure_posting)$'),
            CallbackQueryHandler(settings_callback_handler, pattern='^(set_interval|schedule_times|stop_posting|set_currency|main_menu)$')
        ],
        states={
            SET_CHANNEL: [MessageHandler(filters.ALL & ~filters.COMMAND, save_channel)],
            SET_TEMPLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_template)],
            SET_INTERVAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_interval)],
            SET_CURRENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_currency)],
            SET_SCHEDULE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_schedule)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()