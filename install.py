def create_tables():
    """ایجاد جداول دیتابیس با مدیریت بهتر خطاها"""
    print(f"{GREEN}🔄 در حال ایجاد جداول دیتابیس...{RESET}")

    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if conn.is_connected():
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

            print(f"{GREEN}✅ جداول با موفقیت ایجاد شدند!{RESET}")
            conn.commit()

    except mysql.connector.Error as e:
        print(f"{RED}❌ خطا در ایجاد جداول: {e}{RESET}")
        exit(1)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
