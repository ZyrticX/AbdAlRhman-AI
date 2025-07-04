import sqlite3
import json

def init_db():
    conn = sqlite3.connect("memory.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        data TEXT,
        mood_score FLOAT
    )''')
    conn.commit()
    conn.close()

def save_memory(event: dict, mood: float):
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("INSERT INTO memory (data, mood_score) VALUES (?, ?)", 
              (json.dumps(event), mood))
    conn.commit()
    conn.close()
