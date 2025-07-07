import sqlite3
import os

DB_FILE = os.getenv("DB_FILE", "db.sqlite3")

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
