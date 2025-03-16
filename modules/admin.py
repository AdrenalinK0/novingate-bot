from telegram import Update
from telegram.ext import CallbackContext

def admin_panel(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to Admin Panel!")
    # سایر عملکردهای ادمین