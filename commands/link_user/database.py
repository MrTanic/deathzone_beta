import sqlite3
import os

# Sicherstellen, dass das Verzeichnis existiert
os.makedirs('datenbank/link', exist_ok=True)

# Datenbankverbindung herstellen (erstellt die Datei, wenn sie nicht existiert)
db_path = 'datenbank/link/discord_users.db'

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        discord_id TEXT NOT NULL,
        player_tag TEXT NOT NULL,
        PRIMARY KEY (discord_id, player_tag),
        UNIQUE (player_tag)
    )
    ''')
    conn.commit()
    conn.close()

def add_user(discord_id, player_tag):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO users (discord_id, player_tag)
    VALUES (?, ?)
    ''', (discord_id, player_tag))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT discord_id, player_tag FROM users
    ''')
    users = cursor.fetchall()
    conn.close()
    return [{"discord_id": row[0], "player_tag": row[1]} for row in users]

def get_user_by_player_tag(player_tag):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT discord_id FROM users WHERE player_tag = ?
    ''', (player_tag,))
    user = cursor.fetchone()
    conn.close()
    return user

def delete_user_by_player_tag(player_tag):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM users WHERE player_tag = ?
    ''', (player_tag,))
    conn.commit()
    conn.close()