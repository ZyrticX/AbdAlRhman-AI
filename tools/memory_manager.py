
import sqlite3
from datetime import datetime

def init_chat_memory_db(db_path="memory.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            assistant_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()





import sqlite3

def save_interaction(user_input, assistant_response, db_path="memory.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_input TEXT,
            assistant_response TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO chat_memory (user_input, assistant_response)
        VALUES (?, ?)
    """, (user_input, assistant_response))
    conn.commit()
    conn.close()




def retrieve_recent_memories(limit=5, db_path="memory.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_input, assistant_response FROM chat_memory
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    memories = cursor.fetchall()
    conn.close()
    return memories

