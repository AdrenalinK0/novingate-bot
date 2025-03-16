import mysql.connector
from config import DB_CONFIG

def initialize_database(db_name, db_user, db_password):
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()

    # ایجاد دیتابیس
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")

    # ایجاد جداول
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT UNIQUE,
            balance FLOAT DEFAULT 0,
            referral_code VARCHAR(255)
        )
    """)
    # سایر جداول (مانند اکانت‌ها، تیکت‌ها، پلن‌ها و ...)

    conn.commit()
    cursor.close()
    conn.close()