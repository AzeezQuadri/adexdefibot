import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_USERNAME = "@YourChannel"  # Change this to your channel username
GROUP_USERNAME = "@YourGroup"      # Change this to your group username
TWITTER_LINK = "https://twitter.com/YourTwitter"  # Change to your Twitter

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = (
        f"👋 Hello {user.first_name}!\n\n"
        "🚀 Welcome to our Airdrop Bot! Complete these simple steps to qualify:\n\n"
        "1️⃣ Join our official channels\n"
        "2️⃣ Follow our Twitter\n"
        "3️⃣ Submit your Solana wallet address\n\n"
        "Click the button below to begin!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🌟 Start Airdrop Process", callback_data="start_airdrop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Callback handler for buttons
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_airdrop":
        await step1_join_channels(query)
    elif query.data == "check_joined":
        await step2_twitter(query)
    elif query.data == "check_twitter":
        await step3_wallet(query)
    elif query.data == "submit_wallet":
        await finish_airdrop(query)

# Step 1: Ask to join channels
async def step1_join_channels(query) -> None:
    message = (
        "📢 STEP 1: Join our official channels\n\n"
        f"• Telegram Channel: {CHANNEL_USERNAME}\n"
        f"• Telegram Group: {GROUP_USERNAME}\n\n"
        "Click the button below after joining both."
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ I've Joined Both", callback_data="check_joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=message, reply_markup=reply_markup)

# Step 2: Ask to follow Twitter
async def step2_twitter(query) -> None:
    message = (
        "🐦 STEP 2: Follow our Twitter\n\n"
        f"• Twitter: {TWITTER_LINK}\n\n"
        "Click the button below after following."
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ I've Followed", callback_data="check_twitter")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=message, reply_markup=reply_markup)

# Step 3: Ask for wallet address
async def step3_wallet(query) -> None:
    message = (
        "💰 STEP 3: Submit your Solana wallet address\n\n"
        "Please reply with your Solana wallet address (e.g., 7a5...8h3).\n"
        "This is where your airdrop will be sent."
    )
    
    await query.edit_message_text(text=message)
    
    # Store that we're waiting for wallet address
    context.user_data['awaiting_wallet'] = True

# Handle wallet submission
async def handle_wallet(update: Update, context: CallbackContext) -> None:
    if 'awaiting_wallet' in context.user_data:
        wallet_address = update.message.text
        
        # Very basic validation (just checks length)
        if len(wallet_address) >= 10:  # Adjust as needed
            context.user_data['wallet'] = wallet_address
            del context.user_data['awaiting_wallet']
            
            message = (
                f"Wallet received: {wallet_address}\n\n"
                "Ready to submit?"
            )
            
            keyboard = [
                [InlineKeyboardButton("🚀 Submit for Airdrop", callback_data="submit_wallet")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(text=message, reply_markup=reply_markup)
        else:
            await update.message.reply_text("❌ Invalid wallet address. Please try again.")

# Final step
async def finish_airdrop(query) -> None:
    message = (
        "🎉 Congratulations!\n\n"
        "You've successfully completed all steps for the airdrop!\n\n"
        "We'll distribute tokens soon. Stay tuned to our channels for updates!"
    )
    
    await query.edit_message_text(text=message)

def main() -> None:
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
