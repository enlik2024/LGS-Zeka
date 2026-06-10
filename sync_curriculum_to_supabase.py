"""
curriculum_map.csv → Supabase curriculum_map tablosu senkronizasyonu
Bu script yerel CSV'yi Supabase'e yükler.
"""
import csv
import os

def load_supabase_credentials():
    secrets_path = '.streamlit/secrets.toml'
    url = key = None
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'supabase_url' in line.lower() and '=' in line:
                    url = line.split('=', 1)[1].strip().strip('"\'')
                if 'supabase_key' in line.lower() and '=' in line:
                    key = line.split('=', 1)[1].strip().strip('"\'')
    return url, key

def main():
    print("=" * 60)
    print("curriculum_map.csv → Supabase Senkronizasyonu")
    print("=" * 60)
    
    url, key = load_supabase_credentials()
    if not url or not key:
        print("❌ Supabase credentials bulunamadı!")
        return
    
    print(f"✅ Supabase bağlantısı kuruldu")
    
    from supabase import create_client
    client = create_client(url, key)
    
    # 1. CSV'yi oku
    csv_path = 'curriculum_map.csv'
    rows = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            # Supabase için hazırla
            rows.append({
                'id': i,  # Primary key
                'lesson': row['lesson'],
                'topic': row['topic'],
                'subtopic': row['subtopic'],
                'importance_weight': int(row['importance_weight']),
                'active': row['active'].lower() == 'true'
            })
    
    print(f"📚 {len(rows)} satır okundu")
    
    # 2. Mevcut verileri sil
    print("🗑️ Eski veriler siliniyor...")
    try:
        # Tüm mevcut verileri sil
        client.table('curriculum_map').delete().neq('id', 0).execute()
        print("   ✅ Eski veriler silindi")
    except Exception as e:
        print(f"   ⚠️ Silme hatası (tablo boş olabilir): {e}")
    
    # 3. Yeni verileri ekle (batch)
    print("📥 Yeni veriler yükleniyor...")
    
    # 50'şer batch'ler halinde yükle
    batch_size = 50
    success = 0
    
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        try:
            result = client.table('curriculum_map').upsert(batch).execute()
            if result.data:
                success += len(batch)
                print(f"   ✅ Batch {i//batch_size + 1}: {len(batch)} kayıt")
        except Exception as e:
            print(f"   ❌ Batch {i//batch_size + 1}: {e}")
    
    print(f"\n{'=' * 60}")
    print(f"📊 SONUÇ: {success}/{len(rows)} satır yüklendi")
    print("=" * 60)
    
    # 4. Doğrulama
    print("\n🔍 Doğrulama:")
    try:
        result = client.table('curriculum_map').select('lesson').execute()
        # Ders bazlı sayım
        ders_counts = {}
        for row in result.data:
            d = row['lesson']
            ders_counts[d] = ders_counts.get(d, 0) + 1
        
        print(f"   Toplam: {len(result.data)} kayıt")
        for ders, count in sorted(ders_counts.items()):
            print(f"   - {ders}: {count}")
    except Exception as e:
        print(f"   ❌ {e}")
    
    print("\n✅ Streamlit'i yeniden başlatın veya cache temizleyin.")
    print("   st.cache_data.clear() veya tarayıcı yenileme")

if __name__ == "__main__":
    main()
