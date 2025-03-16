import mysql.connector
import config
import logging

logging.basicConfig(level=logging.INFO)

# اتصال به دیتابیس
try:
    db = mysql.connector.connect(
        host="localhost",
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME
    )
    cursor = db.cursor()
    logging.info("✅ اتصال به دیتابیس برقرار شد.")
except mysql.connector.Error as err:
    logging.error(f"❌ خطا در اتصال به دیتابیس: {err}")
    exit()

# ایجاد جدول کاربران
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# ایجاد جدول کیف پول
cursor.execute("""
CREATE TABLE IF NOT EXISTS wallet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    balance INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
);
""")

# ایجاد جدول اکانت‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username VARCHAR(255),
    password VARCHAR(255),
    server_id INT NOT NULL,
    expiration_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
);
""")

# ایجاد جدول تیکت‌های پشتیبانی
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    message TEXT NOT NULL,
    status ENUM('open', 'closed') DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
);
""")

# ایجاد جدول سرورهای iBang
cursor.execute("""
CREATE TABLE IF NOT EXISTS servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")

# ایجاد جدول درگاه‌های پرداخت
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method VARCHAR(50) NOT NULL,
    details TEXT NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active'
);
""")

# ایجاد جدول ادمین‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    access_level ENUM('full', 'support', 'finance') DEFAULT 'support'
);
""")

# ایجاد جدول پلن‌های فروش
cursor.execute("""
CREATE TABLE IF NOT EXISTS plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    users_limit INT NOT NULL,
    duration_days INT NOT NULL,
    price INT NOT NULL
);
""")

# ایجاد جدول زیرمجموعه‌گیری
cursor.execute("""
CREATE TABLE IF NOT EXISTS referrals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    referred_by BIGINT NOT NULL,
    reward INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE,
    FOREIGN KEY (referred_by) REFERENCES users(telegram_id) ON DELETE CASCADE
);
""")

# ذخیره تغییرات و بستن اتصال
db.commit()
cursor.close()
db.close()
logging.info("✅ جداول دیتابیس با موفقیت ایجاد شدند.")
