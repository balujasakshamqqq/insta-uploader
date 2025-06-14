import sqlite3

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect("database.db")

# Read and execute SQL schema
with open("schema.sql", "r") as f:
    conn.executescript(f.read())

conn.close()
print("✅ Database initialized.")
