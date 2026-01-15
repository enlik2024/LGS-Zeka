import pandas as pd
import os

# LGS Örnek Soru Verisi (Seed Data)
data = {
    "question_id": [
        "mat_uslu_001", "mat_uslu_002", "mat_karekok_001", 
        "fen_mevsim_001", "fen_dna_001", 
        "turkce_sozcuk_001", "turkce_paragraf_001"
    ],
    "lesson": [
        "Matematik", "Matematik", "Matematik", 
        "Fen Bilimleri", "Fen Bilimleri", 
        "Türkçe", "Türkçe"
    ],
    "topic": [
        "Üslü İfadeler", "Üslü İfadeler", "Kareköklü İfadeler", 
        "Mevsimler ve İklim", "DNA ve Genetik Kod", 
        "Sözcükte Anlam", "Paragrafta Anlam"
    ],
    "subtopic": [
        "Üslü Sayıların Özellikleri", "Çözümleme", "Tam Kare Sayılar", 
        "Mevsimlerin Oluşumu", "DNA Yapısı", 
        "Gerçek Anlam", "Ana Düşünce"
    ],
    "difficulty": [2, 3, 3, 2, 4, 1, 3], # 1-5
    "text": [
        "2 üzeri 3 kaçtır?", 
        "Bir bakteri her saat 2'ye bölünerek çoğalıyor. 5 saat sonra kaç bakteri olur?",
        "Alanı 144 cm² olan karenin bir kenarı kaç cm'dir?",
        "Dünya'nın eksen eğikliği kaç derecedir?",
        "DNA'nın yapı birimi nedir?",
        "'Ağır' sözcüğü hangisinde mecaz anlamda kullanılmıştır?",
        "Paragrafın ana düşüncesi nedir?"
    ],
    "option_a": ["6", "16", "10", "23° 27'", "Gen", "Çanta çok ağırdı.", "Okumak güzeldir."],
    "option_b": ["8", "32", "12", "27° 23'", "Nükleotid", "Ağır sözler söyledi.", "Kitap okumalıyız."],
    "option_c": ["9", "64", "14", "90°", "Kromozom", "Ağır adımlarla yürüdü.", "Bilgi güçtür."],
    "option_d": ["12", "128", "16", "0°", "Hücre", "Ağır yemek yedi.", "Okumak zihni açar."],
    "correct_answer": ["B", "B", "B", "A", "B", "B", "D"],
    "image_url": ["", "", "", "", "", "", ""]
}

df = pd.DataFrame(data)

# Dosyayı kaydet
file_path = "questions.csv"
df.to_csv(file_path, index=False)

print(f"Seed data created: {file_path}")
