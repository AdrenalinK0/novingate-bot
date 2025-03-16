from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN, ADMIN_ID
from utils.keyboard_utils import user_main_menu_keyboard, admin_main_menu_keyboard

async def start(update: Update, context):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            'سلام! به پنل ادمین خوش آمدید. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:',
            reply_markup=admin_main_menu_keyboard()
        )
    else:
        await update.message.reply_text(
            'سلام! به ربات novingate خوش آمدید. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:',
            reply_markup=user_main_menu_keyboard()
        )

async def handle_message(update: Update, context):
    text = update.message.text
    if text == '💰 شارژ کیف پول':
        await update.message.reply_text('لطفاً مبلغ مورد نظر را وارد کنید:')
    elif text == '🆕 ساخت اکانت جدید':
        await update.message.reply_text('لطفاً پلن مورد نظر را انتخاب کنید:')
    elif text == '📋 مشاهده اکانت‌ها':
        await update.message.reply_text('لیست اکانت‌های شما:')
    elif text == '📨 ارسال تیکت':
        await update.message.reply_text('لطفاً مشکل یا سوال خود را ارسال کنید:')
    elif text == '📬 مشاهده تیکت‌ها':
        await update.message.reply_text('لیست تیکت‌های شما:')
    elif text == '💳 کیف پول':
        await update.message.reply_text('موجودی کیف پول شما:')
    elif text == '👥 زیرمجموعه‌گیری':
        await update.message.reply_text('لینک زیرمجموعه‌گیری شما:')
    elif text == '📚 آموزش‌ها':
        await update.message.reply_text('لیست آموزش‌ها:')
    else:
        await update.message.reply_text('دستور نامعتبر است.')

def main():
    application = Application.builder().token(TOKEN).build()

    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))

    # پردازش پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()