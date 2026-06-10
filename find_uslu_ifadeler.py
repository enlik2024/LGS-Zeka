
import os
from utils.supabase_client import get_supabase_client

def find_content():
    supabase = get_supabase_client()
    
    # Search for implicit title
    response = supabase.table("icerikler").select("*").ilike("baslik", "%Üslü%").execute()
    
    print("Found contents:")
    for item in response.data:
        print(f"- {item['baslik']} (ID: {item.get('id')}, Type: {item.get('icerik_tipi')})")

if __name__ == "__main__":
    find_content()
