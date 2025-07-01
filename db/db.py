import sqlite3
import os

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect("db/test_results.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            test_name TEXT,
            status TEXT,
            duration REAL,
            error_message TEXT,
            environment TEXT DEFAULT 'local',
            triggered_by TEXT DEFAULT 'manual',
            run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
