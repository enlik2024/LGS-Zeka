import pandas as pd
import csv
import os
from datetime import datetime

def migrate():
    filename = "content.csv"
    if not os.path.exists(filename):
        print("content.csv not found.")
        return

    # 1. Read existing rows
    old_rows = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_rows.append(row)

    # 2. Define New Header (Added derivation_ref)
    new_header = [
        "content_id", "lesson", "topic", "subtopic", "publisher", "source_type", 
        "content_type", "difficulty_band", "estimated_time_min", 
        "summary_bullets", "strategy_steps", "common_mistakes", 
        "mini_check_stem", "mini_check_options_json", "mini_check_correct_option", 
        "page_ref", "status", "active", "created_at", "derivation_ref"
    ]
    
    # 3. Map Old Rows to New Schema
    mapped_rows = []
    for r in old_rows:
        mapped = {
            "content_id": r.get("content_id"),
            "lesson": r.get("lesson"),
            "topic": r.get("topic"),
            "subtopic": r.get("subtopic"),
            "publisher": r.get("publisher"),
            "source_type": r.get("source_type"),
            "content_type": r.get("content_type"),
            "difficulty_band": r.get("difficulty_band"),
            "estimated_time_min": r.get("estimated_time_min"),
            "summary_bullets": r.get("summary_bullets"),
            "strategy_steps": r.get("strategy_steps"),
            "common_mistakes": r.get("common_mistakes"),
            "mini_check_stem": r.get("mini_check_stem"),
            "mini_check_options_json": r.get("mini_check_options_json"),
            "mini_check_correct_option": r.get("mini_check_correct_option"),
            "page_ref": r.get("page_ref"),
            "status": r.get("status"),
            "active": r.get("active"),
            "created_at": r.get("created_at"),
            "derivation_ref": "" # New field
        }
        
        # Convert dict to list in order
        row_list = [mapped.get(col, "") for col in new_header]
        mapped_rows.append(row_list)
        
    # 4. Write to CSV with proper quoting
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(new_header)
        writer.writerows(mapped_rows)
        
    print(f"Content migration v2 complete. Total rows: {len(mapped_rows)}")

if __name__ == "__main__":
    migrate()
