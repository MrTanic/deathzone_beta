import sqlite3
from assets.emojis.reactions_emojis import reactions_emojis

class SaveIMCWLReactions:
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

    def get_reaction_type(self, reaction_emoji):
        if reaction_emoji == "<:ja:961978768765911110>":
            return 'ja'
        elif reaction_emoji == "<:nein:961978783483699251>":
            return 'nein'
        elif reaction_emoji == "<:zap:1204471668198875156>":
            return 'zap'
        return 'nicht reagiert'

    def save_reaction_to_database(self, message_id, user_id, coc_name, reactions, saison_datum):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Löschen der bestehenden Einträge für die gegebene message_id und user_id
        cursor.execute("DELETE FROM im_cwl_umfragen WHERE message_id = ? AND user_id = ?", (message_id, user_id))

        # Überprüfen, ob 'ja' und 'nein' gleichzeitig vorhanden sind
        if 'ja' in reactions and 'nein' in reactions:
            reactions.remove('nein')

        for reaction in reactions:
            cursor.execute('''
                INSERT OR REPLACE INTO im_cwl_umfragen (message_id, user_id, coc_name, reaction, saison_datum)
                VALUES (?, ?, ?, ?, ?)
            ''', (message_id, user_id, coc_name, reaction, saison_datum))

        conn.commit()
        conn.close()