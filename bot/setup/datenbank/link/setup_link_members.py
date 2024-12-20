import sqlite3
import os

# Sicherstellen, dass das Verzeichnis existiert
os.makedirs('datenbank/link', exist_ok=True)

# Datenbankverbindung herstellen (erstellt die Datei, wenn sie nicht existiert)
db_path = 'datenbank/link/discord_users.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabelle erstellen, wenn sie nicht existiert
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    discord_id TEXT PRIMARY KEY,
    player_tag TEXT NOT NULL
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

def get_user(discord_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT player_tag FROM users WHERE discord_id = ?
    ''', (discord_id,))
    
    user = cursor.fetchone()
    conn.close()
    return user