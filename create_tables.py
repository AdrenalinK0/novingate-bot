import mysql.connector
from mysql.connector import Error

def create_tables():
    try:
        # اتصال به دیتابیس
        connection = mysql.connector.connect(
            host="localhost",
            user="your_db_user",
            password="your_db_pass",
            database="your_db_name"
        )
        cursor = connection.cursor()

        # ایجاد جدول کاربران
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT NOT NULL UNIQUE,
                username VARCHAR(255),
                balance DECIMAL(10, 2) DEFAULT 0.00,
                referral_code VARCHAR(255),
                is_admin BOOLEAN DEFAULT FALSE
            )
        """)

        # ایجاد جدول اکانت‌ها
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                username VARCHAR(255),
                password VARCHAR(255),
                expiration_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # ایجاد جدول تیکت‌ها
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                message TEXT,
                status VARCHAR(50) DEFAULT 'open',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # ایجاد جدول پرداخت‌ها
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                amount DECIMAL(10, 2),
                payment_method VARCHAR(255),
                status VARCHAR(50) DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # ایجاد جدول پلن‌ها
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price DECIMAL(10, 2),
                duration_days INT,
                max_users INT
            )
        """)

        connection.commit()
        print("Tables created successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()