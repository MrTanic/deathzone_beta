import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Erstelle einen Logger
    logger = logging.getLogger('DeathZone Beta')
    logger.setLevel(logging.DEBUG)  # Ändere das Log-Level zu DEBUG

    # Erstelle einen Ordner für die Logs, falls nicht vorhanden
    log_directory = "datenbank/logs/bot"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Pfad zur Log-Datei
    log_file_path = os.path.join(log_directory, "bot.log")

    # Erstelle einen Handler, der Log-Einträge in eine Datei schreibt, maximal 5 Dateien mit je 5MB
    handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
    handler.setLevel(logging.DEBUG)  # Stelle sicher, dass der Handler ebenfalls Debug-Meldungen erfasst

    # Erstelle einen Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Füge den Handler zum Logger hinzu
    logger.addHandler(handler)

    # Konfiguriere zusätzlich einen StreamHandler für die Ausgabe in der Konsole
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Stelle sicher, dass der Console-Handler Debug-Meldungen erfasst
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger