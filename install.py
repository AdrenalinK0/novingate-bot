import mysql.connector
from mysql.connector import Error

# اطلاعات اتصال به دیتابیس
DB_CONFIG = {
    "host": "localhost",
    "user": "novingate_user",  # تغییر دهید
    "password": "your_password",  # تغییر دهید
    "database": "novingate_db"
}

def create_tables():
    try:
        # اتصال به دیتابیس
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # ایجاد جدول کاربران (users)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            username VARCHAR(255),
            wallet_balance DECIMAL(10,2) DEFAULT 0.00
        );
        """)

        # ایجاد جدول سرورها (servers)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            address VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """)

        # ایجاد جدول کیف پول (wallet)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            balance DECIMAL(10,2) DEFAULT 0.00,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # ایجاد جدول اکانت‌های خریداری‌شده (accounts)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            server_id INT NOT NULL,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            expiry_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
        );
        """)

        # ایجاد جدول پرداخت‌ها (transactions)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            transaction_type ENUM('deposit', 'withdrawal') NOT NULL,
            status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # ایجاد جدول پشتیبانی (tickets)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            message TEXT NOT NULL,
            status ENUM('open', 'closed') DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # ایجاد جدول پلن‌های فروش (plans)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            user_limit INT NOT NULL,
            duration_days INT NOT NULL,
            price DECIMAL(10,2) NOT NULL
        );
        """)

        # ایجاد جدول زیرمجموعه‌گیری (referrals)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            referrer_id INT NOT NULL,
            referred_id INT NOT NULL,
            reward DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (referred_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # ثبت تغییرات در دیتابیس
        conn.commit()
        print("✅ تمام جداول با موفقیت ایجاد شدند.")
    
    except Error as e:
        print(f"❌ خطا در ایجاد جداول: {e}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 ارتباط با دیتابیس بسته شد.")

if __name__ == "__main__":
    create_tables()
