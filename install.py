import sys
import os
import subprocess
import mysql.connector

# اضافه کردن مسیر پروژه به sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def create_config_file(bot_token, admin_id, db_name, db_user, db_password):
    config_content = f"""
BOT_TOKEN = '{bot_token}'
ADMIN_ID = '{admin_id}'

# تنظیمات دیتابیس
DB_CONFIG = {{
    'host': 'localhost',
    'user': '{db_user}',
    'password': '{db_password}',
    'database': '{db_name}'
}}
"""
    with open(os.path.join(project_root, "config.py"), "w") as config_file:
        config_file.write(config_content)

def install():
    print("Starting NovinGate Bot Installation...")

    # دریافت اطلاعات از کاربر
    bot_token = input("Enter your Telegram Bot Token: ")
    admin_id = input("Enter Admin ID (numeric): ")
    db_name = input("Enter Database Name: ")
    db_user = input("Enter Database Username: ")
    db_password = input("Enter Database Password: ")
    domain = input("Enter your domain (e.g., example.com): ")

    # ایجاد فایل config.py
    print("Creating config.py...")
    create_config_file(bot_token, admin_id, db_name, db_user, db_password)

    # نصب پکیج‌های مورد نیاز
    print("Installing required packages...")
    subprocess.run(["pip3", "install", "-r", "requirements.txt"])

    # تنظیم SSL
    print("Setting up SSL...")
    from utils.ssl_manager import setup_ssl, renew_ssl
    setup_ssl(domain)
    renew_ssl(domain)

    # ایجاد دیتابیس و جداول
    print("Initializing database...")
    from database.db_init import initialize_database
    initialize_database(db_name, db_user, db_password)

    # تنظیم وب‌هوک
    print("Setting webhook...")
    subprocess.run(["python3", "bot.py", "--set-webhook", domain])

    # نصب phpMyAdmin
    print("Installing phpMyAdmin...")
    subprocess.run(["sudo", "apt-get", "install", "phpmyadmin", "-y"])

    # اجرای ربات
    print("Starting the bot...")
    subprocess.run(["python3", "bot.py"])

    print("Installation completed successfully!")
    print(f"Admin Panel: http://{domain}/admin")
    print(f"phpMyAdmin: http://{domain}/phpmyadmin")

if __name__ == "__main__":
    install()