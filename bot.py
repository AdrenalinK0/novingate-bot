import sys
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from config import BOT_TOKEN, ADMIN_ID
from modules.admin import admin_panel
from modules.user import user_panel
import logging

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# تنظیمات لاگ
logging.basicConfig(filename='logs/bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if str(user_id) == ADMIN_ID:
        admin_panel(update, context)
    else:
        user_panel(update, context)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # پردازش انتخاب کاربر
    data = query.data
    if data == "buy_account":
        query.edit_message_text(text="شما گزینه خرید اکانت را انتخاب کردید.")
    elif data == "view_accounts":
        query.edit_message_text(text="شما گزینه مشاهده اکانت‌ها را انتخاب کردید.")
    elif data == "wallet":
        query.edit_message_text(text="شما گزینه کیف پول را انتخاب کردید.")
    elif data == "support":
        query.edit_message_text(text="شما گزینه پشتیبانی را انتخاب کردید.")
    elif data == "education":
        query.edit_message_text(text="شما گزینه آموزش‌ها را انتخاب کردید.")
    elif data == "referral":
        query.edit_message_text(text="شما گزینه زیرمجموعه‌گیری را انتخاب کردید.")
    elif data == "manage_servers":
        query.edit_message_text(text="شما گزینه مدیریت سرورها را انتخاب کردید.")
    elif data == "manage_payments":
        query.edit_message_text(text="شما گزینه مدیریت درگاه‌های پرداخت را انتخاب کردید.")
    elif data == "manage_admins":
        query.edit_message_text(text="شما گزینه مدیریت ادمین‌ها را انتخاب کردید.")
    elif data == "manage_referrals":
        query.edit_message_text(text="شما گزینه مدیریت زیرمجموعه‌گیری را انتخاب کردید.")
    elif data == "view_connections":
        query.edit_message_text(text="شما گزینه مشاهده وضعیت اتصال اکانت‌ها را انتخاب کردید.")
    elif data == "answer_tickets":
        query.edit_message_text(text="شما گزینه پاسخ به تیکت‌ها را انتخاب کردید.")
    elif data == "manage_education":
        query.edit_message_text(text="شما گزینه تنظیمات آموزش‌ها را انتخاب کردید.")
    elif data == "set_cron_job":
        query.edit_message_text(text="شما گزینه تنظیم کرون جاب را انتخاب کردید.")
    elif data == "broadcast_message":
        query.edit_message_text(text="شما گزینه ارسال پیام همگانی را انتخاب کردید.")
    elif data == "manage_users":
        query.edit_message_text(text="شما گزینه مدیریت کاربران را انتخاب کردید.")
    elif data == "define_plans":
        query.edit_message_text(text="شما گزینه تعریف پلن فروش را انتخاب کردید.")
    elif data == "user_mode":
        query.edit_message_text(text="شما به حالت کاربری تغییر وضعیت دادید.")

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # دستورات
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()