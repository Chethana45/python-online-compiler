import sqlite3

conn = sqlite3.connect("users.db")

cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

# PROGRAM FILES TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS programs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
filename TEXT,
code TEXT
)
""")

conn.commit()

conn.close()