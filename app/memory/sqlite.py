import sqlite3
import os

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "app/db/memory.db")

def get_sqlite_connection():
    return sqlite3.connect(SQLITE_DB_PATH)
