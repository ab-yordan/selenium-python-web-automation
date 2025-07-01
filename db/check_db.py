import sqlite3

def show_all_results():
    conn = sqlite3.connect("db/test_results.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM test_runs ORDER BY run_time DESC")
    rows = cursor.fetchall()

    print("\n== Test Results ==")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Run ID       : {row[1]}")
        print(f"Test Name    : {row[2]}")
        print(f"Status       : {row[3]}")
        print(f"Duration     : {row[4]}s")
        print(f"Error Message: {row[5]}")
        print(f"Environment  : {row[6]}")
        print(f"Triggered By : {row[7]}")
        print(f"Run Time     : {row[8]}")
        print("-" * 40)

    conn.close()

if __name__ == "__main__":
    show_all_results()
