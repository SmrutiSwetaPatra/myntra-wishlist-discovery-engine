import sqlite3
import json

def run_audit():
    conn = sqlite3.connect('data/myntra_copilot.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Database Accounting Audit
    print("--- DATABASE ACCOUNTING AUDIT ---")
    
    cur.execute("SELECT count(DISTINCT conversation_id) FROM analyses WHERE model_name = 'gemini-3.5-flash-lite'")
    unique_3_5 = cur.fetchone()[0]
    print(f"Unique conversations with gemini-3.5-flash-lite: {unique_3_5}")
    
    cur.execute("SELECT count(DISTINCT conversation_id) FROM analyses")
    unique_any = cur.fetchone()[0]
    print(f"Unique conversations with any analysis: {unique_any}")
    
    cur.execute("SELECT model_name, count(*) FROM analyses GROUP BY model_name")
    models = cur.fetchall()
    print("Analyses by model:")
    for m in models:
        print(f"  {m[0]}: {m[1]}")
        
    cur.execute("SELECT conversation_id, count(*) FROM analyses GROUP BY conversation_id HAVING count(*) > 1")
    multiples = cur.fetchall()
    print(f"Conversations with >1 analysis: {len(multiples)}")
    if multiples:
        print("  e.g.,", multiples[:3])
        
    cur.execute("SELECT count(*) FROM conversations")
    total_conv = cur.fetchone()[0]
    print(f"Total conversations in DB: {total_conv}")
    
    print("\n--- RELEVANT RECORDS (gemini-3.5-flash-lite) ---")
    # Fetch exactly the gemini-3.5-flash-lite relevant ones
    cur.execute("""
        SELECT a.*, c.raw_content, c.source_url 
        FROM analyses a
        JOIN conversations c ON a.conversation_id = c.id
        WHERE a.relevance = 'True' AND a.model_name = 'gemini-3.5-flash-lite'
    """)
    relevant = cur.fetchall()
    print(f"Found {len(relevant)} relevant records.")
    
    out_data = []
    for r in relevant:
        d = dict(r)
        out_data.append(d)
        
    with open('audit_records.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, indent=2)
        
    print("Data saved to audit_records.json")
        
    conn.close()

if __name__ == '__main__':
    run_audit()
