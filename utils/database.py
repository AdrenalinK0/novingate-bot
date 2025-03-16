import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="your_db_user",
            password="your_db_pass",
            database="your_db_name"
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def user_exists(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone() is not None

    def add_user(self, user_id, username):
        self.cursor.execute("INSERT INTO users (user_id, username) VALUES (%s, %s)", (user_id, username))
        self.connection.commit()

    def get_plans(self):
        self.cursor.execute("SELECT * FROM plans")
        return self.cursor.fetchall()

    def get_user_accounts(self, user_id):
        self.cursor.execute("SELECT * FROM accounts WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def get_user_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        result = self.cursor.fetchone()
        return result['balance'] if result else 0.00

    def add_payment(self, user_id, amount, status):
        self.cursor.execute("INSERT INTO payments (user_id, amount, status) VALUES (%s, %s, %s)", (user_id, amount, status))
        self.connection.commit()

    def add_ticket(self, user_id, message, status):
        self.cursor.execute("INSERT INTO tickets (user_id, message, status) VALUES (%s, %s, %s)", (user_id, message, status))
        self.connection.commit()

    def get_tutorials(self):
        self.cursor.execute("SELECT * FROM tutorials")
        return self.cursor.fetchall()

    def get_referral_code(self, user_id):
        self.cursor.execute("SELECT referral_code FROM users WHERE user_id = %s", (user_id,))
        result = self.cursor.fetchone()
        return result['referral_code'] if result else None

    def is_admin(self, user_id):
        self.cursor.execute("SELECT is_admin FROM users WHERE user_id = %s", (user_id,))
        result = self.cursor.fetchone()
        return result['is_admin'] if result else False

    def get_all_users(self):
        self.cursor.execute("SELECT user_id FROM users")
        return self.cursor.fetchall()