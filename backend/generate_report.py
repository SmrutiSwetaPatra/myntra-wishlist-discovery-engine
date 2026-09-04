import sqlite3
import json

def generate_report():
    conn = sqlite3.connect('data/myntra_copilot.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM insights ORDER BY evidence_count DESC")
    insights = cur.fetchall()
    
    report = "# Final AI Discovery Engine Report\n\n"
    
    # 1. number of records aggregated
    cur.execute("SELECT count(*) FROM analyses WHERE validation_status IN ('validated_relevant', 'indirect_pre_purchase')")
    count = cur.fetchone()[0]
    report += f"**Number of Records Aggregated**: {count}\n\n"
    
    # Distributions
    cur.execute("""
        SELECT a.primary_barrier_category, count(*) as cnt 
        FROM analyses a 
        WHERE a.validation_status IN ('validated_relevant', 'indirect_pre_purchase') 
        GROUP BY a.primary_barrier_category
    """)
    barriers = {row[0]: row[1] for row in cur.fetchall()}
    
    cur.execute("""
        SELECT c.source_url 
        FROM analyses a
        JOIN conversations c ON a.conversation_id = c.id
        WHERE a.validation_status IN ('validated_relevant', 'indirect_pre_purchase')
    """)
    sources_raw = cur.fetchall()
    import collections
    sources = collections.Counter()
    for s in sources_raw:
        if 'youtube' in s[0]: sources['YouTube'] += 1
        elif 'play.google' in s[0]: sources['Google Play'] += 1
        else: sources['Apple App Store'] += 1
        
    report += "## Distributions\n"
    report += f"- **Source Distribution**: {dict(sources)}\n"
    report += f"- **Barrier Distribution**: {barriers}\n\n"
    
    report += "## Top Insights\n\n"
    
    for i in insights:
        report += f"### {i['title']}\n"
        report += f"**Category**: {i['category']}\n"
        report += f"**Type**: {i['direct_vs_indirect']}\n"
        report += f"**Confidence Score**: {i['ai_confidence']}\n"
        report += f"**Evidence Count**: {i['evidence_count']}\n"
        report += f"**Sources Present**: {i['sources_present']}\n"
        report += f"**Supporting Conversation IDs**: {i['supporting_conversation_ids']}\n\n"
        report += f"{i['description']}\n\n"
        
    report += """## Evidence Gaps & Limitations
- **Limitations**: The insights are derived from an extremely small, highly-filtered dataset (7 records) out of 172 raw interactions. Statistical significance cannot be claimed.
- **Evidence Gaps**: There is only *one* direct piece of evidence connecting wishlist friction directly to a barrier (the wishlist cap). The other 6 records represent generalized pre-purchase friction (pricing, platform trust, non-returnable policies, and payment methods) that may cause users to abandon their shopping journey, but the direct causal link to wishlist abandonment is inferred.

## Recommended Product Opportunities (Hypotheses to Validate)
1. **Wishlist Cap Relief**: Test increasing the wishlist item limit or offering a "Compare" feature for users who heavily use the wishlist as a shortlisting/comparison tool.
2. **Pricing Transparency**: Evaluate the checkout flow for hidden platform fees and confusing promotional pricing, as these directly cause hesitation compared to competitors.
3. **Apparel Exchange Policies**: Test offering size-exchanges (even for non-returnable categories like Suits and Blazers) or providing better sizing assurance, as the fear of being "stuck" with an ill-fitting item prevents conversion.
4. **Currency & Payment Support**: For international or tech-hesitant users, investigate whether in-app currency conversion or streamlined payment assistance could recover abandoned intent.
"""
    
    with open('final_report.md', 'w') as f:
        f.write(report)
    
    print("Generated final_report.md")

if __name__ == '__main__':
    generate_report()
