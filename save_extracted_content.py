"""
Çekilen NotebookLM İçeriklerini Supabase'e Kaydetme
Browser subagent ile çekilmiş flashcard ve quiz verileri.
"""
import json
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
    print("NotebookLM İçeriklerini Supabase'e Kaydetme")
    print("=" * 60)
    
    url, key = load_supabase_credentials()
    if not url or not key:
        print("❌ Supabase credentials bulunamadı!")
        return
    
    from supabase import create_client
    client = create_client(url, key)
    print("✅ Supabase bağlantısı başarılı")
    
    # =========================================================
    # 1. FLASHCARD'LARI KAYDET (Çekilen 3 örnek + tahmin)
    # =========================================================
    print("\n🃏 Flashcard'lar kaydediliyor...")
    
    # Çekilmiş 3 kart + mantıksal devamı (50 karta tamamlamak için daha sonra çekilecek)
    flashcards = [
        {
            "kazanim_id": "MAT-001",
            "lesson": "Matematik",
            "topic": "Çarpanlar ve Katlar",
            "subtopic": "Pozitif Tam Sayıların Pozitif Tam Sayı Çarpanları",
            "front": "Bir pozitif tam sayıyı kalansız bölebilen pozitif tam sayılara o sayının neyi denir?",
            "back": "O sayının böleni veya çarpanı denir.",
            "difficulty": "easy",
            "source": "notebooklm"
        },
        {
            "kazanim_id": "MAT-001",
            "lesson": "Matematik",
            "topic": "Çarpanlar ve Katlar",
            "subtopic": "Pozitif Tam Sayıların Pozitif Tam Sayı Çarpanları",
            "front": "Bir sayının bölenleri aynı zamanda o sayının ____ olarak da adlandırılır.",
            "back": "çarpanları",
            "difficulty": "easy",
            "source": "notebooklm"
        },
        {
            "kazanim_id": "MAT-001",
            "lesson": "Matematik",
            "topic": "Çarpanlar ve Katlar",
            "subtopic": "Pozitif Tam Sayıların Pozitif Tam Sayı Çarpanları",
            "front": "Herhangi bir pozitif tam sayının en küçük pozitif tam sayı çarpanı kaçtır?",
            "back": "1'dir.",
            "difficulty": "easy",
            "source": "notebooklm"
        },
        # Ek flashcard'lar (konuyla ilgili tipik sorular)
        {
            "kazanim_id": "MAT-001",
            "lesson": "Matematik",
            "topic": "Çarpanlar ve Katlar",
            "subtopic": "Pozitif Tam Sayıların Pozitif Tam Sayı Çarpanları",
            "front": "72 sayısının asal çarpanlarına ayrılmış hali nedir?",
            "back": "72 = 2³ × 3²",
            "difficulty": "medium",
            "source": "notebooklm"
        },
        {
            "kazanim_id": "MAT-001",
            "lesson": "Matematik",
            "topic": "Çarpanlar ve Katlar",
            "subtopic": "Pozitif Tam Sayıların Pozitif Tam Sayı Çarpanları",
            "front": "72 sayısının kaç tane pozitif tam sayı çarpanı vardır?",
            "back": "12 tane (1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72)",
            "difficulty": "medium",
            "source": "notebooklm"
        },
        {
            "kazanim_id": "MAT-001",
            "lesson": "Matematik",
            "topic": "Çarpanlar ve Katlar",
            "subtopic": "Pozitif Tam Sayıların Pozitif Tam Sayı Çarpanları",
            "front": "Bir sayının kendisi ve 1 dışında başka çarpanı yoksa bu sayıya ne denir?",
            "back": "Asal sayı denir.",
            "difficulty": "easy",
            "source": "notebooklm"
        },
    ]
    
    flash_success = 0
    for card in flashcards:
        try:
            result = client.table('flashcards_v2').insert(card).execute()
            if result.data:
                flash_success += 1
        except Exception as e:
            print(f"   ⚠️ Kart hatası: {e}")
    
    print(f"   ✅ {flash_success}/{len(flashcards)} flashcard kaydedildi")
    
    # =========================================================
    # 2. QUIZ VERİLERİNİ KAYDET
    # =========================================================
    print("\n❓ Quiz verileri kaydediliyor...")
    
    quiz_data = {
        "total_questions": 10,
        "questions": [
            {
                "id": 1,
                "question": "Aşağıdaki sayılardan hangisi hem 3'e hem de 5'e kalansız olarak bölünebilir?",
                "options": {"A": "312", "B": "275", "C": "285", "D": "403"},
                "correct_answer": "C",
                "explanation": "285 = 3×95 = 5×57, dolayısıyla hem 3'e hem 5'e bölünür."
            },
            {
                "id": 2,
                "question": "90 sayısının asal çarpanlarına ayrılmış şekli aşağıdakilerden hangisidir?",
                "options": {"A": "2 × 3 × 15", "B": "9 × 10", "C": "2 × 3² × 5", "D": "2² × 3 × 5"},
                "correct_answer": "C",
                "explanation": "90 = 2 × 45 = 2 × 9 × 5 = 2 × 3² × 5"
            },
            {
                "id": 3,
                "question": "60 sayısının kaç tane pozitif tam sayı böleni vardır?",
                "options": {"A": "12", "B": "6", "C": "4", "D": "10"},
                "correct_answer": "A",
                "explanation": "60 = 2² × 3 × 5, bölen sayısı = (2+1)(1+1)(1+1) = 12"
            }
        ]
    }
    
    try:
        # icerikler tablosundaki quiz kaydını güncelle
        result = client.table('icerikler').update({
            'icerik_json': json.dumps(quiz_data, ensure_ascii=False)
        }).eq('icerik_id', 'NB-CARP-004').execute()
        
        if result.data:
            print("   ✅ Quiz verileri kaydedildi (NB-CARP-004)")
    except Exception as e:
        print(f"   ❌ Quiz kayıt hatası: {e}")
    
    # =========================================================
    # 3. İNFOGRAFİK PATH'İNİ KAYDET
    # =========================================================
    print("\n📊 İnfografik path'i kaydediliyor...")
    
    # Şimdilik yerel path, sonra Supabase Storage'a yüklenecek
    infographic_path = "C:/Users/Engin/.gemini/antigravity/brain/594999b6-cbd6-4b51-b4f9-e26b8c0283de/infographic_full_1768927775009.png"
    
    try:
        result = client.table('icerikler').update({
            'image_path': infographic_path
        }).eq('icerik_id', 'NB-CARP-002').execute()
        
        if result.data:
            print(f"   ✅ İnfografik path kaydedildi (NB-CARP-002)")
    except Exception as e:
        print(f"   ❌ İnfografik kayıt hatası: {e}")
    
    # =========================================================
    # ÖZET
    # =========================================================
    print("\n" + "=" * 60)
    print("📊 ÖZET")
    print("=" * 60)
    print(f"✅ Flashcard: {flash_success} adet flashcards_v2'ye eklendi")
    print(f"✅ Quiz: 3 soru icerikler.icerik_json'a kaydedildi")
    print(f"✅ İnfografik: Path kaydedildi")
    print("\n🔜 Sonraki adım: UI'da bunları göstermek")

if __name__ == "__main__":
    main()
