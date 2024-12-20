import sqlite3
import os

class WarningStrikesManager:
    def __init__(self, db_path="datenbank/strikes/warning_strike.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS member_warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                clan_name TEXT NOT NULL,
                strikes INTEGER NOT NULL,
                reason TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def delete_old_strikes(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM member_warnings WHERE strikes = 1 AND timestamp <= datetime('now', '-1 day')")
        conn.commit()
        conn.close()

    def delete_old_warnings(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM member_warnings WHERE strikes >= 3 AND timestamp <= datetime('now', '-2 days')")
        conn.commit()
        conn.close()