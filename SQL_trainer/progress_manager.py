import sqlite3
import os

STATE_DB_PATH = "app_state.db"

def init_state_db():
    conn = sqlite3.connect(STATE_DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS completed_missions (
                    mission_id INTEGER PRIMARY KEY,
                    completion_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

def mark_mission_completed(mission_id: int):
    conn = sqlite3.connect(STATE_DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO completed_missions (mission_id) VALUES (?)', (mission_id,))
    conn.commit()
    conn.close()

def is_mission_completed(mission_id: int) -> bool:
    if not os.path.exists(STATE_DB_PATH):
        return False
        
    conn = sqlite3.connect(STATE_DB_PATH)
    c = conn.cursor()
    
    # Obsługa błędu gdy plik istnieje, ale tabela jeszcze nie (bo użytkownik odpalił najpierw curriculum)
    try:
        c.execute('SELECT 1 FROM completed_missions WHERE mission_id = ?', (mission_id,))
        res = c.fetchone()
    except sqlite3.OperationalError:
        res = None
        
    conn.close()
    return res is not None

def get_all_completed() -> set:
    if not os.path.exists(STATE_DB_PATH):
        return set()
        
    conn = sqlite3.connect(STATE_DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT mission_id FROM completed_missions')
        res = {row[0] for row in c.fetchall()}
    except sqlite3.OperationalError:
        res = set()
    conn.close()
    return res
