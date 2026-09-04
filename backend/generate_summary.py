import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('data/myntra_copilot.db')
query = """
SELECT 
    s.platform as source,
    a.validation_status,
    a.shopping_stage,
    a.primary_barrier_category,
    a.secondary_barriers,
    a.behavior,
    a.product_category
FROM analyses a 
JOIN conversations c ON a.conversation_id = c.id 
JOIN sources s ON c.source_id = s.id 
WHERE a.validation_status IN (
    'validated_relevant',
    'ai_direct_evidence',
    'indirect_pre_purchase',
    'ai_indirect_evidence',
    'ai_unvalidated',
    'needs_review'
)
"""
df = pd.read_sql_query(query, conn)

def get_breakdown(col):
    return df[col].value_counts().to_dict()

summary = {
    "total_valid_records": len(df),
    "by_source": get_breakdown('source'),
    "by_validation_status": get_breakdown('validation_status'),
    "by_shopping_stage": get_breakdown('shopping_stage'),
    "by_primary_barrier": get_breakdown('primary_barrier_category'),
    "by_secondary_barrier": get_breakdown('secondary_barriers'),
    "by_behavior_type": get_breakdown('behavior'),
    "by_product_category": get_breakdown('product_category')
}

with open("summary_output.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total records found: {len(df)}")
