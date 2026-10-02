import sqlite3

conn = sqlite3.connect("app_data.db")
try:
    # 2. Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # 3. Create a Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
        )
    """)
    print("Table created successfully.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    # Roll back any changes if something went wrong
    conn.rollback()

finally:
    # 6. Close the connection to free up memory/file locks
    conn.close()
    print("\nDatabase connection closed.")