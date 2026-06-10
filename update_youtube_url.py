
import os
import json
from supabase import create_client, Client
import toml

def update_video_url():
    # Load secrets
    secrets = toml.load('.streamlit/secrets.toml')
    url = secrets['supabase_url']
    key = secrets['supabase_key']
    
    supabase: Client = create_client(url, key)
    
    # Target Video URL
    NEW_VIDEO_URL = "https://www.youtube.com/watch?v=kk42zJbYXUU"
    
    # Identify the content (Assuming it's 'Sayı Şifrelerini Kırmak')
    # We can search by title or icerik_tipi='video'
    print(f"Updating video URL to: {NEW_VIDEO_URL}")
    
    response = supabase.table("icerikler") \
        .update({"video_url": NEW_VIDEO_URL}) \
        .eq("baslik", "Sayı Şifrelerini Kırmak") \
        .execute()
        
    print("Update Response:", response.data)

if __name__ == "__main__":
    update_video_url()
