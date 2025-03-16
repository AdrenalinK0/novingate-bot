import mysql.connector
from config import MYSQL_CONFIG

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

def save_user(user_id: int, username: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, username) VALUES (%s, %s)', (user_id, username))
    conn.commit()
    conn.close()