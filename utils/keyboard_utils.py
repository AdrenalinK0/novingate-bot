from telegram import ReplyKeyboardMarkup

def user_main_menu_keyboard():
    keyboard = [
        ['💰 شارژ کیف پول', '🆕 ساخت اکانت جدید'],
        ['📋 مشاهده اکانت‌ها', '📨 ارسال تیکت'],
        ['📬 مشاهده تیکت‌ها', '💳 کیف پول'],
        ['👥 زیرمجموعه‌گیری', '📚 آموزش‌ها']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def admin_main_menu_keyboard():
    keyboard = [
        ['💰 شارژ کیف پول', '🆕 ساخت اکانت جدید'],
        ['📋 مشاهده اکانت‌ها', '📨 ارسال تیکت'],
        ['📬 مشاهده تیکت‌ها', '💳 کیف پول'],
        ['👥 زیرمجموعه‌گیری', '📚 آموزش‌ها'],
        ['⚙️ مدیریت ادمین‌ها', '⚙️ مدیریت سرورها'],
        ['⚙️ مدیریت پلن‌ها', '⚙️ مدیریت پرداخت‌ها']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)