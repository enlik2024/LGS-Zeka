"""
Supabase Client
Streamlit Cloud + Supabase entegrasyonu için client.
"""
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    """
    Supabase client'ı oluşturur ve cache'ler.
    Secrets'tan URL ve Key okur.
    """
    url = None
    key = None
    
    try:
        # 1. Root level büyük harf
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except KeyError:
        try:
            # 2. Root level küçük harf
            url = st.secrets["supabase_url"]
            key = st.secrets["supabase_key"]
        except KeyError:
            try:
                # 3. [supabase] section içinde
                url = st.secrets["supabase"]["url"]
                key = st.secrets["supabase"]["key"]
            except (KeyError, TypeError):
                pass
    
    if not url or not key:
        st.warning("""
        ⚠️ **Supabase credentials eksik!**
        
        `.streamlit/secrets.toml` dosyasına şu satırları ekleyin:
        ```
        supabase_url = "https://xxx.supabase.co"
        supabase_key = "eyJ..."
        ```
        """)
        print(f"DEBUG: Available secrets keys: {list(st.secrets.keys())}")
        return None
    
    print(f"DEBUG: Supabase bağlantısı kuruldu: {url[:40]}...")
    return create_client(url, key)

def check_connection():
    """Supabase bağlantısını test eder."""
    try:
        client = get_supabase()
        if client:
            result = client.table('questions').select('question_id').limit(1).execute()
            return True, "Bağlantı başarılı!"
    except Exception as e:
        return False, str(e)
    return False, "Client oluşturulamadı"
