from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN, MYSQL_CONFIG, ADMIN_ID
from utils.db_utils import get_db_connection, save_user
from utils.keyboard_utils import user_main_menu_keyboard, admin_main_menu_keyboard

def start(update, context):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        update.message.reply_text(
            'سلام! به پنل ادمین خوش آمدید. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:',
            reply_markup=admin_main_menu_keyboard()
        )
    else:
        update.message.reply_text(
            'سلام! به ربات novingate خوش آمدید. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:',
            reply_markup=user_main_menu_keyboard()
        )

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # ثبت دستورات
    dispatcher.add_handler(CommandHandler("start", start))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()