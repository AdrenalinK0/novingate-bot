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

def setup_nginx(domain):
    nginx_config = f"""
server {{
    listen 80;
    server_name {domain};

    location / {{
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
    config_path = f"/etc/nginx/sites-available/{domain}"
    enabled_path = f"/etc/nginx/sites-enabled/{domain}"

    # ایجاد فایل پیکربندی Nginx
    with open(config_path, "w") as nginx_file:
        nginx_file.write(nginx_config)

    # ایجاد لینک سمبلیک برای فعال‌سازی سایت
    if os.path.exists(enabled_path):
        os.remove(enabled_path)
    os.symlink(config_path, enabled_path)

    # تست و ری‌لود Nginx
    subprocess.run(["nginx", "-t"], check=True)
    subprocess.run(["systemctl", "reload", "nginx"], check=True)

def install():
    print("Starting NovinGate Bot Installation...")

    # ایجاد محیط مجازی
    print("Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", "venv"])
    activate_script = os.path.join(project_root, "venv", "bin", "activate")

    # فعال‌سازی محیط مجازی
    print("Activating virtual environment...")
    activate_command = f"source {activate_script}"
    subprocess.run(activate_command, shell=True, executable="/bin/bash")

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
    subprocess.run([os.path.join(project_root, "venv", "bin", "pip"), "install", "-r", "requirements.txt"])

    # تنظیم Nginx
    print("Setting up Nginx...")
    setup_nginx(domain)

    # تنظیم SSL
    print("Setting up SSL...")
    subprocess.run(["sudo", "certbot", "--nginx", "-d", domain, "--non-interactive", "--agree-tos", "--email", "your-email@example.com"])

    # ایجاد دیتابیس و جداول
    print("Initializing database...")
    from database.db_init import initialize_database
    try:
        initialize_database(db_name, db_user, db_password)
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        print("Please check your database username and password.")
        return

    # تنظیم وب‌هوک
    print("Setting webhook...")
    subprocess.run([os.path.join(project_root, "venv", "bin", "python"), "bot.py", "--set-webhook", domain])

    # نصب phpMyAdmin
    print("Installing phpMyAdmin...")
    subprocess.run(["sudo", "apt-get", "install", "phpmyadmin", "-y"])

    # اجرای ربات
    print("Starting the bot...")
    subprocess.run([os.path.join(project_root, "venv", "bin", "python"), "bot.py"])

    print("Installation completed successfully!")
    print(f"Admin Panel: http://{domain}/admin")
    print(f"phpMyAdmin: http://{domain}/phpmyadmin")

if __name__ == "__main__":
    install()