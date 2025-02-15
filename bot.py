from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from pyrogram import Client

# Telegram API डिटेल्स
API_ID = 'YOUR_API_ID_HERE'
API_HASH = 'YOUR_API_HASH_HERE'
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# अपडेट चैनल का यूज़रनेम
REQUIRED_CHANNEL = 'https://t.me/+Qy5s88rkx0hjNmY1'

# Pyrogram Client
pyro_client = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Menu", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    start_message = (
        "🤖 Bot Status: Active ✅\n\n"
        "📢 For announcements and updates, join us 👉 [here](https://t.me/+Qy5s88rkx0hjNmY1).\n\n"
        "💡 Tip: To use Raven in your group, make sure to set it as an admin."
    )
    await update.message.reply_text(start_message, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'menu':
        user_id = query.from_user.id
        try:
            async with pyro_client:
                chat_member = await pyro_client.get_chat_member(REQUIRED_CHANNEL, user_id)
                if chat_member.status in ['member', 'administrator', 'creator']:
                    await query.edit_message_text("Welcome to the Menu! Here are your options...")
                else:
                    await query.edit_message_text(
                        f"To access the menu, please first join our update channel {REQUIRED_CHANNEL}."
                    )
        except Exception as e:
            await query.edit_message_text(f"An error occurred: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == '__main__':
    main()
