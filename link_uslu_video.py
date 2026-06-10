
import os
from utils.supabase_client import get_supabase_client

def update_uslu_video():
    supabase = get_supabase_client()
    
    video_url = "https://www.youtube.com/watch?v=7j6Av_KCBto"
    search_term = "Üslü"
    
    # 1. Find the content
    print(f"Searching for content with title like '%{search_term}%'...")
    response = supabase.table("icerikler").select("*").ilike("baslik", f"%{search_term}%").execute()
    
    if not response.data:
        print("❌ Content not found!")
        return

    # Assuming the first match is correct or looking for a video type
    target_content = None
    for item in response.data:
        print(f"Found: {item['baslik']} ({item['icerik_tipi']})")
        if item['icerik_tipi'] == 'video' or 'Üslü İfadeler' in item['baslik']:
             target_content = item
             break
    
    if target_content:
        print(f"✅ Updating '{target_content['baslik']}'...")
        update_res = supabase.table("icerikler") \
            .update({"video_url": video_url}) \
            .eq("id", target_content['id']) \
            .execute()
        print(f"Update Result: {update_res.data}")
        print("🎉 Success! Video linked.")
    else:
        print("❌ Could not pinpoint the correct video content.")

if __name__ == "__main__":
    update_uslu_video()
