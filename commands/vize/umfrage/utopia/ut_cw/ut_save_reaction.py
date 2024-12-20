import sqlite3
from datetime import datetime
from bot.setup.discord.channel_ids import UT_ANNOUNCEMENT_CHANNEL
from assets.emojis.reactions_emojis import reactions_emojis

LOG_FILE_PATH = "datenbank/logs/cw_date/ut_cw_announcement_dates.txt"

class SaveReactions:
    def __init__(self, db_path, member_db_path):
        self.db_path = db_path
        self.member_db_path = member_db_path

    def load_all_member_info(self):
        conn = sqlite3.connect(self.member_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, coc_name FROM members")
        all_member_info = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return all_member_info

    def load_cw_date_from_log(self, message_id):
        with open(LOG_FILE_PATH, 'r') as file:
            for line in file:
                if line.startswith(str(message_id)):
                    _, date_str = line.strip().split(':')
                    return date_str
        return None  # Falls das Datum nicht gefunden wird

    def get_reaction_type(self, reaction_emoji):
        for key, emoji in reactions_emojis.items():
            if emoji == reaction_emoji:
                return key
        return 'nicht reagiert'

    def save_reaction_to_database(self, message_id, user_id, coc_name, reaction_type, umfrage_datum):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ut_cw_umfrage (message_id, user_id, coc_name, reaction, umfrage_datum)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(message_id, user_id)
            DO UPDATE SET
                reaction=?
            ''', (message_id, user_id, coc_name, reaction_type, umfrage_datum, reaction_type))
        conn.commit()
        conn.close()