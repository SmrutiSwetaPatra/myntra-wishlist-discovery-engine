import sqlite3
db = sqlite3.connect('myntra_copilot.db')
cursor = db.execute("SELECT DISTINCT shopping_stage FROM analyses WHERE validation_status IN ('validated_relevant', 'indirect_pre_purchase', 'ai_direct_evidence', 'ai_indirect_evidence')")
print([row[0] for row in cursor.fetchall()])
