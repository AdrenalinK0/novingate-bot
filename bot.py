from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import mysql.connector
from utils.database import Database

# اتصال به دیتابیس
db = Database()

# دستور شروع
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # بررسی آیا کاربر در دیتابیس وجود دارد
    if not db.user_exists(user_id):
        db.add_user(user_id, username)

    # نمایش منوی اصلی
    keyboard = [
        [InlineKeyboardButton("خرید اکانت", callback_data='buy_account')],
        [InlineKeyboardButton("مشاهده اکانت‌ها", callback_data='view_accounts')],
        [InlineKeyboardButton("کیف پول", callback_data='wallet')],
        [InlineKeyboardButton("تیکت پشتیبانی", callback_data='support_ticket')],
        [InlineKeyboardButton("آموزش‌ها", callback_data='tutorials')],
        [InlineKeyboardButton("زیرمجموعه‌گیری", callback_data='referral')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('به ربات Novingate خوش آمدید!', reply_markup=reply_markup)

# خرید اکانت
def buy_account(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # نمایش پلن‌ها
    plans = db.get_plans()
    keyboard = [[InlineKeyboardButton(plan['name'], callback_data=f'plan_{plan['id']}')] for plan in plans]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="لطفاً یک پلن انتخاب کنید:", reply_markup=reply_markup)

# مشاهده اکانت‌ها
def view_accounts(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    accounts = db.get_user_accounts(user_id)

    if accounts:
        text = "اکانت‌های شما:\n"
        for account in accounts:
            text += f"یوزرنیم: {account['username']}\nپسورد: {account['password']}\nتاریخ انقضا: {account['expiration_date']}\n\n"
    else:
        text = "شما هیچ اکانتی ندارید."

    query.edit_message_text(text=text)

# کیف پول
def wallet(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    balance = db.get_user_balance(user_id)

    keyboard = [
        [InlineKeyboardButton("افزایش موجودی", callback_data='increase_balance')],
        [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"موجودی شما: {balance} تومان", reply_markup=reply_markup)

# افزایش موجودی
def increase_balance(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(text="لطفاً مبلغ مورد نظر را وارد کنید (حداقل 30000 تومان):")
    context.user_data['action'] = 'increase_balance'

# پردازش مبلغ وارد شده
def process_balance(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    amount = float(update.message.text)

    if amount < 30000:
        update.message.reply_text("مبلغ وارد شده باید بیشتر از 30000 تومان باشد.")
        return

    # ذخیره درخواست پرداخت
    db.add_payment(user_id, amount, 'pending')

    keyboard = [
        [InlineKeyboardButton("کارت به کارت", callback_data='card_payment')],
        [InlineKeyboardButton("درگاه پرداخت", callback_data='gateway_payment')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("لطفاً روش پرداخت را انتخاب کنید:", reply_markup=reply_markup)

# پرداخت کارت به کارت
def card_payment(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(text="لطفاً شماره کارت زیر را برای پرداخت استفاده کنید:\n1234-5678-9012-3456\nپس از پرداخت، رسید خود را ارسال کنید.")
    context.user_data['action'] = 'card_payment'

# پردازش رسید کارت به کارت
def process_receipt(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    receipt = update.message.text

    # ارسال رسید به پشتیبانی
    db.add_ticket(user_id, f"رسید پرداخت: {receipt}", 'pending')

    update.message.reply_text("رسید شما برای بررسی به پشتیبانی ارسال شد.")

# تیکت پشتیبانی
def support_ticket(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(text="لطفاً سوال یا مشکل خود را وارد کنید:")
    context.user_data['action'] = 'support_ticket'

# پردازش تیکت
def process_ticket(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    message = update.message.text

    # ذخیره تیکت در دیتابیس
    db.add_ticket(user_id, message, 'open')

    update.message.reply_text("تیکت شما با موفقیت ثبت شد. پشتیبانی به زودی با شما تماس خواهد گرفت.")

# آموزش‌ها
def tutorials(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    tutorials = db.get_tutorials()
    if tutorials:
        text = "آموزش‌های موجود:\n\n"
        for tutorial in tutorials:
            text += f"{tutorial['title']}\n{tutorial['content']}\n\n"
    else:
        text = "هیچ آموزشی موجود نیست."

    query.edit_message_text(text=text)

# زیرمجموعه‌گیری
def referral(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    referral_code = db.get_referral_code(user_id)

    query.edit_message_text(text=f"لینک زیرمجموعه‌گیری شما:\nhttps://t.me/your_bot?start={referral_code}")

# دستورات ادمین
def admin_panel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if db.is_admin(user_id):
        keyboard = [
            [InlineKeyboardButton("مدیریت سرورها", callback_data='manage_servers')],
            [InlineKeyboardButton("مدیریت درگاه‌ها", callback_data='manage_gateways')],
            [InlineKeyboardButton("مدیریت کاربران", callback_data='manage_users')],
            [InlineKeyboardButton("ارسال پیام همگانی", callback_data='broadcast_message')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("پنل ادمین", reply_markup=reply_markup)
    else:
        update.message.reply_text("شما دسترسی ادمین ندارید.")

# ارسال پیام همگانی
def broadcast_message(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(text="لطفاً پیام خود را وارد کنید:")
    context.user_data['action'] = 'broadcast_message'

# پردازش پیام همگانی
def process_broadcast(update: Update, context: CallbackContext):
    message = update.message.text
    users = db.get_all_users()

    for user in users:
        context.bot.send_message(chat_id=user['user_id'], text=message)

    update.message.reply_text("پیام با موفقیت به همه کاربران ارسال شد.")

# پردازش پیام‌ها
def process_message(update: Update, context: CallbackContext):
    action = context.user_data.get('action')

    if action == 'increase_balance':
        process_balance(update, context)
    elif action == 'card_payment':
        process_receipt(update, context)
    elif action == 'support_ticket':
        process_ticket(update, context)
    elif action == 'broadcast_message':
        process_broadcast(update, context)

def main():
    updater = Updater("YOUR_BOT_TOKEN")
    dispatcher = updater.dispatcher

    # دستورات کاربر
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(buy_account, pattern='^buy_account$'))
    dispatcher.add_handler(CallbackQueryHandler(view_accounts, pattern='^view_accounts$'))
    dispatcher.add_handler(CallbackQueryHandler(wallet, pattern='^wallet$'))
    dispatcher.add_handler(CallbackQueryHandler(support_ticket, pattern='^support_ticket$'))
    dispatcher.add_handler(CallbackQueryHandler(tutorials, pattern='^tutorials$'))
    dispatcher.add_handler(CallbackQueryHandler(referral, pattern='^referral$'))

    # دستورات ادمین
    dispatcher.add_handler(CommandHandler("admin", admin_panel))
    dispatcher.add_handler(CallbackQueryHandler(broadcast_message, pattern='^broadcast_message$'))

    # پردازش پیام‌ها
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()