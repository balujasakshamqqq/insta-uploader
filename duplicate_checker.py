import sqlite3

DB_PATH = "queue.db"

def is_duplicate(hash_val):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT 1 FROM videos WHERE hash = ?", (hash_val,)).fetchone()
        return result is not None

def register_hash(hash_val):
    pass