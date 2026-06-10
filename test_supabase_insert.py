"""
NotebookLM İçeriklerini Supabase'e Kaydetme Script'i
Kullanım: python test_supabase_insert.py
"""
import json
import os
from datetime import datetime

# Supabase credentials'ı yükle
def load_supabase_credentials():
    """Secrets.toml'dan Supabase bilgilerini yükler."""
    secrets_path = '.streamlit/secrets.toml'
    url = None
    key = None
    
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r', encoding='utf-8') as f:
            for line in f:
                # supabase_url = "..." formatı
                if 'supabase_url' in line.lower() and '=' in line:
                    url = line.split('=', 1)[1].strip().strip('"\'')
                if 'supabase_key' in line.lower() and '=' in line:
                    key = line.split('=', 1)[1].strip().strip('"\'')
    
    return url, key

def main():
    print("=" * 60)
    print("NotebookLM → Supabase İçerik Aktarımı")
    print("=" * 60)
    
    # 1. Supabase bağlantısı
    url, key = load_supabase_credentials()
    
    if not url or not key:
        print("❌ Supabase credentials bulunamadı!")
        print("   .streamlit/secrets.toml dosyasını kontrol edin.")
        return
    
    print(f"✅ Supabase URL: {url[:40]}...")
    
    try:
        from supabase import create_client
        client = create_client(url, key)
        print("✅ Supabase bağlantısı başarılı")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return
    
    # 2. Çekilen NotebookLM içerikleri
    notebook1_contents = [
        {
            "icerik_id": "NB-CARP-001",
            "icerik_tipi": "guide",
            "baslik": "Sayıları Parçalarına Ayırma Sanatı: Asal Çarpanlara Ayırma Rehberi",
            "notebook_url": "https://notebooklm.google.com/notebook/03c5a26f-1e9f-4082-8bf5-2284b8ef9188",
            "notebooklm_item_name": "Problem Solving Guide",
        },
        {
            "icerik_id": "NB-CARP-002",
            "icerik_tipi": "infographic",
            "baslik": "Sayıların Anatomisi Çarpanlar ve Katlar",
            "notebook_url": "https://notebooklm.google.com/notebook/03c5a26f-1e9f-4082-8bf5-2284b8ef9188",
            "notebooklm_item_name": "Infographic",
        },
        {
            "icerik_id": "NB-CARP-003",
            "icerik_tipi": "guide",
            "baslik": "Çarpanlar ve Katlar Hızlı Rehber",
            "notebook_url": "https://notebooklm.google.com/notebook/03c5a26f-1e9f-4082-8bf5-2284b8ef9188",
            "notebooklm_item_name": "Quick Guide",
        },
        {
            "icerik_id": "NB-CARP-004",
            "icerik_tipi": "quiz",
            "baslik": "Çarpanlar Sınavı",
            "notebook_url": "https://notebooklm.google.com/notebook/03c5a26f-1e9f-4082-8bf5-2284b8ef9188",
            "notebooklm_item_name": "Quiz",
        },
        {
            "icerik_id": "NB-CARP-005",
            "icerik_tipi": "video",
            "baslik": "Sayı Şifrelerini Kırmak",
            "video_url": "https://lh3.googleusercontent.com/notebooklm/AG60hOpjCuMaERkNYpOccoeussLSLvY41I47zdnAJuGAXcqNbOmpw32snwSmSMzY__Om_XYOY3JmKUccTYxzGqg37nbVTBnl_bs-5w_yukApUiiETHLFdwRjkxmVWvyVnAl2w5JtxKXT5aaBWfRAgEw97arsJHlj-w=m22",
            "notebook_url": "https://notebooklm.google.com/notebook/03c5a26f-1e9f-4082-8bf5-2284b8ef9188",
            "notebooklm_item_name": "Deep Dive Video",
            "tahmini_sure_dk": 6,
        },
        {
            "icerik_id": "NB-CARP-006",
            "icerik_tipi": "flashcard",
            "baslik": "Çarpanlar Kartları",
            "notebook_url": "https://notebooklm.google.com/notebook/03c5a26f-1e9f-4082-8bf5-2284b8ef9188",
            "notebooklm_item_name": "Flashcards",
            "icerik_json": {"card_count": 50},
        },
    ]
    
    notebook2_contents = [
        {
            "icerik_id": "NB-USLU-001",
            "icerik_tipi": "quiz",
            "baslik": "Gösterim Testi",
            "notebook_url": "https://notebooklm.google.com/notebook/32634984-6023-4c94-bd51-c455afa2c61c",
            "notebooklm_item_name": "Quiz",
        },
        {
            "icerik_id": "NB-USLU-002",
            "icerik_tipi": "video",
            "baslik": "Bilimsel Gösterim Kodu",
            "video_url": "https://lh3.googleusercontent.com/notebooklm/AG60hOooy-FSA2uxmvmHFod541TBvU5HsqGcKTH4ev0ud8D3m_kRNS14pi_jzaSOXoFx0HMFpYFXfOmkP3qk4hmkZqWl9dH7H2UAF2od9c4CA5vS-3LqXGTdi2WtZ6_87BYCAWUv4hAme1p7oEgRV9Z5xk6nQIy5umY=m22",
            "notebook_url": "https://notebooklm.google.com/notebook/32634984-6023-4c94-bd51-c455afa2c61c",
            "notebooklm_item_name": "Deep Dive Video",
            "tahmini_sure_dk": 6,
        },
        {
            "icerik_id": "NB-USLU-003",
            "icerik_tipi": "infographic",
            "baslik": "Powers of Ten Scaling Reality",
            "notebook_url": "https://notebooklm.google.com/notebook/32634984-6023-4c94-bd51-c455afa2c61c",
            "notebooklm_item_name": "Infographic",
        },
        {
            "icerik_id": "NB-USLU-004",
            "icerik_tipi": "flashcard",
            "baslik": "Üslü Kartlar",
            "notebook_url": "https://notebooklm.google.com/notebook/32634984-6023-4c94-bd51-c455afa2c61c",
            "notebooklm_item_name": "Flashcards",
            "icerik_json": {"card_count": 44},
        },
        {
            "icerik_id": "NB-USLU-005",
            "icerik_tipi": "guide",
            "baslik": "Sayıların Süper Gücü: Bilimsel Gösterim",
            "notebook_url": "https://notebooklm.google.com/notebook/32634984-6023-4c94-bd51-c455afa2c61c",
            "notebooklm_item_name": "Chart Guide",
        },
    ]
    
    all_contents = notebook1_contents + notebook2_contents
    
    # 3. Varsayılan alanları ekle
    for content in all_contents:
        content["kaynak_tipi"] = "notebooklm"
        content["status"] = "approved"
        content["active"] = True
        if "icerik_json" in content and isinstance(content["icerik_json"], dict):
            content["icerik_json"] = json.dumps(content["icerik_json"])
    
    # 4. Supabase'e kaydet
    print(f"\n📥 {len(all_contents)} içerik kaydediliyor...")
    
    success_count = 0
    for content in all_contents:
        try:
            result = client.table('icerikler').upsert(content).execute()
            if result.data:
                success_count += 1
                print(f"   ✅ {content['baslik'][:40]}...")
        except Exception as e:
            print(f"   ❌ {content['baslik'][:30]}: {e}")
    
    print(f"\n{'=' * 60}")
    print(f"📊 SONUÇ: {success_count}/{len(all_contents)} içerik kaydedildi")
    print("=" * 60)
    
    # 5. Doğrulama - kayıtları oku
    print("\n🔍 Doğrulama - Supabase'den okuma:")
    try:
        result = client.table('icerikler').select('icerik_id, baslik, icerik_tipi').execute()
        print(f"   Toplam kayıt: {len(result.data)}")
        for row in result.data[:5]:
            print(f"   - [{row['icerik_tipi']}] {row['baslik'][:40]}")
        if len(result.data) > 5:
            print(f"   ... ve {len(result.data) - 5} kayıt daha")
    except Exception as e:
        print(f"   ❌ Okuma hatası: {e}")

if __name__ == "__main__":
    main()
