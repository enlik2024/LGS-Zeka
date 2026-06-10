"""
Müfredat Kazanımlarını Supabase'e Yükleme Script'i
curriculum_map.csv → meb_kazanimlar tablosu
"""
import csv
import json
import os
from datetime import datetime

def load_supabase_credentials():
    """Secrets.toml'dan Supabase bilgilerini yükler."""
    secrets_path = '.streamlit/secrets.toml'
    url = None
    key = None
    
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'supabase_url' in line.lower() and '=' in line:
                    url = line.split('=', 1)[1].strip().strip('"\'')
                if 'supabase_key' in line.lower() and '=' in line:
                    key = line.split('=', 1)[1].strip().strip('"\'')
    
    return url, key

def generate_kazanim_id(ders, topic, subtopic, index):
    """Kazanım ID'si oluşturur."""
    # Ders kodu
    ders_kodlari = {
        'Matematik': 'MAT',
        'Fen Bilimleri': 'FEN',
        'Türkçe': 'TUR',
        'T.C. İnkılap Tarihi': 'INK',
        'İngilizce': 'ING',
        'Din Kültürü': 'DIN'
    }
    ders_kodu = ders_kodlari.get(ders, 'OTH')
    
    # ID: MAT-001, MAT-002, vb.
    return f"{ders_kodu}-{index:03d}"

def map_oncelik(importance_weight):
    """Önem ağırlığını seviyeye çevirir."""
    if importance_weight >= 5:
        return 'kritik'
    elif importance_weight >= 4:
        return 'yuksek'
    elif importance_weight >= 3:
        return 'orta'
    else:
        return 'dusuk'

def main():
    print("=" * 60)
    print("Müfredat Kazanımları → Supabase Aktarımı")
    print("=" * 60)
    
    # 1. Supabase bağlantısı
    url, key = load_supabase_credentials()
    
    if not url or not key:
        print("❌ Supabase credentials bulunamadı!")
        return
    
    print(f"✅ Supabase URL: {url[:40]}...")
    
    try:
        from supabase import create_client
        client = create_client(url, key)
        print("✅ Supabase bağlantısı başarılı")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return
    
    # 2. CSV'yi oku
    csv_path = 'curriculum_map.csv'
    kazanimlar = []
    ders_sayaci = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ders = row['lesson']
            topic = row['topic']
            subtopic = row['subtopic']
            importance = int(row['importance_weight'])
            active = row['active'].lower() == 'true'
            
            # Ders bazlı sayaç
            if ders not in ders_sayaci:
                ders_sayaci[ders] = 0
            ders_sayaci[ders] += 1
            
            kazanim_id = generate_kazanim_id(ders, topic, subtopic, ders_sayaci[ders])
            
            kazanim = {
                'kazanim_id': kazanim_id,
                'ders': ders,
                'konu': topic,
                'alt_konu': subtopic,
                'sinif': 8,
                'oncelik_seviyesi': map_oncelik(importance),
                'curriculum_map_subtopic': subtopic,
                'active': active
            }
            kazanimlar.append(kazanim)
    
    print(f"\n📚 {len(kazanimlar)} kazanım okundu")
    print(f"   Derse göre dağılım:")
    for ders, count in ders_sayaci.items():
        print(f"   - {ders}: {count}")
    
    # 3. Supabase'e yükle
    print(f"\n📥 Kazanımlar yükleniyor...")
    
    success_count = 0
    for kaz in kazanimlar:
        try:
            result = client.table('meb_kazanimlar').upsert(kaz).execute()
            if result.data:
                success_count += 1
        except Exception as e:
            print(f"   ❌ {kaz['kazanim_id']}: {e}")
    
    print(f"\n{'=' * 60}")
    print(f"📊 SONUÇ: {success_count}/{len(kazanimlar)} kazanım kaydedildi")
    print("=" * 60)
    
    # 4. Doğrulama
    print("\n🔍 Doğrulama - Supabase'den okuma:")
    try:
        result = client.table('meb_kazanimlar').select('ders, count').execute()
        # Ders bazlı sayım
        ders_counts = {}
        all_records = client.table('meb_kazanimlar').select('ders').execute()
        for row in all_records.data:
            d = row['ders']
            ders_counts[d] = ders_counts.get(d, 0) + 1
        
        print(f"   Toplam: {len(all_records.data)} kayıt")
        for ders, count in ders_counts.items():
            print(f"   - {ders}: {count}")
    except Exception as e:
        print(f"   ❌ Okuma hatası: {e}")
    
    # 5. İçerikleri kazanımlarla eşleştir
    print("\n🔗 İçerikler kazanımlarla eşleştiriliyor...")
    
    # Çarpanlar ve Katlar içerikleri → MAT-001 (EKOK), MAT-002 (EBOB), etc.
    eslesme = [
        # Notebook 1 - Çarpanlar ve Katlar
        ('NB-CARP-001', 'MAT-001'),  # Rehber → Pozitif Tam Sayı Çarpanları
        ('NB-CARP-002', 'MAT-002'),  # İnfografik → EKOK
        ('NB-CARP-003', 'MAT-003'),  # Hızlı Rehber → EBOB
        ('NB-CARP-004', 'MAT-003'),  # Quiz → EBOB
        ('NB-CARP-005', 'MAT-001'),  # Video → Çarpanlar
        ('NB-CARP-006', 'MAT-001'),  # Flashcards → Çarpanlar
        
        # Notebook 2 - Üslü İfadeler
        ('NB-USLU-001', 'MAT-005'),  # Quiz → Tam Sayı Kuvvetleri
        ('NB-USLU-002', 'MAT-012'),  # Video → Bilimsel Gösterim
        ('NB-USLU-003', 'MAT-012'),  # İnfografik → Bilimsel Gösterim
        ('NB-USLU-004', 'MAT-005'),  # Flashcards → Tam Sayı Kuvvetleri
        ('NB-USLU-005', 'MAT-012'),  # Guide → Bilimsel Gösterim
    ]
    
    eslesme_count = 0
    for icerik_id, kazanim_id in eslesme:
        try:
            result = client.table('icerikler').update({
                'kazanim_id': kazanim_id
            }).eq('icerik_id', icerik_id).execute()
            if result.data:
                eslesme_count += 1
                print(f"   ✅ {icerik_id} → {kazanim_id}")
        except Exception as e:
            print(f"   ❌ {icerik_id}: {e}")
    
    print(f"\n📊 {eslesme_count}/{len(eslesme)} içerik eşleştirildi")

if __name__ == "__main__":
    main()
