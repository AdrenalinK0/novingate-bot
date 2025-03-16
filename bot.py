import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from database import Database

# بارگیری تنظیمات از فایل .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# تنظیمات لاگ‌گیری
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# اتصال به دیتابیس
db = Database()

# ⚡ شروع ربات
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    username = update.message.chat.username
    db.add_user(user_id, username)

    keyboard = [
        [InlineKeyboardButton("🛒 خرید اکانت", callback_data='buy_account')],
        [InlineKeyboardButton("💰 کیف پول", callback_data='wallet')],
        [InlineKeyboardButton("📞 پشتیبانی", callback_data='support')],
        [InlineKeyboardButton("📚 آموزش‌ها", callback_data='tutorials')],
        [InlineKeyboardButton("👥 زیرمجموعه‌گیری", callback_data='referral')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎉 خوش آمدید! لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=reply_markup)

# ⚡ مدیریت دکمه‌های کاربران
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'buy_account':
        query.message.reply_text("🛒 خرید اکانت - لطفاً پلن مورد نظر را انتخاب کنید.")
    elif query.data == 'wallet':
        user = db.get_user(query.message.chat_id)
        query.message.reply_text(f"💰 موجودی کیف پول شما: {user['wallet_balance']} تومان")
    elif query.data == 'support':
        query.message.reply_text("📞 لطفاً سوال خود را ارسال کنید. تیم پشتیبانی پاسخ خواهد داد.")
    elif query.data == 'tutorials':
        query.message.reply_text("📚 آموزش‌های مربوطه به زودی اضافه می‌شود.")
    elif query.data == 'referral':
        query.message.reply_text("👥 لینک زیرمجموعه‌گیری شما:\n\n🔗 example.com/ref?user=123")

# ⚡ پنل مدیریت
def admin_panel(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ شما دسترسی به پنل مدیریت ندارید.")
        return

    keyboard = [
        [InlineKeyboardButton("📊 مدیریت کاربران", callback_data='manage_users')],
        [InlineKeyboardButton("📞 پاسخ به تیکت‌ها", callback_data='manage_tickets')],
        [InlineKeyboardButton("⚙️ تنظیمات", callback_data='settings')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("⚙️ پنل مدیریت", reply_markup=reply_markup)

# ⚡ مدیریت پیام‌های کاربران
def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    text = update.message.text

    if user_id == ADMIN_ID:
        update.message.reply_text("📌 پیام شما دریافت شد و در حال پردازش است...")
    else:
        db.add_ticket(user_id, text)
        update.message.reply_text("✅ تیکت شما ارسال شد. پشتیبانی به زودی پاسخ خواهد داد.")

# ⚡ مدیریت تیکت‌های پشتیبانی در پنل ادمین
def manage_tickets(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ شما دسترسی ندارید.")
        return

    tickets = db.get_all_tickets()
    if not tickets:
        update.message.reply_text("📭 هیچ تیکت جدیدی وجود ندارد.")
        return

    for ticket in tickets:
        update.message.reply_text(f"👤 کاربر: {ticket['user_id']}\n📩 پیام: {ticket['message']}")
        update.message.reply_text("✅ برای پاسخ دادن، ریپلای کنید.")

# ⚡ پاسخ به تیکت‌ها
def reply_ticket(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user_id = int(update.message.reply_to_message.text.split("\n")[0].split(":")[1].strip())
        response = update.message.text
        context.bot.send_message(chat_id=user_id, text=f"📩 پاسخ پشتیبانی:\n\n{response}")
        update.message.reply_text("✅ پاسخ شما به کاربر ارسال شد.")

# ⚡ تنظیمات ربات در پنل ادمین
def settings(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ شما دسترسی ندارید.")
        return

    keyboard = [
        [InlineKeyboardButton("⚡ تنظیم کرون جاب", callback_data='cron_job')],
        [InlineKeyboardButton("🔄 مدیریت درگاه پرداخت", callback_data='manage_payments')],
        [InlineKeyboardButton("📚 تنظیم آموزش‌ها", callback_data='manage_tutorials')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("⚙️ تنظیمات ربات", reply_markup=reply_markup)

# ⚡ اجرای ربات
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("admin", admin_panel))
    dispatcher.add_handler(CommandHandler("settings", settings))
    dispatcher.add_handler(CommandHandler("tickets", manage_tickets))
    dispatcher.add_handler(MessageHandler(Filters.reply & Filters.text, reply_ticket))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
