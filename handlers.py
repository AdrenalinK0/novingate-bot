from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import database
import config

# تنظیمات اولیه
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# دکمه‌های اصلی کاربر
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🛒 خرید اکانت", callback_data="buy_account"),
        InlineKeyboardButton("📂 مشاهده اکانت‌ها", callback_data="view_accounts"),
        InlineKeyboardButton("💰 کیف پول", callback_data="wallet"),
        InlineKeyboardButton("🎫 پشتیبانی", callback_data="support"),
        InlineKeyboardButton("📚 آموزش‌ها", callback_data="tutorials"),
        InlineKeyboardButton("🔗 زیرمجموعه‌گیری", callback_data="referral"),
    )
    return keyboard

# دکمه‌های مدیریت ادمین
def admin_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔧 مدیریت سرورها", callback_data="manage_servers"),
        InlineKeyboardButton("💳 مدیریت پرداخت", callback_data="manage_payments"),
        InlineKeyboardButton("👤 مدیریت کاربران", callback_data="manage_users"),
        InlineKeyboardButton("📢 ارسال پیام همگانی", callback_data="send_broadcast"),
        InlineKeyboardButton("📊 مدیریت پلن‌ها", callback_data="manage_plans"),
        InlineKeyboardButton("⚙ تنظیمات", callback_data="settings"),
        InlineKeyboardButton("🔄 تغییر به حالت کاربر", callback_data="switch_to_user"),
    )
    return keyboard

# استارت ربات
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = database.get_user(message.from_user.id)
    if not user:
        database.add_user(message.from_user.id, message.from_user.username)

    if message.from_user.id == config.ADMIN_ID:
        await message.answer("👋 خوش آمدید! شما به عنوان ادمین وارد شده‌اید.", reply_markup=admin_menu())
    else:
        await message.answer("👋 خوش آمدید! لطفاً یکی از گزینه‌های زیر را انتخاب کنید.", reply_markup=main_menu())

# مدیریت کلیک روی دکمه‌ها
@dp.callback_query_handler(lambda c: c.data == "buy_account")
async def buy_account(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "🛒 لطفاً پلن مورد نظر خود را انتخاب کنید.")

@dp.callback_query_handler(lambda c: c.data == "wallet")
async def wallet(callback_query: types.CallbackQuery):
    user = database.get_user(callback_query.from_user.id)
    if user:
        await bot.send_message(callback_query.from_user.id, f"💰 موجودی شما: {user['balance']} تومان")
    else:
        await bot.send_message(callback_query.from_user.id, "❌ حساب شما یافت نشد!")

@dp.callback_query_handler(lambda c: c.data == "support")
async def support(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "🎫 لطفاً پیام خود را ارسال کنید. تیم پشتیبانی به زودی پاسخ خواهد داد.")

# اجرای ربات
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
