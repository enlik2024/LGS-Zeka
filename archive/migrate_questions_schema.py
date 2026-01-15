import pandas as pd
import csv
import os
import json
from datetime import datetime

def migrate():
    filename = "questions.csv"
    if not os.path.exists(filename):
        print("questions.csv not found.")
        return

    # 1. Read existing rows
    old_rows = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_rows.append(row)

    # 2. Define New Header
    new_header = [
        "question_id", "question_text", "options_json", "correct_option", 
        "lesson", "topic", "subtopic", "difficulty_label", 
        "question_type", "question_origin", "origin_detail", 
        "derivation_ref", "quality_state", "active", 
        "created_at", "updated_at", "image_url"
    ]
    
    # 3. Map Old Rows to New Schema
    mapped_rows = []
    for r in old_rows:
        # Construct options_json
        options = {
            "A": r.get("option_a", ""),
            "B": r.get("option_b", ""),
            "C": r.get("option_c", ""),
            "D": r.get("option_d", "")
        }
        
        # Determine origin
        old_origin = r.get("question_origin", "UNKNOWN")
        new_origin = "publisher"
        if "MEB" in old_origin.upper():
            new_origin = "meb"
        elif "LGS" in old_origin.upper():
            new_origin = "meb"
            
        mapped = {
            "question_id": r.get("question_id"),
            "question_text": r.get("text"),
            "options_json": json.dumps(options, ensure_ascii=False),
            "correct_option": r.get("correct_answer"),
            "lesson": r.get("lesson"),
            "topic": r.get("topic"),
            "subtopic": r.get("subtopic"),
            "difficulty_label": r.get("difficulty_label"),
            "question_type": "mcq",
            "question_origin": new_origin,
            "origin_detail": old_origin,
            "derivation_ref": "",
            "quality_state": "active",
            "active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "image_url": r.get("image_url", "")
        }
        
        # Convert dict to list in order
        row_list = [mapped.get(col, "") for col in new_header]
        mapped_rows.append(row_list)
        
    # 4. Write to CSV with proper quoting
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(new_header)
        writer.writerows(mapped_rows)
        
    print(f"Questions migration complete. Total rows: {len(mapped_rows)}")

if __name__ == "__main__":
    migrate()
