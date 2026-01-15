# LGS Neural-Koç – Ek Fikirler ve Geliştirme Notları  
## (Beyin Fırtınası Özeti + IDE İçin Uygulama Komutları)

Bu doküman, ana yol haritasına **ek olarak** tasarlanmış yeni fikirleri içerir.  
Amaç:
- Projeyi daha işlevsel,
- Pilot öğrencinin profilini daha iyi gözeten,
- Uzun vadede ürünleşmeye daha hazır

hale getirecek geliştirme alanlarını tanımlamaktır.

Her fikir için:
- Kısa açıklama,
- Öğrenciye etkisi,
- Teknik uygulama notları,
- AI IDE (Cursor / Windsurf vb.) için örnek komut bloğu

verilmiştir. Bu dosya, ana `yol_haritasi.md` ile birlikte kullanılmalıdır.


---

## 1. Öğrenci Deneyimini Güçlendiren Fikirler

### 1.1. Gün Sonu “Küçük Zafer” Özeti

**Amaç:**  
Pilot öğrencinin “bugün bir şey başardım” hissini almasını sağlamak.  
Sadece netleri değil, **gelişimi ve çabasını** görünür kılmak.

**Öğrenciye Etkisi:**
- Gün sonunda pozitif kapanış.
- “Her gün minik zafer” algısı ile devam motivasyonu.

**Teknik Uygulama Notları:**
- Yeni fonksiyon: `analysis_engine.compute_daily_summary(student_id, date)`
  - O gün çözülen soru sayısı,
  - Doğru/yanlış oranı,
  - Düne göre fark (ör: matematik doğruluğu %40 → %50).  
- Streamlit:
  - “Bugün” ekranının altına `st.container` içinde “Bugün Özeti” kutusu.

**AI IDE Komut Örneği:**

```text
Görev: Gün sonu özet kutusunu ekle.

Dosyalar:
- app/analysis_engine.py
- streamlit_app.py

Adımlar:
1. analysis_engine.py içine compute_daily_summary(student_id: str, date: datetime.date) fonksiyonunu yaz.
   - Answers ve Questions DataFrame'lerini kullan.
   - Sadece verilen tarihte oluşturulan kayıtları dikkate al.
   - Çıktı: {
       "total_solved": int,
       "correct_count": int,
       "accuracy": float,   # 0-1
       "delta_vs_yesterday": {
         "accuracy": float  # pozitif veya negatif
       }
     }

2. streamlit_app.py'de "Bugün" sayfasında, sayfanın altına bir container ekle:
   - Başlık: "Bugünlük Küçük Zaferin"
   - İçerik: compute_daily_summary çıktısını kullanarak doğal dille bir özet yaz.
   - Örnek metin: "Bugün 24 soru çözdün, doğruluk oranını dünden %10 artırdın."

3. UI sade ve okunabilir olsun, sayıların yanında ufak emoji kullanabilirsin (örn: ✅, 📈).
```


---

## 2. Akademik Mantığı Derinleştiren Fikirler

### 2.1. Kavram Ustalığı Skoru (Micro-Skill Heatmap)

**Amaç:**  
Her konu/alt konu (topic/subtopic) için 0–100 arası **ustalık skoru** çıkararak:

- Çocuğa “sen burada iyisin / burası zayıf” diyebilmek,
- AI planlayıcıya hangi konularda soru ağırlığı verileceğini göstermek.

**Öğrenciye Etkisi:**
- Hedef netleşir: “Karekök ustalık skorum %48, bunu %60’a çıkaralım.”
- Kendi haritasını görür, kontrol hissi artar.

**Teknik Uygulama Notları:**
- Yeni fonksiyon: `analysis_engine.compute_mastery_scores(student_id)`
  - Her `(lesson, topic, subtopic)` için:
    - toplam soru sayısı,
    - doğru/yanlış sayısı,
    - mastery_score = doğru_oranı * 100 (veya daha sofistike formül).
- UI:
  - Analiz ekranında küçük bir heatmap / tablo:
    - Renk kodu: kırmızı (<40), sarı (40–70), yeşil (70+).

**AI IDE Komut Örneği:**

```text
Görev: Kavram ustalığı skorlarını hesapla ve göster.

Dosyalar:
- app/analysis_engine.py
- streamlit_app.py

Adımlar:
1. analysis_engine.py'ye compute_mastery_scores(student_id: str) fonksiyonunu ekle.
   - Answers ve Questions DataFrame'lerini kullan.
   - Gruplama: lesson, topic, subtopic bazında.
   - Çıktı DataFrame kolonları:
     - lesson
     - topic
     - subtopic
     - total_questions
     - correct_count
     - accuracy (0-1)
     - mastery_score (0-100)
     - mastery_level ("dusuk", "orta", "yuksek")

2. streamlit_app.py'de Analiz sekmesine bir bölüm ekle:
   - Başlık: "Kavram Ustalığı Haritan"
   - compute_mastery_scores çıktısını tablo olarak göster.
   - mastery_level'e göre satırları renkli badge/border ile işaretle.

3. İleride bu fonksiyonu exam_engine.build_student_skill_summary içinde de kullanmak için modüler yaz.
```


---

## 3. Psikoloji & Davranış Katmanı

### 3.1. “Moral Booster” Set – Kötü Deneme Sonrası Hafif Set

**Amaç:**  
Ani kötü performans sonrası öğrencinin moralini toparlamak için, güçlü olduğu konulardan **kolay sorular** içeren kısa bir paket vermek.

**Öğrenciye Etkisi:**
- “Ben yapamıyorum” düşüncesi kırılır.
- Hızlı bir başarı hissi ile sistemden kopmaz.

