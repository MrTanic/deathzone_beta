import sqlite3
import os

# Stellen Sie sicher, dass das Verzeichnis existiert
os.makedirs('datenbank/umfrage/utopia', exist_ok=True)

# Pfad zur Datenbankdatei
db_path = os.path.join('datenbank', 'umfrage', 'utopia', 'ut_cwl_umfrage.db')

def setup_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabelle für CWL Umfragen erstellen
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ut_cwl_umfragen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        coc_name TEXT NOT NULL,
        reaction TEXT CHECK(reaction IN ('ja', 'nein', 'zap', 'nicht reagiert')),
        saison_datum TEXT NOT NULL,
        UNIQUE(message_id, user_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Datenbank erfolgreich eingerichtet!")

if __name__ == "__main__":
    setup_database()