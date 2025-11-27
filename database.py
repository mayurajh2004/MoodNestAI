import sqlite3
import datetime

DB_NAME = "mental_health.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table (simple for now, maybe just device ID or session ID)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Chats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sentiment Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score REAL,
            magnitude REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # System Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def log_chat(user_id, role, content):
    conn = get_db_connection()
    conn.execute('INSERT INTO chats (user_id, role, content) VALUES (?, ?, ?)', (user_id, role, content))
    conn.commit()
    conn.close()

def log_sentiment(user_id, score, magnitude):
    conn = get_db_connection()
    conn.execute('INSERT INTO sentiment_logs (user_id, score, magnitude) VALUES (?, ?, ?)', (user_id, score, magnitude))
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=50):
    conn = get_db_connection()
    chats = conn.execute('SELECT * FROM chats WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?', (user_id, limit)).fetchall()
    conn.close()
    return [dict(chat) for chat in chats][::-1]

def get_sentiment_history(user_id):
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM sentiment_logs WHERE user_id = ? ORDER BY timestamp ASC', (user_id,)).fetchall()
    conn.close()
    return [dict(log) for log in logs]
