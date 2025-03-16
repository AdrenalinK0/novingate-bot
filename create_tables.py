import mysql.connector
from mysql.connector import Error

def create_tables():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_db_user",
            password="your_db_pass",
            database="your_db_name"
        )
        cursor = connection.cursor()

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

        # سایر جداول...

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