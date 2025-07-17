from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Bot configuration - YOUR TOKEN IS HARDCODED HERE
TOKEN = "7775404809:AAFnzFYa4iNJRslyKDp2KwEi0obixH_ado0"
CHANNEL_LINK = "https://t.me/your_channel"  # Replace with your actual channel link
GROUP_LINK = "https://t.me/your_group"      # Replace with your actual group link
TWITTER_LINK = "https://twitter.com/your_twitter"  # Replace with your actual Twitter link

def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message and instructions"""
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("I've joined all", callback_data='joined')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🚀 Welcome to Our Airdrop Bot!\n\n"
        "To participate:\n"
        "1. Join our channel\n"
        "2. Join our group\n"
        "3. Follow our Twitter\n"
        "4. Submit your wallet address\n\n"
        "After completing all steps, click below:",
        reply_markup=reply_markup
    )

def handle_joined(update: Update, context: CallbackContext) -> None:
    """Handle when user claims to have joined all channels"""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        "Great! Now please send me your wallet address to complete the airdrop registration."
    )

def handle_wallet(update: Update, context: CallbackContext) -> None:
    """Handle wallet address submission"""
    wallet_address = update.message.text
    
    # Just accept any text as wallet address (no validation)
    update.message.reply_text(
        "🎉 Congratulations! You've successfully registered for the airdrop.\n\n"
        "We'll distribute tokens after the airdrop ends. Stay tuned in our channels!"
    )

def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(handle_joined, pattern='^joined$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet))

    # Start the Bot
    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
