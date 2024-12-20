import sqlite3
import os

class DBConnection:
    def __init__(self, db_paths):
        self.db_paths = db_paths

    def get_db_connection(self, clan):
        return sqlite3.connect(self.db_paths[clan])