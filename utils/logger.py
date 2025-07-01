import sqlite3
import os

def log_result(test_name, status, duration, run_id=None, error_message=None, environment="local", triggered_by="manual"):
    db_path = "db/test_results.db"
    if not os.path.exists(db_path):
        raise FileNotFoundError("Database not found. Run db/db.py first.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO test_runs (run_id, test_name, status, duration, error_message, environment, triggered_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (run_id, test_name, status, duration, error_message, environment, triggered_by))

    conn.commit()
    conn.close()
