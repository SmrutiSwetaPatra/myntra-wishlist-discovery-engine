import sqlite3
import pandas as pd

conn = sqlite3.connect('data/myntra_copilot.db')
query = """
SELECT s.platform, a.validation_status, count(*) 
FROM analyses a 
JOIN conversations c ON a.conversation_id = c.id 
JOIN sources s ON c.source_id = s.id 
GROUP BY s.platform, a.validation_status
"""
df = pd.read_sql_query(query, conn)
print(df)
