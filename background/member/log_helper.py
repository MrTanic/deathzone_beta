from datetime import datetime

LOG_FILE_PATH = "datenbank/logs/member/member.log"  # Pfad zur Log-Datei

class LogHelper:
    @staticmethod
    def log_to_file(message):
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"{datetime.now()}: {message}\n")