import sqlite3

def run():
    conn = sqlite3.connect('data/myntra_copilot.db')
    cur = conn.cursor()
    cur.execute("SELECT conversation_id, model_name FROM analyses WHERE relevance='True'")
    rows = cur.fetchall()
    
    print('Total true rows:', len(rows))
    print('Unique true convs:', len(set([r[0] for r in rows])))
    
    # Also let's print how many are 3.6-flash vs 3.5-flash-lite
    for model in ['gemini-3.5-flash-lite', 'gemini-3.6-flash']:
        cur.execute(f"SELECT count(*) FROM analyses WHERE relevance='True' AND model_name='{model}'")
        count = cur.fetchone()[0]
        print(f"True in {model}: {count}")

if __name__ == '__main__':
    run()
