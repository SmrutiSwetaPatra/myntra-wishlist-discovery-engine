import sqlite3
import pandas as pd
import json
import collections

conn = sqlite3.connect('data/myntra_copilot.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

audit = {}

# 1. DATA COLLECTION
cur.execute("SELECT count(*) FROM conversations")
audit['total_records'] = cur.fetchone()[0]

cur.execute("""
    SELECT s.platform, count(*) 
    FROM conversations c 
    JOIN sources s ON c.source_id = s.id 
    GROUP BY s.platform
""")
audit['source_breakdown'] = {row[0]: row[1] for row in cur.fetchall()}

cur.execute("""
    SELECT count(*) 
    FROM conversations c 
    LEFT JOIN analyses a ON c.id = a.conversation_id 
    WHERE a.id IS NULL OR a.primary_barrier_category IS NULL
""")
audit['collected_not_enriched'] = cur.fetchone()[0]

# 2. AI ENRICHMENT
cur.execute("SELECT count(*) FROM analyses WHERE primary_barrier_category IS NOT NULL")
audit['successfully_analyzed'] = cur.fetchone()[0]

cur.execute("SELECT count(*) FROM analyses WHERE relevance = 'False' OR relevance = 'false'")
audit['failed_analysis'] = cur.fetchone()[0]

cur.execute("SELECT count(*) FROM analyses WHERE primary_barrier_category IS NULL")
audit['missing_invalid_analysis'] = cur.fetchone()[0]

cur.execute("SELECT DISTINCT model_name, model_version FROM analyses")
audit['models_used'] = [dict(row) for row in cur.fetchall()]

cur.execute("SELECT validation_status, count(*) FROM analyses GROUP BY validation_status")
audit['validation_statuses'] = {row[0]: row[1] for row in cur.fetchall()}

# 3. EVIDENCE CLASSIFICATION
# (Already covered by validation_statuses)

# 4. TAXONOMY
cur.execute("SELECT purchase_intent, count(*) FROM analyses GROUP BY purchase_intent")
audit['purchase_intent'] = {row[0]: row[1] for row in cur.fetchall()}

cur.execute("SELECT shopping_stage, count(*) FROM analyses GROUP BY shopping_stage")
audit['shopping_stage'] = {row[0]: row[1] for row in cur.fetchall()}

cur.execute("SELECT primary_barrier_category, count(*) FROM analyses GROUP BY primary_barrier_category")
audit['primary_barrier'] = {row[0]: row[1] for row in cur.fetchall()}

cur.execute("SELECT secondary_barriers, count(*) FROM analyses GROUP BY secondary_barriers")
audit['secondary_barriers'] = {str(row[0]): row[1] for row in cur.fetchall()}

cur.execute("SELECT behavior, count(*) FROM analyses GROUP BY behavior")
audit['behavior_type'] = {row[0]: row[1] for row in cur.fetchall()}

cur.execute("SELECT product_category, count(*) FROM analyses GROUP BY product_category")
audit['product_category'] = {row[0]: row[1] for row in cur.fetchall()}

# 8. FINAL DATA QUALITY
cur.execute("""
    SELECT count(*) FROM conversations 
    WHERE id IN (
        SELECT id FROM conversations GROUP BY raw_content HAVING count(*) > 1
    )
""")
audit['duplicate_records'] = cur.fetchone()[0]

cur.execute("""
    SELECT count(*) FROM conversations 
    WHERE length(raw_content) < 15
""")
audit['short_noisy_records'] = cur.fetchone()[0]

cur.execute("""
    SELECT count(*) FROM analyses 
    WHERE shopping_stage = 'post-purchase' OR primary_barrier_category = 'Post-purchase issue'
""")
audit['post_purchase_records'] = cur.fetchone()[0]

with open("audit_results.json", "w") as f:
    json.dump(audit, f, indent=2)

print("Audit script finished.")
