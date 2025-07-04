import sqlite3
from datetime import datetime

DB_PATH = "/data/abd_alrahman/memory.db"

def save_interaction(user_input, bot_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_input TEXT,
            bot_response TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO memory (timestamp, user_input, bot_response)
        VALUES (?, ?, ?)
    ''', (datetime.now().isoformat(), user_input, bot_response))

    conn.commit()
    conn.close()

def recall_memory(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT user_input, bot_response FROM memory ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()

    return rows

