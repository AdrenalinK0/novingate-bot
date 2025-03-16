import os
import subprocess
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# رنگ‌های خروجی ترمینال
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# بارگذاری متغیرهای محیطی
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# تابع اجرای دستورات شل
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"{RED}❌ خطا: {result.stderr}{RESET}")
        exit(1)
    return result.stdout

# نصب پکیج‌های موردنیاز
def install_dependencies():
    print(f"{GREEN}🔄 نصب وابستگی‌های موردنیاز...{RESET}")
    run_command("apt update && apt upgrade -y")
    run_command("apt install -y python3 python3-pip mysql-server ufw certbot python3-certbot-nginx")
    run_command("pip3 install -r requirements.txt")

# تنظیم فایروال
def setup_firewall():
    print(f"{GREEN}🛡️ تنظیم فایروال...{RESET}")
    run_command("ufw allow 22/tcp")  # SSH
    run_command("ufw allow 443/tcp")  # SSL
    run_command("ufw allow 80/tcp")  # HTTP
    run_command("ufw enable")

# ایجاد دیتابیس و جداول
def create_database():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"{GREEN}✅ دیتابیس {DB_NAME} ایجاد شد!{RESET}")
    except Error as e:
        print(f"{RED}❌ خطا در ایجاد دیتابیس: {e}{RESET}")
        exit(1)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ایجاد جداول دیتابیس
def create_tables():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            id INT AUTO_INCREMENT PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            balance DECIMAL(10,2) DEFAULT 0,
            FOREIGN KEY (telegram_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        );
        """)
        
        print(f"{GREEN}✅ جداول دیتابیس ایجاد شدند!{RESET}")
        conn.commit()
    except Error as e:
        print(f"{RED}❌ خطا در ایجاد جداول: {e}{RESET}")
        exit(1)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# تنظیم گواهی SSL
def setup_ssl():
    domain = input(f"{GREEN}🌐 لطفاً دامنه ربات را وارد کنید: {RESET}")
    print(f"{GREEN}🔒 در حال گرفتن گواهی SSL برای {domain}...{RESET}")
    run_command(f"certbot --nginx -d {domain}")
    print(f"{GREEN}✅ گواهی SSL با موفقیت دریافت شد!{RESET}")

# تنظیم وبهوک
def set_webhook():
    webhook_url = input(f"{GREEN}🌍 لطفاً آدرس وبهوک را وارد کنید: {RESET}")
    print(f"{GREEN}🔗 تنظیم وبهوک...{RESET}")
    run_command(f"curl -X POST https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")
    print(f"{GREEN}✅ وبهوک تنظیم شد!{RESET}")

# اجرای ربات به‌صورت سرویس
def setup_service():
    print(f"{GREEN}⚙️ تنظیم اجرای دائمی ربات...{RESET}")
    service_content = f"""
    [Unit]
    Description=Novingate Bot Service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /root/novingate-bot/bot.py
    WorkingDirectory=/root/novingate-bot/
    Restart=always
    User=root

    [Install]
    WantedBy=multi-user.target
    """
    with open("/etc/systemd/system/novingate.service", "w") as service_file:
        service_file.write(service_content)
    run_command("systemctl daemon-reload")
    run_command("systemctl enable novingate.service")
    run_command("systemctl start novingate.service")
    print(f"{GREEN}✅ ربات به‌صورت دائمی اجرا شد!{RESET}")

# اجرای فرآیند نصب
def main():
    print(f"{GREEN}🚀 شروع فرآیند نصب ربات...{RESET}")
    install_dependencies()
    setup_firewall()
    create_database()
    create_tables()
    setup_ssl()
    set_webhook()
    setup_service()
    print(f"{GREEN}🎉 نصب با موفقیت انجام شد!{RESET}")

if __name__ == "__main__":
    main()