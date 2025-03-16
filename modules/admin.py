from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def admin_panel(update: Update, context: CallbackContext):
    # ایجاد دکمه‌های شیشه‌ای برای ادمین
    keyboard = [
        [InlineKeyboardButton("مدیریت سرورها", callback_data='manage_servers')],
        [InlineKeyboardButton("مدیریت درگاه‌های پرداخت", callback_data='manage_payments')],
        [InlineKeyboardButton("مدیریت ادمین‌ها", callback_data='manage_admins')],
        [InlineKeyboardButton("مدیریت زیرمجموعه‌گیری", callback_data='manage_referrals')],
        [InlineKeyboardButton("مشاهده وضعیت اتصال اکانت‌ها", callback_data='view_connections')],
        [InlineKeyboardButton("پاسخ به تیکت‌ها", callback_data='answer_tickets')],
        [InlineKeyboardButton("تنظیمات آموزش‌ها", callback_data='manage_education')],
        [InlineKeyboardButton("تنظیم کرون جاب", callback_data='set_cron_job')],
        [InlineKeyboardButton("ارسال پیام همگانی", callback_data='broadcast_message')],
        [InlineKeyboardButton("مدیریت کاربران", callback_data='manage_users')],
        [InlineKeyboardButton("تعریف پلن فروش", callback_data='define_plans')],
        [InlineKeyboardButton("حالت کاربری", callback_data='user_mode')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ارسال پیام با دکمه‌ها
    update.message.reply_text("لطفا یک گزینه را انتخاب کنید:", reply_markup=reply_markup)