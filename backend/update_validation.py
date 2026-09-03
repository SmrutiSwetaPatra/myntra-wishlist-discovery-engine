import sqlite3

def update_db():
    conn = sqlite3.connect('data/myntra_copilot.db')
    cur = conn.cursor()
    cur.execute("UPDATE analyses SET validation_status = 'ai_unvalidated' WHERE validation_status IS NULL")
    conn.commit()
    print("Updated validation statuses to 'ai_unvalidated'.")
    conn.close()

if __name__ == '__main__':
    update_db()
