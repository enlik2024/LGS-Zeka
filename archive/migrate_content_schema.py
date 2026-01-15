import pandas as pd
import csv
import os
from datetime import datetime

def migrate():
    filename = "content.csv"
    if not os.path.exists(filename):
        print("content.csv not found.")
        return

    # 1. Read existing valid rows (Old Schema)
    # We use csv reader to handle the mismatch manually
    old_rows = []
    new_rows = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"Old Header ({len(header)}): {header}")
        
        for row in reader:
            if len(row) == 13:
                old_rows.append(row)
            elif len(row) == 19:
                new_rows.append(row)
            else:
                print(f"Skipping row with {len(row)} columns.")

    # 2. Define New Header
    new_header = [
        "content_id", "lesson", "topic", "subtopic", "publisher", "source_type", 
        "content_type", "difficulty_band", "estimated_time_min", 
        "summary_bullets", "strategy_steps", "common_mistakes", 
        "mini_check_stem", "mini_check_options_json", "mini_check_correct_option", 
        "page_ref", "status", "active", "created_at"
    ]
    
    # 3. Map Old Rows to New Schema
    # Old: content_id,lesson,topic,subtopic,content_type,source_type,summary_bullets,strategy_steps,common_mistakes,mini_check_question,mini_check_answer,active,status
    mapped_rows = []
    for r in old_rows:
        mapped = {
            "content_id": r[0],
            "lesson": r[1],
            "topic": r[2],
            "subtopic": r[3],
            "publisher": "Manuel", # Default
            "source_type": r[5],
            "content_type": r[4],
            "difficulty_band": 3, # Default
            "estimated_time_min": 5, # Default
            "summary_bullets": r[6],
            "strategy_steps": r[7],
            "common_mistakes": r[8],
            "mini_check_stem": r[9],
            "mini_check_options_json": "{}",
            "mini_check_correct_option": r[10],
            "page_ref": "",
            "status": r[12],
            "active": r[11],
            "created_at": datetime.now().isoformat()
        }
        # Convert dict to list in order
        row_list = [mapped.get(col, "") for col in new_header]
        mapped_rows.append(row_list)
        
    # 4. Process New Rows (Already in New Schema format, just need to ensure order if they match)
    # Assuming new rows match the new header order exactly because they were written by the new code
    final_rows = mapped_rows + new_rows
    
    # 5. Write to CSV with proper quoting
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL) # Safer quoting
        writer.writerow(new_header)
        writer.writerows(final_rows)
        
    print(f"Migration complete. Total rows: {len(final_rows)}")

if __name__ == "__main__":
    migrate()
