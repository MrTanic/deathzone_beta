import sqlite3
import os

# Datei, in der die Spielerdatenbank gespeichert wird
DB_FILE = "datenbank/player/legend_log/legend_player.db"

def create_database():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Tabelle erstellen
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT NOT NULL UNIQUE
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Spielerdatenbank erfolgreich in {DB_FILE} erstellt.")

# Ausführung der Einrichtung
if __name__ == "__main__":
    create_database()