**Teknik Uygulama Notları:**
- `analysis_engine.detect_negative_trend(student_id)`
  - Son 2–3 deneme puanlarında ciddi düşüş varsa True döndür.
- `exam_engine.create_moral_booster_exam(student_id)`
  - Öğrencinin iyi olduğu konulardan kolay sorular seç (mastery_score yüksek, difficulty_label 1–2).
- UI:
  - Analiz ekranında uyarı banner’ı:
    - “Son iki denemede netlerin düştü. 10 soruluk moral seti çözmek ister misin?”

**AI IDE Komut Örneği:**

```text
Görev: Moral booster seti ekle.

Dosyalar:
- app/analysis_engine.py
- app/exam_engine.py
- streamlit_app.py

Adımlar:
1. analysis_engine.detect_negative_trend(student_id: str) fonksiyonunu yaz.
   - Son 3 exam için toplam neti hesapla.
   - Basit bir eşik kullan: son exam, öncekinin %20 altındaysa True.

2. exam_engine.create_moral_booster_exam(student_id: str) fonksiyonunu yaz.
   - compute_mastery_scores yardımıyla mastery_score'u yüksek konuları bul.
   - Questions'tan bu konulardan difficulty_label 1 veya 2 olan 10 soru seç.
   - Yeni exam kaydı oluştur.

3. Analiz ekranında:
   - Eğer detect_negative_trend True ise sarı bir uyarı göster.
   - Mesaj içinde "Moral Denemesi Oluştur" butonu olsun.
   - Buton create_moral_booster_exam'i çağırıp soru çözme ekranına yönlendirsin.
```


---

## 4. Yapısal İyileştirmeler

### 4.1. LLM Abstraction Layer (Model Bağımsız Katman)

**Amaç:**  
Gemini 2.5’e bağımlılığı azaltmak, gelecekte farklı bir modele geçmeyi kolaylaştırmak.

**Teknik Uygulama Notları:**
- `llm_adapter` içinde tüm LLM çağrıları için ortak fonksiyonlar:
  - `llm_generate_json(task: str, payload: dict) -> dict`
  - `llm_chat(task: str, payload: dict) -> str`
- Bu fonksiyonlar içinde `provider = "gemini"` kullanılır, ancak dışarıdan model ismi kullanılmaz.
- Prompt şablonlarını `llm_prompts.md` altında metin olarak saklayıp, koda string olarak çekebilirsin.

**AI IDE Komut Örneği:**

```text
Görev: LLM adapter katmanını model bağımsız hale getir.

Dosyalar:
- app/llm_adapter.py

Adımlar:
1. llm_adapter.py'de public API olacak iki fonksiyon tasarla:
   - llm_generate_json(task: str, payload: dict, api_key: str) -> dict
   - llm_chat(task: str, payload: dict, api_key: str) -> str

2. task parametresi "adaptif_plan", "teaching", "variant_generation" gibi metinler olacak.
   Her task için:
   - Uygun system_prompt ve user_prompt'u bir sözlükten çek.
   - Gemini 2.5 API'sine çağrı yap.

3. Eski fonksiyonları (generate_json_with_gemini vb.) bu yeni abstraksiyona yönlendir.
4. Koda yorum ekle: Gelecekte provider değişirse sadece llm_adapter.py değişecek.
```


### 4.2. Feature Flags – Deneysel Özellikleri Aç/Kapa

**Amaç:**  
Yeni fikirleri pilot öğrencide denerken, gerekirse tek satırdan açıp kapatabilmek.

**Teknik Uygulama Notları:**
- `config/feature_flags.yaml` benzeri bir dosya:
  - `warmup_mode: true`
  - `moral_booster: true`
  - `mastery_scores: true`
- `settings` yüklenirken bu YAML parse edilir, global bir config objesine aktarılır.
- Streamlit ve backend fonksiyonlar feature flag’lere bakarak ilgili özelliği aktifleştirir.

**AI IDE Komut Örneği:**

```text
Görev: Feature flags sistemi ekle.

Dosyalar:
- config/feature_flags_example.yaml
- app/data_access.py veya ayrı config_loader.py
- streamlit_app.py

Adımlar:
1. config/feature_flags_example.yaml dosyasını oluştur, içinde örnek flag'ler olsun:
   - warmup_mode: true
   - moral_booster: true
   - mastery_scores: true

2. Config yükleme sırasında bu YAML dosyasını okuyup bir dict'e aktar.

3. streamlit_app.py içinde şu kontrolleri yap:
   - Eğer warmup_mode false ise ısınma modu UI'sini gösterme.
   - Eğer moral_booster false ise ilgili banner'i gösterme.
   - Eğer mastery_scores false ise "Kavram Ustalığı Haritan" bölümünü gösterme.

4. Kodda feature flag'leri merkezi bir config objesi üzerinden kullan (örn: st.session_state["features"]). 
```


---

## Son Not

Bu dokümandaki fikirler:

- Ana yol haritasını “şişirmek” için değil,  
- İhtiyaç oldukça **seçip devreye alabileceğin** ileri seviye modüller olarak düşünülmelidir.

Pratik kullanım önerisi:
1. Önce ana `yol_haritasi.md` içindeki Faz 0–3’ü tamamla.
2. Ardından bu dosyadan **en fazla 2–3 fikri** seç ve ilgili AI IDE komut bloklarını kullanarak kod tabanına entegre et.
3. Pilot öğrenciden gelen gerçek tepkilere göre hangi fikirlerin gerçekten işe yaradığını gözlemle ve sadece onları ileri taşı.

Bu dosya, LGS Neural-Koç’un **ikinci vitese geçtiği** yer olarak görülebilir.
