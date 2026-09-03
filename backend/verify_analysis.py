import asyncio
import os
import sqlite3
from collections import Counter
from app.core.config import settings

def run_verification():
    db_path = os.path.join(os.path.dirname(__file__), settings.SQLITE_DB_PATH)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Total conversations
    cur.execute("SELECT count(*) FROM conversations")
    total_convs = cur.fetchone()[0]

    # 2-10: We need to parse the log file for some metrics
    log_file = r"C:\Users\smrut\.gemini\antigravity-ide\brain\72de0eab-a134-4c2a-9b9e-c2acdc2d9d9f\.system_generated\tasks\task-729.log"
    with open(log_file, 'r', encoding='utf-8') as f:
        log_text = f.read()
    
    attempted = log_text.count("Processing conversation")
    failed_429 = log_text.count("RESOURCE_EXHAUSTED")
    failed_schema = log_text.count("validation error")
    
    cur.execute("SELECT count(*) FROM analyses")
    total_analyses = cur.fetchone()[0]
    
    cur.execute("SELECT count(*) FROM analyses WHERE relevance = 'True'")
    relevant_analyses = cur.fetchone()[0]
    
    cur.execute("SELECT count(*) FROM analyses WHERE relevance = 'False'")
    irrelevant_analyses = cur.fetchone()[0]
    
    # Check for foreign key validity
    cur.execute("SELECT count(*) FROM analyses WHERE conversation_id NOT IN (SELECT id FROM conversations)")
    invalid_fks = cur.fetchone()[0]
    
    # Check duplicates
    cur.execute("SELECT conversation_id, model_name, prompt_version, count(*) FROM analyses GROUP BY conversation_id, model_name, prompt_version HAVING count(*) > 1")
    duplicates = len(cur.fetchall())
    
    # Models, schemas
    cur.execute("SELECT DISTINCT model_name, prompt_version, schema_version FROM analyses")
    models_used = cur.fetchall()
    
    print("--- VERIFICATION REPORT ---")
    print(f"1. Total conversations: {total_convs}")
    print(f"2. Total attempted by pipeline: {attempted}")
    print(f"3. Total successfully processed by Relevance Gate: {total_analyses}")
    print(f"4. Relevant conversations (where Deep Analysis was performed): {relevant_analyses}")
    print(f"5. Irrelevant conversations: {irrelevant_analyses}")
    print(f"6. Deep Analysis records successfully created: {relevant_analyses}")
    print(f"7. Records skipped because of cache: (Derived) {total_convs - attempted}")
    print(f"8. Records failed (due to 429 or other errors): {attempted - total_analyses}")
    print(f"9. Number of 429/API errors in log: {failed_429}")
    print(f"10. Number of Pydantic/schema validation failures in log: {failed_schema}")
    print(f"11,12. Models and versions in DB: {models_used}")
    print(f"13. Invalid Foreign Keys: {invalid_fks}")
    print(f"14. Duplicate Analysis records: {duplicates}")
    
    # Distributions
    def print_dist(name, col, table="analyses"):
        if table == "analyses":
            cur.execute(f"SELECT {col}, count(*) FROM {table} WHERE relevance = 'True' GROUP BY {col} ORDER BY count(*) DESC")
        else:
            cur.execute(f"SELECT {col}, count(*) FROM {table} GROUP BY {col} ORDER BY count(*) DESC")
        dist = cur.fetchall()
        print(f"\n{name} Distribution:")
        for k, v in dist:
            print(f"  {k}: {v}")

    print_dist("Source", "source_url", "conversations")
    print_dist("Relevance", "relevance")
    print_dist("Purchase Intent", "purchase_intent")
    print_dist("Shopping Stage", "shopping_stage")
    print_dist("Primary Barrier Category", "primary_barrier_category")
    print_dist("Primary Barrier Detail", "primary_barrier_detail")
    print_dist("Secondary Barriers", "secondary_barriers")
    print_dist("Uncertainty", "uncertainty")
    print_dist("Behavior Type", "behavior")
    print_dist("Product Category", "product_category")
    print_dist("Occasion", "occasion")
    print_dist("Comparison Behavior", "comparison_behavior")
    print_dist("External Research", "external_research")
    print_dist("Workaround", "workaround")
    print_dist("Desired Information", "desired_information")
    print_dist("Unmet Need", "unmet_need")
    
    conn.close()

if __name__ == '__main__':
    run_verification()
