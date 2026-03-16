import sqlite3
import json

DB_NAME = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            channel_id TEXT,
            template TEXT DEFAULT "Today's Gold is {gold} and Euro is {euro}",
            interval INTEGER DEFAULT 60,
            schedule_times TEXT,
            currency TEXT DEFAULT "EUR",
            is_active INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user_settings(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        # Create default entry if user doesn't exist
        cursor.execute("INSERT INTO user_settings (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
    res = dict(row)
    conn.close()
    return res

def update_user_setting(user_id, column, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Ensure user exists first
    get_user_settings(user_id)
    
    query = f"UPDATE user_settings SET {column} = ? WHERE user_id = ?"
    cursor.execute(query, (value, user_id))
    conn.commit()
    conn.close()

def set_active_status(user_id, status: bool):
    update_user_setting(user_id, "is_active", 1 if status else 0)

# Initialize database on import
init_db()
