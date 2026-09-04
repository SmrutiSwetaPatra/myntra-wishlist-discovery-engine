import json

questions = [
    # 1. Wishlist Behavior
    {"id": "q01", "category": "wishlist behavior", "expected_mode": "answerable", "question": "What is the primary function of the wishlist according to user feedback?"},
    {"id": "q02", "category": "wishlist behavior", "expected_mode": "partially_answerable", "question": "How often do users review their wishlist before making a final purchase?"},
    {"id": "q03", "category": "wishlist behavior", "expected_mode": "answerable", "question": "Is the 1000-item wishlist limit a significant barrier for users?"},
    
    # 2. Purchase Barriers
    {"id": "q04", "category": "purchase barriers", "expected_mode": "answerable", "question": "What are the most common pre-purchase barriers mentioned by users?"},
    {"id": "q05", "category": "purchase barriers", "expected_mode": "answerable", "question": "How do non-returnable policies affect purchase decisions?"},
    {"id": "q06", "category": "purchase barriers", "expected_mode": "partially_answerable", "question": "Are shipping delays a major pre-purchase barrier compared to quality issues?"},
    
    # 3. Purchase Intent
    {"id": "q07", "category": "purchase intent", "expected_mode": "answerable", "question": "What issues disrupt users who display high purchase intent?"},
    {"id": "q08", "category": "purchase intent", "expected_mode": "insufficient_evidence", "question": "What percentage of low-intent users eventually convert to high intent within 30 days?"},
    {"id": "q09", "category": "purchase intent", "expected_mode": "partially_answerable", "question": "How does purchase intent differ when buying occasion-wear vs casual wear?"},

    # 4. Purchase Postponement
    {"id": "q10", "category": "purchase postponement", "expected_mode": "answerable", "question": "Why do users intentionally postpone their purchases?"},
    {"id": "q11", "category": "purchase postponement", "expected_mode": "answerable", "question": "Is price the only reason users postpone purchases, or are there other factors?"},
    {"id": "q12", "category": "purchase postponement", "expected_mode": "partially_answerable", "question": "Do users postpone purchases longer for high-ticket items?"},

    # 5. Uncertainty
    {"id": "q13", "category": "uncertainty", "expected_mode": "answerable", "question": "What are the main sources of uncertainty users feel before buying?"},
    {"id": "q14", "category": "uncertainty", "expected_mode": "answerable", "question": "How does product authenticity affect user confidence?"},
    {"id": "q15", "category": "uncertainty", "expected_mode": "partially_answerable", "question": "What information would resolve user uncertainty regarding fabric feel?"},

    # 6. Fit/Size
    {"id": "q16", "category": "fit/size", "expected_mode": "answerable", "question": "How do sizing issues prevent users from converting?"},
    {"id": "q17", "category": "fit/size", "expected_mode": "answerable", "question": "What happens when a user's desired size is unavailable but they want to buy?"},
    {"id": "q18", "category": "fit/size", "expected_mode": "partially_answerable", "question": "Are fit issues more prominent in formal wear (suits/blazers) than in casual clothing?"},

    # 7. Price
    {"id": "q19", "category": "price", "expected_mode": "answerable", "question": "How do hidden fees at checkout impact user behavior?"},
    {"id": "q20", "category": "price", "expected_mode": "answerable", "question": "What is the user sentiment regarding price changes during sales events like Independence Day?"},
    {"id": "q21", "category": "price", "expected_mode": "insufficient_evidence", "question": "What exact discount percentage is required to overcome hesitation on suits?"},

    # 8. Quality/Trust
    {"id": "q22", "category": "quality/trust", "expected_mode": "answerable", "question": "How do concerns about counterfeit or used products affect trust?"},
    {"id": "q23", "category": "quality/trust", "expected_mode": "partially_answerable", "question": "Is quality a bigger issue for electronics or apparel on Myntra?"},
    {"id": "q24", "category": "quality/trust", "expected_mode": "answerable", "question": "What trust issues arise from non-returnable policies?"},

    # 9. Comparison Behavior
    {"id": "q25", "category": "comparison behavior", "expected_mode": "answerable", "question": "How do users compare Myntra with competitors like Amazon or Flipkart?"},
    {"id": "q26", "category": "comparison behavior", "expected_mode": "partially_answerable", "question": "Do users primarily compare prices or return policies across platforms?"},
    {"id": "q27", "category": "comparison behavior", "expected_mode": "answerable", "question": "How does the wishlist facilitate comparison shopping?"},

    # 10. External Research
    {"id": "q28", "category": "external research", "expected_mode": "answerable", "question": "What external platforms do users rely on before making a purchase on Myntra?"},
    {"id": "q29", "category": "external research", "expected_mode": "answerable", "question": "Why do users leave the app to do external research?"},
    {"id": "q30", "category": "external research", "expected_mode": "partially_answerable", "question": "Do users research fit issues on YouTube more often than pricing?"},

    # 11. Workarounds
    {"id": "q31", "category": "workarounds", "expected_mode": "answerable", "question": "What workarounds do users employ when they encounter payment issues?"},
    {"id": "q32", "category": "workarounds", "expected_mode": "partially_answerable", "question": "How do users manage their wishlists once they hit the item limit?"},
    {"id": "q33", "category": "workarounds", "expected_mode": "insufficient_evidence", "question": "What is the most common browser extension users install to track Myntra prices?"},

    # 12. User Segmentation
    {"id": "q34", "category": "user segmentation", "expected_mode": "answerable", "question": "How do the barriers faced by users in the 'decision' stage differ from those in the 'discovery' stage?"},
    {"id": "q35", "category": "user segmentation", "expected_mode": "partially_answerable", "question": "Do high-intent users complain more about pricing or delivery times?"},
    {"id": "q36", "category": "user segmentation", "expected_mode": "insufficient_evidence", "question": "Are female shoppers more likely to use the wishlist for comparison than male shoppers?"},

    # 13. Cross-Source Analysis
    {"id": "q37", "category": "cross-source analysis", "expected_mode": "answerable", "question": "Compare the nature of complaints on Google Play versus YouTube."},
    {"id": "q38", "category": "cross-source analysis", "expected_mode": "partially_answerable", "question": "Are trust issues mentioned more frequently on the App Store or YouTube?"},
    {"id": "q39", "category": "cross-source analysis", "expected_mode": "insufficient_evidence", "question": "What is the average star rating of the Google Play reviews in this dataset compared to App Store?"},

    # 14. Quantitative Analysis
    {"id": "q40", "category": "quantitative analysis", "expected_mode": "answerable", "question": "What is the exact count of validated relevant records versus ai_unvalidated records?"},
    {"id": "q41", "category": "quantitative analysis", "expected_mode": "answerable", "question": "What are the top 3 barrier categories by volume across the entire corpus?"},
    {"id": "q42", "category": "quantitative analysis", "expected_mode": "answerable", "question": "What percentage of human-validated evidence mentions price as a primary barrier?"},
    {"id": "q43", "category": "quantitative analysis", "expected_mode": "insufficient_evidence", "question": "Out of 10,000 daily active users, how many abandon due to hidden fees?"},

    # 15. Opportunity Identification
    {"id": "q44", "category": "opportunity identification", "expected_mode": "answerable", "question": "What product opportunities exist to improve the wishlist experience?"},
    {"id": "q45", "category": "opportunity identification", "expected_mode": "answerable", "question": "Based on sizing friction, what feature could be implemented to increase conversion?"},
    {"id": "q46", "category": "opportunity identification", "expected_mode": "partially_answerable", "question": "Identify an opportunity to reduce purchase postponement related to sales events."},

    # 16. Non-Monetary Opportunities
    {"id": "q47", "category": "non-monetary opportunities", "expected_mode": "answerable", "question": "What non-monetary solutions could address trust issues regarding product authenticity?"},
    {"id": "q48", "category": "non-monetary opportunities", "expected_mode": "answerable", "question": "How could UI changes resolve uncertainty without offering discounts?"},
    {"id": "q49", "category": "non-monetary opportunities", "expected_mode": "partially_answerable", "question": "What non-monetary strategies could mitigate frustration with non-returnable policies?"},

    # 17. Unsupported/Insufficient-Evidence Questions
    {"id": "q50", "category": "insufficient_evidence", "expected_mode": "insufficient_evidence", "question": "What is the exact wishlist-to-purchase conversion rate?"},
    {"id": "q51", "category": "insufficient_evidence", "expected_mode": "insufficient_evidence", "question": "How many users delete the app after encountering a payment failure?"},
    {"id": "q52", "category": "insufficient_evidence", "expected_mode": "insufficient_evidence", "question": "What is the average age of users complaining about the wishlist limit?"},
    {"id": "q53", "category": "insufficient_evidence", "expected_mode": "insufficient_evidence", "question": "How much revenue is lost annually due to non-returnable policies on suits?"},
    {"id": "q54", "category": "insufficient_evidence", "expected_mode": "insufficient_evidence", "question": "What is the geographic distribution of users who abandon their carts?"},

    # 18. Causal Questions
    {"id": "q55", "category": "causal questions", "expected_mode": "insufficient_evidence", "question": "Does removing the wishlist limit guarantee a 20% increase in sales?"},
    {"id": "q56", "category": "causal questions", "expected_mode": "answerable", "question": "What evidence supports the claim that hidden fees cause cart abandonment?"},
    {"id": "q57", "category": "causal questions", "expected_mode": "partially_answerable", "question": "Do fake reviews directly cause users to buy from competitors?"},
    {"id": "q58", "category": "causal questions", "expected_mode": "insufficient_evidence", "question": "Why does adding a size chart solve all fit-related return issues?"},
    
    # Mix / Edge Cases
    {"id": "q59", "category": "quantitative analysis", "expected_mode": "answerable", "question": "Compare the number of users facing price issues against those facing fit issues."},
    {"id": "q60", "category": "opportunity identification", "expected_mode": "answerable", "question": "Prioritize the top three opportunity areas based strictly on the volume of evidence available."}
]

with open('app/engine/benchmark_questions.json', 'w') as f:
    json.dump(questions, f, indent=2)

print(f"Created {len(questions)} benchmark questions.")
