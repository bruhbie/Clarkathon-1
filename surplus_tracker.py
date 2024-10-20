import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name="food_surplus.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant TEXT,
            food_type TEXT,
            quantity TEXT,
            posted_at TIMESTAMP
        )
        ''')
        self.conn.commit()

    def add_alert(self, restaurant, food_type, quantity):
        self.cursor.execute('''
        INSERT INTO alerts (restaurant, food_type, quantity, posted_at)
        VALUES (?, ?, ?, ?)
        ''', (restaurant, food_type, quantity, datetime.now()))
        self.conn.commit()

    def get_active_alerts(self):
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        self.cursor.execute('''
        SELECT * FROM alerts
        WHERE posted_at > ?
        ''', (twenty_four_hours_ago,))
        return self.cursor.fetchall()

    def remove_old_alerts(self):
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        self.cursor.execute('''
        DELETE FROM alerts
        WHERE posted_at <= ?
        ''', (twenty_four_hours_ago,))
        self.conn.commit()

    def close(self):
        self.conn.close()