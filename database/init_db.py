import mysql.connector
from config import MYSQL_CONFIG

def create_tables():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    with open('database/create_tables.sql', 'r') as file:
        sql_script = file.read()

    cursor.execute(sql_script, multi=True)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()