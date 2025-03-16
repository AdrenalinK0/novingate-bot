from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def user_panel(update: Update, context: CallbackContext):
    # ایجاد دکمه‌های شیشه‌ای برای کاربر
    keyboard = [
        [InlineKeyboardButton("خرید اکانت", callback_data='buy_account')],
        [InlineKeyboardButton("مشاهده اکانت‌ها", callback_data='view_accounts')],
        [InlineKeyboardButton("کیف پول", callback_data='wallet')],
        [InlineKeyboardButton("پشتیبانی", callback_data='support')],
        [InlineKeyboardButton("آموزش‌ها", callback_data='education')],
        [InlineKeyboardButton("زیرمجموعه‌گیری", callback_data='referral')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ارسال پیام با دکمه‌ها
    update.message.reply_text("لطفا یک گزینه را انتخاب کنید:", reply_markup=reply_markup)