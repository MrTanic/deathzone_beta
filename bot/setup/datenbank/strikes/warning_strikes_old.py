import sqlite3
import os

# Pfad zur Verwarnungs-Datenbank
db_path = "datenbank/strikes"
db_file = os.path.join(db_path, "warning_strike.db")

# Erstellen des Ordners, falls er nicht existiert
os.makedirs(db_path, exist_ok=True)

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(db_file)

# Einen Cursor erstellen
cursor = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
# Entfernen des UNIQUE Constraints für user_id und clan_name
# Hinzufügen einer AUTOINCREMENT ID
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

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()