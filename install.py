import os
import subprocess
import mysql.connector
from mysql.connector import Error

def install_dependencies():
    print("✅ نصب وابستگی‌ها...")
    subprocess.run(["apt", "update"])
    subprocess.run(["apt", "install", "-y", "python3-pip", "mysql-server", "ufw", "certbot", "python3-certbot-nginx"])
    subprocess.run(["pip3", "install", "-r", "requirements.txt"])

def configure_firewall():
    print("✅ تنظیم فایروال...")
    subprocess.run(["ufw", "allow", "OpenSSH"])
    subprocess.run(["ufw", "allow", "80/tcp"])
    subprocess.run(["ufw", "allow", "443/tcp"])
    subprocess.run(["ufw", "--force", "enable"])

def setup_database():
    try:
        print("✅ ایجاد دیتابیس و جداول...")
        conn = mysql.connector.connect(host='localhost', user='root', password='your_root_password')
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS novingate_db")
        cursor.execute("GRANT ALL PRIVILEGES ON novingate_db.* TO 'novingate_user'@'localhost' IDENTIFIED BY 'your_password'")
        cursor.execute("FLUSH PRIVILEGES")
        conn.commit()
        conn.close()
    except Error as e:
        print(f"❌ خطا در ایجاد دیتابیس: {e}")

def create_tables():
    try:
        conn = mysql.connector.connect(host='localhost', user='novingate_user', password='your_password', database='novingate_db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (telegram_id BIGINT PRIMARY KEY, username VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS wallet (id INT AUTO_INCREMENT PRIMARY KEY, telegram_id BIGINT, balance DOUBLE, FOREIGN KEY (telegram_id) REFERENCES users(telegram_id))")
        conn.commit()
        conn.close()
        print("✅ جداول با موفقیت ایجاد شد.")
    except Error as e:
        print(f"❌ خطا در ایجاد جداول: {e}")

def main():
    install_dependencies()
    configure_firewall()
    setup_database()
    create_tables()
    print("🚀 نصب با موفقیت انجام شد!")

if __name__ == "__main__":
    main()
