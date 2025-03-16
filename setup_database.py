import mysql.connector

# اطلاعات دیتابیس (این را از config یا .env دریافت کنید)
db_config = {
    "host": "localhost",
    "user": "novingate_user",
    "password": "your_password",
    "database": "novingate_db"
}

# اتصال به دیتابیس
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# ابتدا جدول servers ایجاد شود
cursor.execute("""
CREATE TABLE IF NOT EXISTS servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")

# سپس سایر جداول ایجاد شوند
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    wallet_balance DECIMAL(10,2) DEFAULT 0.00
);
""")

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

conn.commit()
cursor.close()
conn.close()
print("✅ دیتابیس و جداول با موفقیت ایجاد شدند.")
