import json

with open('app/engine/benchmark_questions.json', 'r') as f:
    questions = json.load(f)

# Define modifications
modifications = {
    "q03": {"question": "What evidence do we have that the wishlist item limit creates friction?", "expected_mode": "partially_answerable"},
    "q09": {"expected_mode": "insufficient_evidence"},
    "q12": {"expected_mode": "insufficient_evidence"},
    "q15": {"expected_mode": "insufficient_evidence"},
    "q23": {"expected_mode": "insufficient_evidence"},
    "q26": {"expected_mode": "partially_answerable"},
    "q28": {"expected_mode": "partially_answerable"},
    "q30": {"expected_mode": "insufficient_evidence"},
    "q35": {"expected_mode": "insufficient_evidence"},
    "q38": {"expected_mode": "partially_answerable"},
    "q39": {"expected_mode": "answerable"},
    "q40": {"question": "Across the 172 conversations, what is the distribution of evidence-quality tiers?", "expected_mode": "answerable"},
    "q56": {"expected_mode": "partially_answerable"},
    "q60": {"question": "Rank the top opportunity areas by evidence volume, while clearly distinguishing direct from indirect evidence.", "expected_mode": "answerable"},
}

# Apply modifications
for q in questions:
    if q["id"] in modifications:
        mods = modifications[q["id"]]
        if "question" in mods:
            q["question"] = mods["question"]
        if "expected_mode" in mods:
            q["expected_mode"] = mods["expected_mode"]

# Add Q61-Q65
new_questions = [
    {"id": "q61", "category": "wishlist behavior", "expected_mode": "partially_answerable", "question": "What evidence directly connects wishlist behavior to purchase decisions?"},
    {"id": "q62", "category": "opportunity identification", "expected_mode": "answerable", "question": "Which problems have the strongest direct evidence versus the highest evidence volume?"},
    {"id": "q63", "category": "non-monetary opportunities", "expected_mode": "partially_answerable", "question": "If Myntra cannot offer discounts, which non-monetary opportunity should we investigate first and why?"},
    {"id": "q64", "category": "opportunity identification", "expected_mode": "answerable", "question": "What additional data would we need to determine which opportunity would have the biggest impact on wishlist-to-purchase conversion?"},
    {"id": "q65", "category": "wishlist behavior", "expected_mode": "answerable", "question": "What can this dataset tell us about wishlist-to-purchase conversion, and what can it not tell us?"}
]

questions.extend(new_questions)

# Validation
ids = set()
question_texts = set()
modes = {"answerable", "partially_answerable", "insufficient_evidence"}

valid = True
errors = []

for q in questions:
    if q["id"] in ids:
        valid = False
        errors.append(f"Duplicate ID: {q['id']}")
    ids.add(q["id"])
    
    if q["question"] in question_texts:
        valid = False
        errors.append(f"Duplicate question text: {q['question']}")
    question_texts.add(q["question"])
    
    if q["expected_mode"] not in modes:
        valid = False
        errors.append(f"Invalid mode in {q['id']}: {q['expected_mode']}")

if valid and len(questions) == 65:
    with open('app/engine/benchmark_questions.json', 'w') as f:
        json.dump(questions, f, indent=2)
    print("SUCCESS: 65 unique questions validated and saved.")
    
    # Generate summary stats
    mode_counts = {"answerable": 0, "partially_answerable": 0, "insufficient_evidence": 0}
    for q in questions:
        mode_counts[q["expected_mode"]] += 1
    
    print(f"Modes: {mode_counts}")
else:
    print(f"FAILED validation. Length: {len(questions)}")
    for e in errors:
        print(e)
