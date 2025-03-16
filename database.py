import mysql.connector
import os
from dotenv import load_dotenv

# بارگیری متغیرهای محیطی
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


# تابع برای ایجاد اتصال به دیتابیس
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ خطا در اتصال به دیتابیس: {err}")
        return None


# ثبت کاربر جدید در دیتابیس
def add_user(telegram_id, username, referred_by=None):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (telegram_id, username, referred_by)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE username = VALUES(username)
        """, (telegram_id, username, referred_by))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"❌ خطا در افزودن کاربر: {err}")
        return False
    finally:
        cursor.close()
        conn.close()


# دریافت اطلاعات کاربر بر اساس آیدی تلگرام
def get_user(telegram_id):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"❌ خطا در دریافت اطلاعات کاربر: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


# افزایش موجودی کیف پول کاربر
def update_balance(user_id, amount):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"❌ خطا در بروزرسانی موجودی کیف پول: {err}")
        return False
    finally:
        cursor.close()
        conn.close()


# ثبت یک تراکنش جدید
def add_transaction(user_id, amount, method, status="pending"):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (user_id, amount, method, status)
            VALUES (%s, %s, %s, %s)
        """, (user_id, amount, method, status))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"❌ خطا در ثبت تراکنش: {err}")
        return False
    finally:
        cursor.close()
        conn.close()


# دریافت تراکنش‌های یک کاربر
def get_transactions(user_id):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        transactions = cursor.fetchall()
        return transactions
    except mysql.connector.Error as err:
        print(f"❌ خطا در دریافت تراکنش‌ها: {err}")
        return []
    finally:
        cursor.close()
        conn.close()


# ایجاد یک تیکت جدید
def create_ticket(user_id, message):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (user_id, message)
            VALUES (%s, %s)
        """, (user_id, message))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"❌ خطا در ثبت تیکت: {err}")
        return False
    finally:
        cursor.close()
        conn.close()


# دریافت لیست تیکت‌های یک کاربر
def get_tickets(user_id):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tickets WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        tickets = cursor.fetchall()
        return tickets
    except mysql.connector.Error as err:
        print(f"❌ خطا در دریافت تیکت‌ها: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
