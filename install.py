import os
import mysql.connector
import subprocess
import time

def get_input(prompt, default=None):
    value = input(prompt + (f" (پیش‌فرض: {default})" if default else "") + ": ").strip()
    return value if value else default

# دریافت اطلاعات موردنیاز از کاربر
print("🔹 لطفاً اطلاعات موردنیاز برای نصب را وارد کنید:")

bot_domain = get_input("دامنه ربات خود را وارد کنید (بدون 'https://')").lower()
if bot_domain.startswith("https://"):
    print("⚠️ لطفاً فقط نام دامنه را بدون 'https://' وارد کنید.")
    exit(1)

bot_token = get_input("🔑 توکن ربات تلگرام خود را وارد کنید")
admin_id = get_input("🆔 آی‌دی عددی ادمین ربات را وارد کنید")
db_name = get_input("📂 نام دیتابیس", "novingate_db")
db_user = get_input("👤 نام کاربری دیتابیس", "novingate_user")
db_pass = get_input("🔑 رمز عبور دیتابیس")

# نصب پیش‌نیازهای ضروری
print("📦 در حال نصب پکیج‌های ضروری...")
os.system("apt update && apt install -y python3 python3-pip mysql-server certbot")

# دریافت گواهی SSL
print("🔹 در حال دریافت گواهی SSL...")
certbot_command = f"certbot certonly --standalone --preferred-challenges http -d {bot_domain} --non-interactive --agree-tos -m your-email@example.com"
if os.system(certbot_command) != 0:
    print("❌ خطا در دریافت گواهی SSL. لطفاً دامنه و پورت‌ها را بررسی کنید.")
    exit(1)

# تنظیم تمدید خودکار SSL
os.system("echo '0 0,12 * * * root certbot renew --quiet' > /etc/cron.d/certbot-renew")

# ایجاد دیتابیس و جداول
try:
    print("🛠 در حال ایجاد دیتابیس و جداول...")
    conn = mysql.connector.connect(user="root", password="")
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}'")
    cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost'")
    cursor.execute("FLUSH PRIVILEGES")
    conn.commit()
    conn.close()
    print("✅ دیتابیس با موفقیت ایجاد شد!")
except mysql.connector.Error as err:
    print(f"❌ خطا در ایجاد دیتابیس: {err}")
    exit(1)

# تنظیم وبهوک تلگرام
webhook_url = f"https://{bot_domain}/webhook/{bot_token}"
print(f"🌐 تنظیم وبهوک: {webhook_url}")
webhook_command = f"curl -s -X POST https://api.telegram.org/bot{bot_token}/setWebhook -d url={webhook_url}"
if os.system(webhook_command) == 0:
    print("✅ وبهوک با موفقیت تنظیم شد!")
else:
    print("❌ خطا در تنظیم وبهوک.")

# ارسال پیام موفقیت به ادمین
admin_message = f"✅ نصب ربات با موفقیت انجام شد!\n\n🔹 دامنه: {bot_domain}\n🔑 توکن: {bot_token}\n📂 دیتابیس: {db_name}\n👤 نام کاربری دیتابیس: {db_user}"
send_message_command = f'curl -s -X POST https://api.telegram.org/bot{bot_token}/sendMessage -d chat_id={admin_id} -d text="{admin_message}"'
os.system(send_message_command)

print("🚀 نصب با موفقیت انجام شد!")
