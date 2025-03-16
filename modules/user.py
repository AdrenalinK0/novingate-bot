from telegram import Update
from telegram.ext import CallbackContext

def user_panel(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to User Panel!")
    # سایر عملکردهای کاربر