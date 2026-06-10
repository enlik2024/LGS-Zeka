import os
import shutil

RAW_DIR = "raw_videos"
NEW_NAME = "Uslu_Ifadeler.mp4"

def rename_and_process():
    if not os.path.exists(RAW_DIR):
        print("Raw dir not found")
        return

    # Find the specific input file
    target_input = "Üslü_Sayılar.mp4"
    files = [f for f in os.listdir(RAW_DIR) if f == target_input]
    
    if not files:
        # Fallback: maybe it's already renamed?
        files = [f for f in os.listdir(RAW_DIR) if f == NEW_NAME]
        if not files:
            print(f"File '{target_input}' not found in raw_videos")
            return
        print(f"File already renamed to {NEW_NAME}")
        current_file = NEW_NAME
    else:
        current_file = files[0]

    old_path = os.path.join(RAW_DIR, current_file)
    new_path = os.path.join(RAW_DIR, NEW_NAME)
    
    if current_file != NEW_NAME:
        print(f"Renaming '{current_file}' to '{NEW_NAME}'...")
        os.rename(old_path, new_path)
    else:
        print(f"File already named '{NEW_NAME}'")

    print("Starting processing...")
    # Import and run processing
    import process_videos
    process_videos.process_videos()

if __name__ == "__main__":
    rename_and_process()
