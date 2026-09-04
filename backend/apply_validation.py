import sqlite3
import json

def apply():
    conn = sqlite3.connect('data/myntra_copilot.db')
    cur = conn.cursor()
    
    # 1. Alter table
    try:
        cur.execute("ALTER TABLE analyses ADD COLUMN validation_status VARCHAR")
        print("Added validation_status column.")
    except sqlite3.OperationalError as e:
        print("Column may already exist:", e)
        
    # Map of conversation_id to status
    mappings = {
        # A. Strong wishlist-to-purchase evidence
        "f22ae03e3d894694a532a06fab036514": "validated_relevant",
        
        # B. Strong pre-purchase shopping barrier
        "0dc4cc34ecf3453eba559a039c6aff5c": "indirect_pre_purchase",
        "529509ab55304925b015d256bb2d5c98": "indirect_pre_purchase",
        "299be55d96bb4831b0874da512c700db": "indirect_pre_purchase",
        "a3dd045e21654e47b086a4178f4b7c7d": "indirect_pre_purchase",
        "bd603a71c1af4eb997523c50ce1d88df": "indirect_pre_purchase",
        "abd9a2d9a7194be9822e9c48750c150f": "indirect_pre_purchase",
        
        # C. General shopping issue
        "26bc2f1d785e4eea88f9bd5c380a4e6a": "excluded_general",
        
        # D. Post-purchase issue
        "88c8eb0a0efa4900b9f7a1555582e314": "excluded_post_purchase",
        "7df3d1e0513c4f2d8eb7ef2bd1433200": "excluded_post_purchase",
        "1cca2293ac3a46639943b712e1f090f0": "excluded_post_purchase",
        "5945458a2c4f447f9426204f4deb8397": "excluded_post_purchase",
        "5a7a3dc7f97b456f889e58462dd452aa": "excluded_post_purchase",
        
        # E. Ambiguous
        "e47ad060b5ec448091672a330f4015fd": "excluded_ambiguous",
        "4fb4ee214cf448708362f43a3364eb66": "excluded_ambiguous",
        "aa5f003b38f841c69afdeda6f3b7cae4": "excluded_ambiguous",
        "336d9d0533564dad872789858071e943": "excluded_ambiguous",
    }
    
    # 2. Update statuses
    # We only care about gemini-3.5-flash-lite records
    for conv_id, status in mappings.items():
        cur.execute(
            "UPDATE analyses SET validation_status = ? WHERE conversation_id = ? AND model_name = 'gemini-3.5-flash-lite'",
            (status, conv_id)
        )
        
    conn.commit()
    print("Updated statuses.")
    
    # 3. Output summary
    cur.execute("SELECT count(*) FROM analyses WHERE validation_status IN ('validated_relevant', 'indirect_pre_purchase')")
    included_count = cur.fetchone()[0]
    print(f"\nFinal included records: {included_count}")
    
    cur.execute("SELECT count(*) FROM analyses WHERE validation_status LIKE 'excluded_%'")
    excluded_count = cur.fetchone()[0]
    print(f"Excluded records: {excluded_count}")
    
    # Let's extract the summary stats for the included ones
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT a.*, c.source_url 
        FROM analyses a
        JOIN conversations c ON a.conversation_id = c.id
        WHERE a.validation_status IN ('validated_relevant', 'indirect_pre_purchase')
    """)
    included_rows = cur.fetchall()
    
    import collections
    sources = collections.Counter()
    barriers = collections.Counter()
    stages = collections.Counter()
    intents = collections.Counter()
    wishlist = collections.Counter()
    confidences = collections.Counter()
    
    for r in included_rows:
        if 'youtube.com' in r['source_url']:
            sources['YouTube'] += 1
        elif 'play.google' in r['source_url']:
            sources['Google Play'] += 1
        elif 'apple.com' in r['source_url']:
            sources['App Store'] += 1
            
        barriers[r['primary_barrier_category']] += 1
        stages[r['shopping_stage']] += 1
        intents[r['purchase_intent']] += 1
        wishlist[r['wishlist_intent']] += 1
        confidences[r['ai_confidence']] += 1

    print("\n--- Summary of 7 Included Records ---")
    print("Sources:", dict(sources))
    print("Barriers:", dict(barriers))
    print("Stages:", dict(stages))
    print("Intents:", dict(intents))
    print("Wishlist Behavior:", dict(wishlist))
    print("Confidence Scores:", dict(confidences))
    
    conn.close()

if __name__ == '__main__':
    apply()
