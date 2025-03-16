from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import BOT_TOKEN, ADMIN_ID
from modules.admin import admin_panel
from modules.user import user_panel
import logging

# تنظیمات لاگ
logging.basicConfig(filename='logs/bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if str(user_id) == ADMIN_ID:
        admin_panel(update, context)
    else:
        user_panel(update, context)

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # دستورات
    dispatcher.add_handler(CommandHandler("start", start))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()