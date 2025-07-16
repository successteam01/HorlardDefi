import os
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Configuration (replace with your details)
BOT_TOKEN = "7440525122:AAEGzN3cIrHcFIMp10IZ7kT4QiuXLlzm6BE"
TWITTER_URL = "https://twitter.com/horlrads"
CHANNEL_LINK = "t.me/horlards"
GROUP_LINK = "t.me/horlards1"
FACEBOOK_URL = "https://facebook.com/horlards"

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with instructions"""
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("✅ I've Completed All Tasks", callback_data="completed")]]
    
    message = (
        f"👋 Welcome {user.first_name} to Mr. Horlards Airdrop Call!\n\n"
        "🎁 To receive 100 SOL, complete these steps:\n\n"
        f"1. JOIN CHANNEL: {CHANNEL_LINK}\n"
        f"2. JOIN GROUP: {GROUP_LINK}\n"
        f"3. FOLLOW TWITTER: {TWITTER_URL}\n"
        f"4. LIKE FACEBOOK: {FACEBOOK_URL}\n\n"
        "Click the button below when done!"
    )
    
    await update.message.reply_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

async def handle_completion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle task completion confirmation"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎉 Well done! Hope you didn't cheat the system!\n\n"
        "💸 Please send your SOLANA wallet address now to receive 100 SOL\n\n"
        "Example: 5Tw3bBsiy7jT4J7QxEmB3mL8XSAJiT2kR5zTqDZ1V6E"
    )

async def handle_sol_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process SOL address submission"""
    sol_address = update.message.text.strip()
    
    # Basic SOL address validation
    if not re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", sol_address):
        await update.message.reply_text(
            "⚠️ Invalid SOL address! Please send a valid Solana wallet address.\n"
            "Example: 5Tw3bBsiy7jT4J7QxEmB3mL8XSAJiT2kR5zTqDZ1V6E"
        )
        return
    
    # Success message with fake transaction
    await update.message.reply_text(
        f"🚀 Congratulations! You've qualified for Mr. Horlards Airdrop!\n\n"
        f"💸 100 SOL is on its way to:\n{sol_address}\n\n"
        "⌛ Processing time: 2-48 hours\n"
        "⚠️ Note: This is a TEST bot - no real SOL will be sent"
    )

def main() -> None:
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_completion, pattern="^completed$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sol_address))
    
    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
