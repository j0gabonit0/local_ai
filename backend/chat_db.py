import sqlite3
from datetime import datetime

conn = sqlite3.connect("chat.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    role TEXT,
    message TEXT,
    timestamp TEXT
)
""")

def save_message(user, role, message):
    conn.execute(
        "INSERT INTO messages (user, role, message, timestamp) VALUES (?, ?, ?, ?)",
        (user, role, message, datetime.utcnow().isoformat())
    )
    conn.commit()

def get_history(user):
    cursor = conn.execute(
        "SELECT role, message FROM messages WHERE user=? ORDER BY id ASC",
        (user,)
    )
    return cursor.fetchall()
