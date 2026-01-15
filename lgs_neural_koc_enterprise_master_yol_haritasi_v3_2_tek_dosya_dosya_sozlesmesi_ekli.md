# LGS Neural-Koç – TEK DOSYA Enterprise Master Sözleşme (v3.1)
## “AI IDE atlamasın” + “tüm detaylar tek yerde” birleşik sürüm

Bu sürüm, senin eleştirin doğrultusunda iki ihtiyacı **tek dosyada** birleştirir:

1) **Enterprise-level, atlamasız faz sözleşmeleri**  
2) **Önceki detaylı yol haritası + ek fikirler metninin tamamı**

Yani artık:
- IDE’ye sadece özet verip detay kaybettirmiyoruz,
- ama aynı zamanda fazlar için “yorum şansı bırakmayan” kontrat katmanını da üstte tutuyoruz.

---

## NASIL KULLANILIR (Zorunlu Protokol)

### 1) Master Context sırası
AI IDE’ye görev verirken şu hiyerarşiyi bağlayıcı kabul et:

1. **Bölüm I – Faz Sözleşmeleri (v3.1)**  
2. **Dosya & Klasör Sözleşmesi**  
3. **Bölüm II-III – Tam metin ekler**

### 2) Faz-kapısı
Bir fazın DoD’i sağlanmadan bir sonraki faza geçilmez.

### 3) Tek doğru komut bloğu kuralı
Her faz için, ilgili bölümde yer alan “AI IDE Komut Paketi” dışına çıkılmaz.

---

## DOSYA & KLASÖR SÖZLEŞMESİ (DEĞİŞTİRİLEMEZ)

Bu proje, faz-kapılı ve uzun vadede Sheets → Supabase geçişine açık bir mimariyle tasarlanmıştır.  
AI IDE’nin “iyi niyetli refactor” refleksleri (dosya taşıma, ad değiştirme, aşırı katmanlaştırma) bu tür projelerde:

- faz sırasını bozabilir,
- tek kapı prensibini kırabilir,
- veri erişimini dağınık hale getirerek migrasyonu pahalılaştırabilir,
- pilot aşamada gereksiz karmaşıklık üretebilir.

Bu nedenle aşağıdaki liste ve kurallar **bağlayıcıdır.**

### 1) Kanonik dosya listesi (tek doğru isim/konum)

Aşağıdaki dosyalar bu projede **sabit** kabul edilir:

**Kök**
- `streamlit_app.py`

**Uygulama katmanı**
- `app/data_access.py`
- `app/llm_adapter.py`
- `app/analysis_engine.py`
- `app/exam_engine.py`
- `app/schedule_engine.py`
- `app/ui_components.py` *(varsa)*

**Eğitim katmanı (FAZ D sonrası)**
- `app/content_engine.py`
- `app/curriculum_engine.py`
- `app/teaching_engine.py`
- `app/content_ingest_engine.py` *(yalnız FAZ D-2’de aktifleşir)*

**Konfigürasyon**
- `config/settings.yaml`
- `config/feature_flags.yaml`

**Test**
- `tests/`

### 2) Dosya kilit kuralları (AI IDE için)**

1) Yukarıdaki kanonik dosyaların **adı değiştirilemez**.  
2) Bu dosyalar **başka klasöre taşınamaz**.  
3) Bu dosyalar **bölünemez veya birleştirilemez**.  
4) Yeni dosya eklemek gerekiyorsa sadece şu dizinlere eklenebilir:  
   - `app/`  
   - `tests/`  
   - `config/`  
5) Yeni eklenen her dosya için:
   - hangi faza ait olduğu dosya başı docstring’de yazılacak.  
6) **Tek kapı ilkesi** bu liste ile birlikte yorumlanır:  
   - LLM çağrıları *daima* `llm_adapter` üzerinden  
   - Veri erişimi *daima* `data_access` üzerinden

### 3) Faz-bazlı dosya kullanım sınırı

AI IDE, aşağıdaki fazlarda yalnız ilgili modülleri genişletebilir:

- **FAZ A:**  
  `data_access`, `analysis_engine`, `exam_engine`, `llm_adapter`, `streamlit_app`  
- **FAZ B:**  
  + `schedule_engine`, `ui_components`  
- **FAZ C:**  
  Faz A-B modülleri içinde adaptif eklemeler  
- **FAZ D:**  
  + `content_engine`, `curriculum_engine`, `teaching_engine`  
- **FAZ D-2:**  
  + `content_ingest_engine`  
- **FAZ E+:**  
  observability/promptops dosyaları eklenebilir

### 4) Yasağa rağmen gerekirse

Eğer mimari gereği mutlaka yeni bir temel dosya gerekiyorsa:  
- Yeni dosya adı **master dokümana “Migration Notu” altında eklenmeden** kullanılmaz.  
Bu madde, kontrolün sende kalması için özellikle konmuştur.

---

# BÖLÜM I — Atlamasız Faz Sözleşmeleri (v3.1)

Aşağıdaki faz sözleşmeleri, önceki v3 metninin üstüne,
**FAZ C’nin genişletilmiş sürümünü** entegre edecek şekilde güncellenmiştir.
Bu bölüm, IDE’nin “kısaltma/yorumlama” davranışını engellemek için normatif metindir.

# LGS Neural-Koç – Enterprise “Atlamasız” Master Yol Haritası (v3)
## AI IDE’ye Yorum Şansı Bırakmayan Faz Sözleşmeleri
### Pilot (1 öğrenci) → Çoklu Öğrenci → Ürünleşme → Ölçeklenebilir Platform

Bu doküman, önceki tüm yol haritalarının niyetini koruyarak **fazları “sözleşme formatında” yeniden yazar.**  
Hedef: Cursor/Windsurf vb. IDE’lerde bu metin **tek başına Master Context** olarak verildiğinde bile,  
AI’nin “yorumlayıp sadeleştirmesi” veya kritik işleri atlaması engellensin.

Bu yüzden her faz için:
- **Girdi ön koşulu (Pre-DoD)**
- **SERT KURALLAR**
- **Dosya/Modül sınırı**
- **Fonksiyon listesi**
- **UI görev listesi**
- **Test zorunlulukları**
- **Definition of Done (DoD)**
- **Tek doğru AI IDE komut bloğu**

zorunlu şekilde tanımlanmıştır.

> Not:  
> Bu v3 sürümü “faz sözleşmeleri”ni **normatif ana metin** olarak sunar.  
> Önceki uzun dokümanlar artık “ek doküman” niteliğindedir.  
> IDE’ye iş verirken esas referans **bu dosya** olmalıdır.

---

## 0) GLOBAL MASTER KURALLAR (Tüm Fazlarda Bağlayıcı)

### 0.1 Tek Kapı İlkesi
1) **LLM çağrıları tek kapı:** `app/llm_adapter.py`  
2) **Veri erişimi tek kapı:** `app/data_access.py`  
3) **Plan/mode/feature config tek kapı:** `config/` altı YAML dosyaları

### 0.2 Etiket ve Veri Disiplini
- **Questions** için zorunlu:  
  - `lesson, topic, subtopic, difficulty_label, question_origin, correct_option, options_json, active`
- **Content** için zorunlu:  
  - `lesson, topic, subtopic, content_type, source_type, summary_bullets, strategy_steps, common_mistakes, mini_check_* , active`
- **Etiketsiz kayıt = pasif kayıt.**

### 0.3 UI “3 Kart Kuralı”
Pilot öğrenci ekranlarında aynı anda **en fazla 3 ana odak** gösterilir.  
Karmaşık dashboard yok; minimal sürtünme öncelik.

### 0.4 Feature Flags Zorunluluğu
Deneysel her özellik `feature_flags.yaml` ile kontrol edilir.  
Varsayılan kapalı, pilot geri bildirimine göre açılır.

### 0.5 Test Asgari Standardı
Her faz sonunda:
- En az **3 yeni pytest senaryosu**  
- Kritik akışlar için **happy path + 1 edge case + 1 failover**

### 0.6 Faz-Kapısı
Bir fazın DoD’i sağlanmadan **bir sonraki faza geçilemez**.  
IDE AI bu kuralı “uygulama içi checklist” olarak kod yorumlarında da belirtmelidir.

---

## 1) Faz Haritası (Yeni Plan Eşleştirmesi)

- **FAZ A:** MVP Stabilizasyonu ve Temel Veri Omurgası [TAMAMLANDI]
- **FAZ B:** Günlük Rutin + Motivasyon Çekirdeği [TAMAMLANDI]
- **FAZ C:** Gerçek Adaptif Soru Motoru (CAT-Lite) [TAMAMLANDI]
- **FAZ D:** Eğitim Katmanı (Content/Curriculum) + Manuel → Yarı Otomatik PDF [TAMAMLANDI]
- **FAZ E:** Ürün Kalitesi, Observability, PromptOps, Feature Ops [TAMAMLANDI]
- **FAZ F:** Sheets → Supabase + Çoklu Öğrenci [PİLOT İÇİN ERTELENDİ]
- **FAZ G:** Enterprise Analitik + Ebeveyn/Koç Kokpiti [TAMAMLANDI]  

---

# FAZ A — MVP Stabilizasyonu ve Temel Veri Omurgası [TAMAMLANDI]

## Amaç
Mevcut Python + Sheets + Streamlit + Gemini 2.5 MVP’nin  
**kırılmadan çalışan, modüler, testlenebilir** çekirdeğini oluşturmak.

## Neden
Faz B-C-D’deki tüm kişiselleştirme ve adaptiflik,  
A fazındaki **doğru veri kaydı + doğru analiz** üzerine inşa edilir.

## Bağımlılık
Yok.

## Pre-DoD (Girdi Ön Koşulları)
- Mevcut repo çalışır halde olmalı.
- Google Sheets erişim anahtarları ve temel tablar oluşturulmuş olmalı:
  - `Students, Questions, Exams, ExamQuestions, Answers, Schedule`

## SERT KURALLAR
1) **Sheets erişimi yalnız data_access.**  
2) **LLM yalnız llm_adapter.**  
3) `ExamQuestions` ilişkisel sheet’i **bu fazda zorunlu** eklenir.  
4) Analiz metrikleri “silently fail” yapmaz; eksik veri için kullanıcıya anlaşılır uyarı döner.

## Dosya/Modül Sınırı
- `app/data_access.py`
- `app/analysis_engine.py`
- `app/exam_engine.py`
- `app/llm_adapter.py`
- `app/schedule_engine.py` (iskele)
- `streamlit_app.py`
- `config/settings.yaml`
- `config/feature_flags.yaml` (iskele)
- `tests/`

## Fonksiyon Paketi
### A1) Data Access
- `load_students()` / `save_students()`  
- `load_questions()` / `save_questions()`  
- `load_exams()` / `save_exams()`  
- `load_exam_questions()` / `save_exam_questions()`  
- `load_answers()` / `append_answer()`  
- `load_schedule()` / `save_schedule()`

### A2) Exam Engine (Fixed)
- `create_fixed_exam(student_id, blueprint)`  
- `get_exam_questions(exam_id)`  
- `finalize_exam(exam_id)`

### A3) Analysis Engine (Basic)
- `compute_basic_accuracy(student_id, lesson=None)`  
- `compute_recent_activity(student_id, days=7)`

### A4) LLM Adapter (v1)
- `llm_generate_json(task, payload, api_key)`  
- `llm_chat(task, payload, api_key)`  
- Basit retry + JSON parse koruması

## UI Paketi
- “Sabit Mini Deneme Oluştur”  
- “Deneme Çöz”  
- “Basit Analiz” (son 7 gün, ders bazlı doğruluk)

## Test Paketi (Min)
1) Sabit deneme oluşturma → `Exams` ve `ExamQuestions` yazıldı mı?  
2) Cevap girme → `Answers` append çalışıyor mu?  
3) Analiz fonksiyonu boş veriyle düzgün uyarı veriyor mu?

## DoD
- 10 soruluk fixed exam uçtan uca çalışır:
  - yarat → sırayla göster → cevap kaydet → bitir  
- `ExamQuestions` sheet’i aktif kullanılıyor.  
- LLM adapter tek kapı çalışıyor.  
- En az 3 pytest yeşil.

## AI IDE Komut Paketi (Tek Doğru Blok)
```text
MASTER SÖZLEŞME — FAZ A

Amaç: MVP stabilizasyonu ve veri omurgası.

SERT KURALLAR:
1) Sheets erişimi sadece app/data_access.py üzerinden.
2) LLM çağrıları sadece app/llm_adapter.py üzerinden.
3) ExamQuestions sheet’i eklenecek ve zorunlu kullanılacak.
4) Her fonksiyon type hints + docstring ile yazılacak.
5) 3 pytest senaryosu yazılacak.

Dosyalar:
- app/data_access.py
- app/analysis_engine.py
- app/exam_engine.py
- app/llm_adapter.py
- streamlit_app.py
- config/settings.yaml
- tests/test_phase_a.py

Görev:
A1) ExamQuestions okuma/yazma katmanını ekle.
A2) create_fixed_exam + çözme akışını uçtan uca çalışır hale getir.
A3) Basit analiz fonksiyonlarını ekle.
A4) LLM adapter v1'i standartlaştır.
A5) 3 test yaz.

Kabul Kriterleri:
- 10 soruluk fixed exam 1 dakikadan kısa sürede oluşturuluyor.
- Answers kayıtları doğru düşüyor.
- Testler yeşil.
```

---

# FAZ B — Günlük Rutin + Motivasyon Çekirdeği [TAMAMLANDI]

## Amaç
Pilot öğrenciyi sistemde tutacak **günlük çalışma işletim sistemi** oluşturmak.

## Neden
Zor profil öğrencide gerçek başarı, önce **sürdürülebilir kullanım** ile gelir.

## Bağımlılık
FAZ A

## Pre-DoD
- `Schedule` sheet’i aktif ve örnek haftalık template içeriyor.
- Faz A fixed exam akışı çalışıyor.

## SERT KURALLAR
1) Öğrenci ekranı **3 kart kuralına** uyacak.  
2) Günde en fazla **2–3 ana blok** vurgulanacak.  
3) “Başlama sürtünmesi”ni artıran hiçbir UI eklentisi yapılmayacak.  
4) Tüm motivasyon özellikleri feature flag altında.

## Dosya/Modül Sınırı
- `app/schedule_engine.py`
- `app/analysis_engine.py`
- `app/ui_components.py`
- `streamlit_app.py`
- `config/feature_flags.yaml`

## Fonksiyon Paketi
- `get_today_blocks(student_id)`  
- `find_active_block(blocks, now)`  
- `find_next_block(blocks, now)`  
- `mark_block_completed(schedule_id)`  
- `compute_today_completion_percent(student_id)`  
- `compute_daily_summary(student_id, date)`

## UI Paketi
- “Bugün” sekmesi:
  - aktif blok kartı  
  - sıradaki blok kartı  
  - gün tamamlama yüzdesi  
  - “Bugünlük Küçük Zafer”

## Test Paketi (Min)
1) Bugünün blokları doğru listeleniyor mu?  
2) Blok tamamlandı işaretleme doğru mu?  
3) Günlük özet doğru hesaplanıyor mu?

## DoD
- “Bugün” sekmesi veri yoksa fallback gösteriyor.  
- 1 tıkla blok tamamlanabiliyor.  
- Günlük özet otomatik üretiliyor.  
- 3 pytest yeşil.

## AI IDE Komut Paketi
```text
MASTER SÖZLEŞME — FAZ B

SERT KURALLAR:
1) UI 3 kart kuralı.
2) Tüm motivasyon öğeleri feature flag ile kontrol edilecek.
3) Günlük özet compute_daily_summary zorunlu.

Dosyalar:
- app/schedule_engine.py
- app/analysis_engine.py
- app/ui_components.py
- streamlit_app.py
- config/feature_flags.yaml
- tests/test_phase_b.py

Görev:
B1) schedule_engine fonksiyonlarını ekle.
B2) "Bugün" sekmesini oluştur.
B3) Günlük küçük zafer özetini entegre et.
B4) 3 test yaz.

Kabul Kriterleri:
- Bugün ekranı 10 sn altında yükleniyor.
- Blok tamamlama ve progress düzgün çalışıyor.
```

---

## FAZ C — Adaptif Soru Motoru (CAT-Lite) [TAMAMLANDI]
**Amaç:**  
Mikro-skill bazlı, zorluk dengeli **gerçek adaptif mini deneme** üretimini çalışır hale getirmek.  
Bu faz, eski yol haritasındaki “Faz 4 Fix (Gerçek Adaptif Mantık)” adımının **yeni master plandaki resmi karşılığıdır**.

**Bağımlılık:** Faz A-B

**Bu faz bitmeden başlanmayacak bir sonraki faz:**  
- **FAZ D — Eğitim Katmanı (Content/Curriculum + PDF)**

### Neden bu faz kritik?
Eğitim katmanı kişiselleştirme kalitesini şu iki şeye yaslar:
1) Öğrencinin doğru/yanlış desenleri  
2) Mikro-skill (topic/subtopic) bazlı ustalık trendleri  

Bu iki veri güvenilir değilse “Öğren” önerileri rastgeleleşir.  
Bu yüzden **adaptif tanı motoru** önce oturtulur.

---

### Teslimatlar
- **Mastery skorları (topic/subtopic/difficulty bazlı)**
- **LLM planlayıcı + kural tabanlı final seçim**
- **Adaptif plan JSON şeması + doğrulama katmanı**
- **Moral booster akışı**
- **Yetersiz soru fallback (graceful degrade)**
- **Unit test seti (min 3 senaryo)**

---

### SERT KURALLAR (Bağlayıcı)
1) **LLM sadece PLAN üretir.**  
   - Final soru seçimi **Python kurallarıyla** yapılır.
2) **Zorluk etiketi veri tabanında tek kaynak doğruluktur.**  
   - `difficulty_label` yoksa adaptif seçim DEVREYE ALINMAZ.
3) **Soru kaynağı etiketi zorunlu:**  
   - `question_origin ∈ {publisher, meb, ai_original, ai_variant_of_pool}`
4) **Sheets erişimi tek kapı:** `app/data_access.py`
5) **LLM çağrısı tek kapı:** `app/llm_adapter.py`
6) **Yetersiz soru durumunda sistem çökmez.**  
   - Önce aynı subtopic içinde zorluk kaydır  
   - Yetmezse topic genişlet  
   - Yetmezse ders genel havuzuna kontrollü açıl
7) **Plan çıktısı strict JSON schema ile doğrulanır.**  
   - Parse hatasında otomatik retry (max 1)  
   - Hâlâ hata varsa rule-based fallback planı kullan

---

### Gerekli Veri Hazırlığı (DoD ön koşulu)
**Questions sheet** minimum kolonları:
- question_id
- lesson
- topic
- subtopic
- difficulty_label (1-5)
- question_origin
- options_json
- correct_option
- active

**Answers sheet** minimum kolonları:
- answer_id
- exam_id
- question_id
- student_id
- is_correct
- attempt_type
- created_at

---

### Fonksiyonel İş Paketi
#### C1) Mastery Motoru
- `compute_mastery_scores(student_id)`  
  - Grup: lesson/topic/subtopic/difficulty  
  - Çıktı: accuracy + mastery_score + mastery_level  

- `build_student_skill_summary(student_id)`  
  - LLM’e gidecek **kompakt** öğrenci profili  
  - Zayıf 5 alt konu + güçlü 3 alt konu + son trend

#### C2) LLM Planlayıcı
- `request_adaptive_plan_from_llm(summary)`  
  - Çıktı strict JSON:
```json
{
  "lesson": "Matematik",
  "target_total_questions": 15,
  "mix": [
    {"topic":"...", "subtopic":"...", "difficulty_label":2, "count":4},
    {"topic":"...", "subtopic":"...", "difficulty_label":3, "count":3}
  ],
  "rationale_bullets": ["..."]
}
```

#### C3) Python Final Seçim + Exam Oluşturma
- `create_adaptive_exam(student_id, plan)`  
  - Plan doğrulama  
  - Soru havuzundan filtreleme  
  - Fallback kuralları  
  - `Exams` + `ExamQuestions` + initial metadata kayıt

#### C4) Negatif Trend ve Moral Set
- `detect_negative_trend(student_id)`  
- `create_moral_booster_exam(student_id)`

#### C5) UI
- “Adaptif Deneme Oluştur”  
- Negatif trend banner: “Moral Denemesi Oluştur”

#### C6) Testler
- Minimum 3 pytest senaryosu:
  1) Normal veri → plan + exam başarı
  2) Subtopic’te yetersiz soru → zorluk kaydırma fallback
  3) LLM JSON parse hatası → rule-based fallback

---

### Definition of Done (DoD)
- `compute_mastery_scores` ve `build_student_skill_summary` çalışıyor.
- LLM plan JSON’u **kaydediliyor** ve schema doğrulamasından geçiyor.
- `create_adaptive_exam`:
  - topic/subtopic/difficulty filtrelerine **gerçekten** uyuyor.
  - yetersiz soru durumunda **otomatik dengeliyor**.
- 15 soruluk adaptif deneme **60 saniye altında** oluşturuluyor.
- Negatif trend → moral set banner’ı UI’da çıkıyor.
- 3 pytest senaryosu yeşil.

---

### AI IDE Komut Paketi (Bu faz için tek doğru komut bloğu)
```text
MASTER CONTEXT:
Yeni master plana göre şu an FAZ C kapsamındayız.
Hedef: "Gerçek adaptif sınav planlama"yı Gemini 2.5 ile çalışır hale getirmek.
Eğitim katmanı (Content/Curriculum) FAZ D ve bu iş bitmeden başlanmayacak.

SERT KURALLAR:
1) LLM sadece PLAN üretir. Final soru seçimi Python ile yapılır.
2) LLM çağrıları sadece app/llm_adapter.py üzerinden.
3) Sheets erişimi sadece app/data_access.py üzerinden.
4) Questions içinde difficulty_label ve question_origin yoksa eksik kolonları ekle ve doldur.
5) Yetersiz soru durumunda graceful fallback zorunlu.
6) Plan JSON’u strict schema ile doğrulanacak.
7) Minimum 3 unit test yazılacak.

DOSYALAR:
- app/data_access.py
- app/analysis_engine.py
- app/exam_engine.py
- app/llm_adapter.py
- streamlit_app.py

GÖREVLER:
C1) compute_mastery_scores(student_id) yaz.
C2) build_student_skill_summary(student_id) yaz.
C3) request_adaptive_plan_from_llm(summary) yaz (JSON schema strict).
C4) create_adaptive_exam(student_id, plan) yaz:
    - planı doğrula
    - Python ile soru_id seç
    - Exams + ExamQuestions + Answers akışını hazırla
C5) UI’ye "Adaptif Deneme Oluştur" butonu ekle.
C6) detect_negative_trend + create_moral_booster_exam yaz; banner ekle.
C7) Yetersiz soru fallback senaryoları için 3 unit test yaz.

KABUL KRİTERLERİ:
- 15 soruluk adaptif deneme 60 sn altında oluşuyor.
- Plan JSON kaydediliyor.
- Soru seçimi topic/subtopic/difficulty filtrelerine uyuyor.
- Yetersiz soru durumunda sistem çökmeden planı otomatik dengeliyor.
- Moral set banner’i doğru tetikleniyor.
```
# FAZ D — Eğitim Katmanı (Content/Curriculum) + Manuel → Yarı Otomatik PDF [TAMAMLANDI]

## Amaç
Soru motorunun yanına **eğitim-temelli** ikinci motoru eklemek.  
“Yanlıştan öğrenmeye tek tık” akışını kurmak.

## Bağımlılık
FAZ B-C

## Pre-DoD
- `compute_mastery_scores` stabil çalışıyor.  
- Topic/subtopic etiket disiplini oturdu.  
- Yeni sheets hazır:
  - `Content`
  - `Curriculum_Map`

## SERT KURALLAR
1) Eğitim katmanı **önce manuel içerikle** çalışır.  
   - PDF otomasyonu **Faz D-2 alt adımı** olarak sonradan eklenir.
2) Tam metin depolama yok; **fiş yaklaşımı** zorunlu:
   - `summary_bullets`
   - `strategy_steps`
   - `common_mistakes`
   - `mini_check_*`
3) `Curriculum_Map`’te olmayan tag ile içerik/soru önerisi yapılmaz.  
4) İçerik kaynağı etiketi zorunlu: `source_type`.

## Dosya/Modül Sınırı
- `app/data_access.py`
- `app/curriculum_engine.py`
- `app/content_engine.py`
- `app/teaching_engine.py`
- `app/content_ingest_engine.py` (yalnız D-2)
- `streamlit_app.py`

## Fonksiyon Paketi
### D1) Curriculum
- `load_curriculum_map()`  
- `validate_tags(lesson, topic, subtopic)`  
- `get_default_content_mix(...)`  
- `get_default_question_mix(...)`

### D2) Content Selection
- `load_content_df()`  
- `get_recommended_content(...)`  
- `build_learning_packet(student_id, lesson, topic, subtopic, source_filter)`

### D3) Wrong-to-Learn Hook
- `suggest_content_for_wrong_question(question_id, student_id)`

### D-2 (PDF Yarı Otomatik – Bu alt adım D1-D3 DoD sonrası)
- `extract_pdf_text_by_page(pdf_path)`  
- `select_candidate_pages(text_by_page)`  
- `request_content_fiche_from_llm(page_text)`  
- `merge_fiches_into_micro_lesson(fiches)`  
- `append_content_to_sheet(fiche)`

## UI Paketi
- “Öğren” sekmesi:
  - topic/subtopic seçimi  
  - kaynak filtresi (publisher/ai/hybrid)  
  - micro-lesson kartı  
  - mini-check  
  - “Hemen Uygula (5 soru)”  
- Soru çözme ekranında:
  - yanlış sonrası “İlgili Konuyu Öğren” butonu

## Test Paketi (Min)
1) build_learning_packet JSON-serializable mı?  
2) validate_tags olmayan içerik önerisi engelleniyor mu?  
3) wrong-to-learn hook doğru content öneriyor mu?

## DoD
- 2 subtopic için 10–20 manuel içerik fişi ile Öğren sekmesi çalışıyor.  
- Yanlış sorudan tek tıkla ilgili içerik açılıyor.  
- Mini-check sonuçları kaydediliyor (opsiyonel LearningEvents).  
- 3 pytest yeşil.

## AI IDE Komut Paketi
```text
MASTER SÖZLEŞME — FAZ D

SERT KURALLAR:
1) PDF otomasyonu bu fazın ilk kısmında YOK.
2) Fiş yaklaşımı zorunlu (summary/strategy/mistakes/mini_check).
3) Curriculum_Map tag doğrulaması olmadan öneri yok.
4) source_type zorunlu.
5) 3 pytest yazılacak.

Dosyalar:
- app/data_access.py
- app/curriculum_engine.py
- app/content_engine.py
- app/teaching_engine.py
- streamlit_app.py
- tests/test_phase_d.py

Görev:
D1) Content + Curriculum sheet erişim katmanlarını ekle.
D2) curriculum_engine fonksiyonlarını yaz.
D3) content_engine selection + build_learning_packet.
D4) "Öğren" sekmesi MVP.
D5) Soru çözme ekranına "İlgili Konuyu Öğren" hook'u.
D6) 3 test.

Kabul Kriterleri:
- Manuel içerikle Öğren sekmesi uçtan uca çalışıyor.
- Yanlış sorudan içerik önerisi 1 tık.
```

---

# FAZ E — Ürün Kalitesi, Observability, PromptOps, Feature Ops [TAMAMLANDI]

## Amaç
Pilot projesini “bakımı yapılabilir ürün” seviyesine taşımak.

## Bağımlılık
FAZ A-D

## Pre-DoD
- Faz D manuel Öğren akışı tamamlandı.

## SERT KURALLAR
1) Tüm deneysel özellikler feature flag altında.  
2) Event log olmadan yeni major feature eklenmez.  
3) Prompt şablonları versiyonlanmadan LLM task eklenmez.

## Dosya/Modül Sınırı
- `config/feature_flags.yaml`
- `app/event_logger.py`
- `app/llm_prompts/`
- `app/llm_adapter.py`
- `tests/`

## Teslimatlar
- Feature flags v1
- Event log v1
- Prompt versioning
- Basit hata raporlama
- Test coverage min %30

## DoD
- 10+ event loglanıyor.  
- Prompt versiyon dosyaları var.  
- Feature flags ile warmup/moral/mastery/learn modları aç-kapa.  
- Coverage raporu üretiliyor.

## AI IDE Komut Paketi
```text
MASTER SÖZLEŞME — FAZ E

SERT KURALLAR:
1) Feature flag olmadan yeni özellik ekleme.
2) Event log zorunlu.
3) Promptlar versionlı klasörde tutulacak.

Dosyalar:
- config/feature_flags.yaml
- app/event_logger.py
- app/llm_adapter.py
- app/llm_prompts/
- tests/test_phase_e.py

Görev:
E1) Feature flag loader ekle.
E2) event_logger ile 10 event'i logla.
E3) Prompt şablonlarını dosyala ve versionla.
E4) 3 test.

Kabul Kriterleri:
- Flags ile UI bölümleri aç/kapa.
- Eventler Sheets veya local log'a düşüyor.
```

---

# FAZ F — Sheets → Supabase + Çoklu Öğrenci [PİLOT İÇİN ERTELENDİ]

## Amaç
Veri katmanını enterprise-grade hale getirmek ve çoklu öğrenciye geçmek.

## Bağımlılık
FAZ E

## Pre-DoD
- Tüm sheet kolonları DB-ready isimlerde ve stabil.

## SERT KURALLAR
1) data_access, backend değişimiyle çalışacak şekilde interface korunacak.  
2) Migration script yazılmadan yeni tablo eklenmez.

## Teslimatlar
- Supabase şeması
- Migration script
- Basic auth/role (admin veya sınırlı erişim)
- Çoklu öğrenci seçimi UI

## DoD
- Aynı fonksiyon çağrılarıyla:
  - Sheets backend → Supabase backend swap edilebiliyor.
- 3 öğrenci ile izole test senaryosu geçiyor.

## AI IDE Komut Paketi
```text
MASTER SÖZLEŞME — FAZ F

SERT KURALLAR:
1) data_access interface bozulmayacak.
2) Migration script zorunlu.

Görev:
F1) Supabase tablolarını oluştur.
F2) Sheets export → DB import script yaz.
F3) data_access içinde backend switch mekanizması ekle.
F4) Çoklu öğrenci seçimi UI.
F5) 3 test.

Kabul Kriterleri:
- Backend switch ile aynı UI çalışıyor.
```

---

# FAZ G — Enterprise Analitik + Ebeveyn/Koç Kokpiti [TAMAMLANDI]

## Amaç
Öğrenci + ebeveyn + koç için KPI odaklı görünürlük katmanı.

## Bağımlılık
FAZ F

## Teslimatlar
- Haftalık raporlar
- Mastery heatmap
- Net trendleri
- Öğrenme etkisi raporu (content before/after delta)

## DoD
- Haftalık PDF/HTML rapor üretimi (opsiyonel)  
- Ebeveyn ekranı sade KPI’lar içeriyor.  
- En az 5 metrik otomatik güncelleniyor.

---

## 2) “IDE AI Atlamasın” Uygulama Protokolü

### 2.1 PR Parçalama Kuralı
Her faz en az 2-3 küçük PR’a bölünür:
- Backend
- UI
- Test

### 2.2 Her PR için Zorunlu Checklist
1) Yeni fonksiyon docstring + type hint  
2) En az 1 test  
3) Feature flag gereksinimi kontrolü  
4) UI 3 kart kuralı kontrolü  

---

## 3) Pilot İçin En Güvenli İlerleme Sırası (Kısa Özet)

1) **FAZ A** → veri omurgası  
2) **FAZ B** → öğrenciyi tut  
3) **FAZ C** → gerçek adaptif sınav planlama  
4) **FAZ D (manuel içerik)** → soru + eğitim çift motor  
5) **FAZ D-2 (PDF yarı otomatik)** → verim artışı  
6) **FAZ E** → ürün kalitesi + observability  
7) **FAZ F** → DB + çoklu öğrenci  
8) **FAZ G** → enterprise analitik

---

## 4) Son Not
Bu v3 sözleşme metni, özellikle pilot öğrencinin zor motivasyon profilinde:
- “önce kullanım → sonra zekâ → sonra otomasyon”  
stratejisini dayatır.  
Bu, hem pedagojik hem ürünleşme açısından en düşük riskli hattır.


---

# BÖLÜM II — Orijinal Ana Yol Haritası (TAM METİN)

Bu bölüm, `lgs_neural_koc_yol_haritasi.md` dosyasının **değiştirilmemiş** tam metnidir.
Detaylı feature listeleri, eski faz notları ve örnek akışlar burada referans olarak korunur.

---
# LGS Neural-Koç – Uçtan Uca Yol Haritası  
## Python + Spreadsheets (geçici) + Gemini 2.5 + Streamlit

Bu doküman, LGS Neural-Koç projesi için **çok detaylı ve ince düşünülmüş** bir yol haritasıdır.  
Hedef: AI IDE (Cursor, Windsurf vb.) üzerinde bu dokümanı referans alan bir yapay zekânın, **ek yorum gerektirmeden** proje kodunu parça parça üretebilmesi.

Aşağıdaki içerik:

- Pedagojik ve psikolojik çerçeveyi,
- Teknik mimariyi,
- Faz bazlı geliştirme planını,
- Spreadsheet şemalarını,
- Python/Streamlit modül planını,
- Gemini 2.5 ile kullanılacak örnek prompt şablonlarını,
- Pilot öğrenciye özgü günlük rutin ve bildirim mantığını

adım adım tanımlar.


---

## 0. Kısa Özet – Ne İnşa Ediliyor?

**LGS Neural-Koç**, LGS öğrencileri için:

1. Çözdükleri soruları ve denemeleri kaydeden,
2. Hangi mikro-kazançlarda (micro-skill) zorlandıklarını tespit eden,
3. Bu verilere göre yeni mini denemeler ve görevler (task’lar) oluşturan,
4. Yanlış sorular üzerinden “Bu konuyu öğret” tarzında **AI koçluk** yapan,
5. Günlük rutine uygun, **düşük sürtünmeli ama tutarlı** bir çalışma planı gösteren,
6. Dijital dikkat dağınıklığını azaltmak için **blok çalışmaları**, **analog molalar** ve basit bildirimlerle nudging yapan,

Python + Streamlit + Gemini 2.5 tabanlı bir **kişisel öğrenme platformudur**.  
Başlangıçta **tek bir pilot öğrenci** ile çalışacak, daha sonra çoklu kullanıcıya ölçeklenebilir şekilde tasarlanacaktır.


---

## 1. Projenin Vizyonu ve Kısıtlar

### 1.1. Vizyon

- LGS sürecinde, öğrenciyi 360–420 bandından **450+ bandına** çıkarmayı hedefleyen,
- Sadece net sayısı değil, **neden hata yaptığını** gösteren,
- Matematik ve Türkçe başta olmak üzere sayısal-sözel dengeyi yöneten,
- Öğrencinin **günlük rutinine ve psikolojisine uygun** çalışan,
- Yayınevlerinin sorularını **telif haklarına saygılı** bir şekilde kullanan,
- En başta **spreadsheets + basit Python** ile çalışan, sonra Postgres gibi kalıcı mimariye geçebilen,

bir öğrenme koçu.

### 1.2. Kısıtlar ve Varsayımlar

- Pilot öğrenci zorlu bir karakter:
  - Çabuk motivasyon kaybı,
  - Evde düzensiz çalışma,
  - Dışsal motivasyona bağımlılık,
  - Dijital oyun/video bağımlılığına yatkınlık.
- İlk aşamada veri kalıcı depolama için **spreadsheet (Google Sheets / Excel) kullanılacak**.
- LLM olarak **Gemini 2.5 (multimodal)** kullanılacak.
- UI için **Streamlit** kullanılacak (tek sayfa veya birkaç sekmeli yapı).
- Pilot süreci boyunca:
  - Hukuki risk azaltmak için **yayınevlerinin soruları modelde fine-tune edilmeden**, sadece veritabanı/spreadsheet üzerinden kullanılacak.
  - Router / telefon Focus Mode ayarları, kod dışında ebeveynle birlikte manuel yönetilecek (sistem sadece bunları hatırlatır).


---

## 2. Genel Mimari Tasarım

### 2.1. Katmanlar

1. **Sunum Katmanı (UI) – Streamlit**
   - Öğrenci paneli (Bugün ekranı, timeline, sayaç, görevler)
   - Soru çözüm ekranı
   - Hata analizi ekranı
   - “Bu konuyu öğret” diyalog ekranı (modal/dialog)
   - Ebeveyn / koç paneli (ileride)

2. **Uygulama Mantığı – Python Servis Modülleri**
   - `data_access`: Spreadsheet okuma/yazma fonksiyonları
   - `exam_engine`: Deneme/mini test üretimi
   - `analysis_engine`: Öğrenci performans analizi
   - `teaching_engine`: “Bu konuyu öğret” etkileşim akışları
   - `schedule_engine`: Günlük/haftalık plan mantığı
   - `llm_adapter`: Gemini 2.5 ile konuşan ortak arayüz

3. **Veri Katmanı – Spreadsheet (geçici)**
   - `Students` sheet
   - `Questions` sheet
   - `Exams` sheet
   - `Answers` sheet
   - `Schedule` sheet

4. **LLM Katmanı – Gemini 2.5**
   - Adaptif deneme planlayıcı
   - Zorluk tahmin edici (opsiyonel)
   - Soru çözücü ve açıklayıcı koç
   - Mini ders üretici (“Bu konuyu öğret”)
   - UI metin yardımcısı (motivasyon cümleleri vs.)


### 2.2. Klasör Yapısı (MVP)

AI IDE’ye doğrudan verilecek hedef klasör yapısı:

```text
lgs-neural-koc/
  README.md
  requirements.txt
  streamlit_app.py

  config/
    settings_example.yaml

  data/
    spreadsheets/
      students.xlsx
      questions.xlsx
      exams.xlsx
      answers.xlsx
      schedule.xlsx

  app/
    __init__.py
    llm_adapter.py
    data_access.py
    exam_engine.py
    analysis_engine.py
    teaching_engine.py
    schedule_engine.py
    ui_components.py   # Streamlit yardımcı bileşenleri
```

IDE komutu verirken bu yapıyı sabit kabul edecek şekilde tanımlanmalıdır.


---

## 3. Spreadsheet Şemaları (V1 – Geçici Depolama)

### 3.1. `students.xlsx` – Öğrenci Bilgileri

Sheet adı: `Students`

| Column           | Tip     | Açıklama                                       |
|------------------|---------|-----------------------------------------------|
| student_id       | string  | Benzersiz ID (örn: "pilot_ogrenci_01")        |
| name             | string  | Ad Soyad                                      |
| school           | string  | Okul adı                                      |
| grade            | int     | Sınıf (örn: 8)                                |
| notes            | string  | Serbest not (profil bilgileri)                |
| active           | bool    | Aktif/pilot kullanımda mı                     |


### 3.2. `questions.xlsx` – Soru Havuzu

Sheet adı: `Questions`

| Column           | Tip     | Açıklama                                                            |
|------------------|---------|----------------------------------------------------------------------|
| question_id      | string  | Benzersiz ID                                                        |
| publisher        | string  | Yayın evi                                                           |
| source_book      | string  | Kitap / deneme adı                                                 |
| page_ref         | string  | Sayfa/soru referansı (örn: "s.42 Soru 7")                           |
| lesson           | string  | Türkçe / Matematik / Fen / …                                       |
| topic            | string  | Örn: "Kareköklü sayılar"                                           |
| subtopic         | string  | Örn: "karekökten çıkarma", "modelleme"                             |
| difficulty_label | int     | 1 (çok kolay) – 5 (çok zor)                                       |
| type             | string  | yeni_nesil / klasik / paragraf / grafik / tablo                    |
| stem_text        | string  | Soru kökünün düz metni (varsa)                                     |
| options_json     | string  | JSON string: {"A": "...", "B": "...", ...}                         |
| correct_option   | string  | "A"/"B"/"C"/"D"                                                    |
| media_path       | string  | Görsel yolu veya ileride kullanılacak referans                      |
| active           | bool    | Kullanılabilir mi                                                   |


### 3.3. `exams.xlsx` – Denemeler / Oturumlar

Sheet adı: `Exams`

| Column           | Tip     | Açıklama                                                       |
|------------------|---------|-----------------------------------------------------------------|
| exam_id          | string  | Benzersiz ID                                                   |
| student_id       | string  | `Students.student_id`                                          |
| title            | string  | Örn: "Pilot Mini Deneme 01"                                   |
| mode             | string  | "sabit" / "adaptif" / "konu_tarama"                           |
| created_at       | string  | ISO datetime                                                   |
| status           | string  | "planlandi" / "devam" / "tamamlandi"                          |
| meta_json        | string  | Plan bilgisi (JSON): hedef konular, zorluk dağılımı vs.       |


### 3.4. `answers.xlsx` – Öğrenci Yanıtları

Sheet adı: `Answers`

| Column           | Tip     | Açıklama                                                       |
|------------------|---------|-----------------------------------------------------------------|
| answer_id        | string  | Benzersiz ID                                                   |
| exam_id          | string  | `Exams.exam_id`                                                |
| student_id       | string  | `Students.student_id`                                          |
| question_id      | string  | `Questions.question_id`                                        |
| given_option     | string  | Öğrencinin işaretlediği şık                                   |
| is_correct       | bool    | Doğru mu                                                       |
| time_spent_sec   | int     | Soru üzerinde harcanan süre (varsa)                           |
| attempt_type     | string  | "bos_birakti" / "denedi_bulamadi" / "tahmin" / "normal"       |
| created_at       | string  | ISO datetime                                                   |


### 3.5. `schedule.xlsx` – Günlük / Haftalık Plan

Sheet adı: `Schedule`

| Column           | Tip     | Açıklama                                                                 |
|------------------|---------|---------------------------------------------------------------------------|
| schedule_id      | string  | Benzersiz ID                                                             |
| student_id       | string  | `Students.student_id`                                                    |
| day_of_week      | string  | "Pazartesi", "Salı", ...                                                 |
| block_start      | string  | "14:30" formatında                                                       |
| block_end        | string  | "15:00" formatında                                                       |
| block_type       | string  | "okul" / "etut" / "kurs" / "ev_calismasi" / "mola"                      |
| task_type        | string  | "mat_konusal" / "mat_islem" / "turkce_paragraf" / "fen_tekrar" / ...    |
| target_desc      | string  | Örn: "10 soru kareköklü ifadeler (kolay-orta)"                          |
| is_active        | bool    | Blok şu an geçerli mi                                                    |


Bu şemalar, ileride Postgres’e birebir taşınabilecek şekilde tasarlanmıştır.


---

## 4. Faz Bazlı Geliştirme Planı

Bu bölüm, AI IDE’ye doğrudan verilebilecek **komut-blokları** içerir. Her faz için:

- Hedefler
- Çıktılar
- Dosya / modül görevleri
- AI IDE için örnek prompt


### Faz 0 – Ortam Kurulumu ve Temel İskelet [TAMAMLANDI]

**Hedef:**  
Projeyi çalıştırmak için minimum Python + Streamlit iskeletini kurmak, spreadsheet’lere bağlantıyı hazırlamak.

**Çıktılar:**
- `requirements.txt`
- `streamlit_app.py` içinde basit “Hello” arayüzü
- `config/settings_example.yaml`
- `app/data_access.py` içinde temel okuma/yazma fonksiyonları iskeleti

**AI IDE Komutu Örneği:**

```text
Rolün: Kıdemli Python ve Streamlit geliştiricisisin.
Proje: lgs-neural-koc, LGS öğrencisi için öğrenme koçu.
Görev: Aşağıdaki klasör yapısına göre minimal iskeleti oluştur.

Klasör yapısı:
- streamlit_app.py
- requirements.txt
- config/settings_example.yaml
- app/__init__.py
- app/data_access.py

Gereklilikler:
1. requirements.txt içinde en az şunlar olsun:
   - streamlit
   - pandas
   - openpyxl  # Excel okuma/yazma
   - pyyaml

2. config/settings_example.yaml içinde örnek ayarlar tanımla:
   - spreadsheets klasör yolu
   - varsayılan öğrenci id (pilot_ogrenci_01)

3. app/data_access.py dosyasında şu fonksiyonları tanımla (içini şimdilik pass bırak):
   - load_students_df()
   - load_questions_df()
   - load_exams_df()
   - load_answers_df()
   - load_schedule_df()
   Her biri, data/spreadsheets klasöründeki ilgili .xlsx dosyasını pandas DataFrame olarak döndürecek.

4. streamlit_app.py şu işleri yapsın:
   - Başlık: "LGS Neural-Koç – Pilot"
   - Sol tarafta öğrenci seçimi için bir selectbox (şimdilik sabit liste).
   - Ana alanda "Sistem Hazır" yazan basit bir metin göster.

Kodlar PEP8 uyumlu olsun, yorum satırları ile fonksiyonların amacını açıklayın.
```


### Faz 1 – Spreadsheet Entegrasyonu ve Basit Analiz [TAMAMLANDI]

**Hedef:**  
Gerçek soru/cevap verilerini spreadsheet’ten okuyup, pilot öğrenci için **statik** bir analiz ekranı sunmak.

**Çıktılar:**
- `app/data_access.py` içi doldurulmuş okuma fonksiyonları
- `app/analysis_engine.py` içinde temel analiz fonksiyonları
- Streamlit arayüzünde:
  - Öğrencinin son X denemedeki netleri (Mat, Türkçe, Fen)
  - Basit grafikler (bar chart / line chart)

**Önerilen Fonksiyonlar:**

```python
# app/analysis_engine.py

def get_student_exam_summary(students_df, exams_df, answers_df, student_id: str):
    """
    Verilen öğrenci için her exam_id bazında;
    ders bazlı doğru/yanlış ve toplam net değerlerini hesaplar.
    Basit bir DataFrame döndürür.
    """
    ...

def compute_lesson_stats(exam_summary_df):
    """
    Tüm sınavlar üzerinden ders bazlı ortalama net, min, max değerlerini hesaplar.
    """
    ...
```

**AI IDE Komutu Örneği:**

```text
Görev: Mevcut spreadsheet yapısına göre pilot öğrenci için statik analiz ekranı oluştur.

Dosyalar:
- app/data_access.py
- app/analysis_engine.py
- streamlit_app.py

Adımlar:
1. data_access.py içinde load_* fonksiyonlarını pandas + openpyxl ile doldur.
2. analysis_engine.py içine yukarıda tanımlanan iki fonksiyonu gerçek kodla yaz.
3. streamlit_app.py içinde:
   - Sol menüde "Analiz" sekmesi oluştur.
   - Öğrenciyi seçtikten sonra son 5 denemeyi tablo ve grafik olarak göster:
     - Tablo: Sınav adı, Türkçe net, Matematik net, Fen net, Toplam puan (varsa).
     - Grafik: Matematik netlerinin sınavlara göre line chart’ı.

Tasarım minimal ama okunabilir olsun. Kodlarda hata kontrolü ekle (dosya yoksa uyarı ver vb.).
```


### Faz 2 – Pilot Öğrenci “Bugün” Ekranı ve Zaman Çizelgesi [EKSİK]

**Hedef:**  
Pilot öğrencinin günlük rutini ile uyumlu, sadece o güne ait blokları gösteren bir “Bugün” ekranı.

**Çıktılar:**
- `app/schedule_engine.py` içinde günlük blokları veren fonksiyon.
- Streamlit’te “Bugün” sayfası:
  - Zaman çizelgesi (timeline)
  - Aktif blok (şu anki zaman hangi blokta)
  - Sıradaki blok bilgisi
  - Her blok için görev tanımı (ör: “10 soru kareköklü ifadeler”).

**Önerilen Fonksiyonlar:**

```python
# app/schedule_engine.py

from datetime import datetime, time
import pandas as pd

def get_today_blocks(schedule_df: pd.DataFrame, student_id: str, now: datetime) -> pd.DataFrame:
    """
    Verilen tarih ve öğrenci için, Schedule sheet'inden bugüne ait blokları döndürür.
    Saat sırasına göre sıralar.
    """

def find_active_block(today_blocks_df: pd.DataFrame, now: datetime):
    """
    now saatine göre hangi bloğun aktif olduğunu belirler.
    Yoksa None döndürür.
    """

def find_next_block(today_blocks_df: pd.DataFrame, now: datetime):
    """
    now sonrasındaki ilk bloğu döndürür.
    """
```

**AI IDE Komutu Örneği:**

```text
Görev: Pilot öğrenci için "Bugün" ekranını oluştur.

Dosyalar:
- app/schedule_engine.py
- streamlit_app.py

İşlevsel Gereksinimler:
1. schedule_engine.py içine yukarıdaki 3 fonksiyonu yaz.
2. streamlit_app.py içinde yeni bir sekme/menü oluştur: "Bugün".
3. "Bugün" sayfasında:
   - Bugünün tarihini göster.
   - Pilot öğrenci için get_today_blocks ile blokları al ve bir tablo olarak göster.
   - find_active_block ile mevcut bloğu, find_next_block ile sıradaki bloğu bul.
   - Görsel olarak:
     - Aktif bloğu farklı renkle veya badge ile vurgula.
     - Sıradaki blok için "Şu saatte başlayacak: ..." metni yaz.

UI tasarımında:
- Tarih ve öğrenci adı üstte yer alsın.
- Altında "Bugünkü Çalışma Blokların" başlıklı bir bölüm olsun.
```


### Faz 3 – Statik Mini Deneme Çözme Akışı [EKSİK]

**Hedef:**  
Şimdilik adaptif olmayan, sabit bir mini denemeyi seçip çözdürebileceğimiz bir akış oluşturmak.

**Çıktılar:**
- `app/exam_engine.py` içinde sabit deneme yaratma ve kayıt fonksiyonları.
- Soru çözüm ekranı (Streamlit):
  - Soru + şıklar
  - Cevap seçimi
  - Sonuç kaydı (`Answers` sheet’e).

**Önerilen Fonksiyonlar:**

```python
# app/exam_engine.py

def create_fixed_exam_for_student(exams_df, questions_df, student_id: str, lesson_filter: str, num_questions: int):
    """
    Belirli bir dersten (örn: "Matematik") rastgele veya basit kurallarla seçilmiş num_questions kadar soru ile
    yeni bir exam kaydı oluşturur.
    exams_df DataFrame'ini ve yeni exam_id'yi döndürür.
    """

def get_exam_questions(questions_df, exam_id: str):
    """
    İlgili exam_id için hangi question_id'lerin seçildiğini döndürür.
    (İlk aşamada exam_questions ilişkisini basit tutabilir, gerekirse Exams.meta_json içinde saklayabilirsin.)
    """
```

**AI IDE Komutu Örneği:**

```text
Görev: Sabit mini deneme çözme akışını oluştur.

Dosyalar:
- app/exam_engine.py
- app/data_access.py
- streamlit_app.py

Adımlar:
1. exam_engine.py içinde create_fixed_exam_for_student ve get_exam_questions fonksiyonlarını yaz.
2. data_access.py içinde Exams ve Answers için yazma fonksiyonları ekle:
   - append_exam_record(exam_obj)
   - append_answer_record(answer_obj)
3. streamlit_app.py'de yeni bir sekme: "Mini Deneme Çöz".
   - Öğrenci ve ders seçimi (sadece pilot + matematik başlatılabilir).
   - "Mini Deneme Oluştur (10 Soru)" butonu.
   - Oluşturulan exam_id için soruları sırayla göster:
     - Soru kökü (stem_text veya sadece referans)
     - Şıklar (options_json içinden)
     - Öğrencinin seçimini radio button ile al.
   - Her cevap verildiğinde Answers sheet'ine kayıt ekle.
   - Deneme bitince basit bir özet göster (doğru/yanlış sayısı).

Kod yazarken:
- Basitleştir, UI minimal ama işlevsel olsun.
- Hata kontrolü ekle (yeterli soru yoksa uyar). 
```


### Faz 4 – Gemini 2.5 Entegrasyonu: Adaptif Deneme Planlayıcı [KISMEN TAMAMLANDI - AI Koç Var, Sınav Planlayıcı Yok]

**Hedef:**  
Gemini 2.5’i kullanarak, öğrenci performans özetine göre **adaptif mini deneme planı** üretmek ve bunu uygulamaya bağlamak.

**Çıktılar:**
- `app/llm_adapter.py` içinde Gemini 2.5 ile JSON output alan genel bir fonksiyon.
- `app/exam_engine.py` içinde adaptif plan üretimi:
  - Öğrenci performans özetini hazırlayan fonksiyon
  - Gemini’den gelen plana göre soru seçen fonksiyon.

**Önerilen Fonksiyon İmzaları:**

```python
# app/llm_adapter.py

def generate_json_with_gemini(system_prompt: str, user_prompt: str, api_key: str) -> dict:
    """
    Gemini 2.5 API'sine istek yapar, çıktıyı JSON'a parse eder.
    Hataları yakalar ve anlamlı exception fırlatır.
    """

# app/exam_engine.py

def build_student_skill_summary(answers_df, questions_df, student_id: str) -> dict:
    """
    Öğrencinin son X yanıtından yola çıkarak, konu / zorluk bazlı bir özet oluşturur.
    Çıktı JSON-serializable bir dict olsun.
    """

def request_adaptive_plan_from_llm(skill_summary: dict) -> dict:
    """
    llm_adapter.generate_json_with_gemini fonksiyonunu kullanarak,
    LLM'den {"deneme_plani": [...]} yapısında bir plan ister.
    """

def create_adaptive_exam(exams_df, questions_df, student_id: str, plan: dict):
    """
    LLM'den gelen plana göre veritabanındaki sorulardan seçim yaparak yeni bir exam oluşturur.
    """
```

**AI IDE Komutu Örneği (Gemini tarafı):**

```text
Rolün: Gemini 2.5 ile çalışan bir Python geliştiricisisin.

Görev: app/llm_adapter.py içinde generate_json_with_gemini fonksiyonunu yaz.

Gereksinimler:
- Google'ın resmi Python client'ını veya basit HTTPS isteğini kullan.
- Parametreler: system_prompt (string), user_prompt (string), api_key (string).
- LLM'den JSON formatlı yanıt bekle. Yanıtı güvenli şekilde parse et (try/except).
- Hata durumunda anlamlı exception veya None döndür, Streamlit tarafında gösterilebilir bir mesaj üretilebilsin.
```

**AI IDE Komutu Örneği (adaptif plan):**

```text
Görev: exam_engine içinde adaptif deneme üretimini bağla.

Adımlar:
1. build_student_skill_summary:
   - Answers ve Questions DataFrame'lerini kullanarak,
   - Öğrencinin konu ve zorluk bazlı doğru/yanlış istatistiklerini çıkar.
   - {"matematik": {"karekoklu_sayilar": {"z3": {"dogru": x, "yanlis": y}, ...}}} gibi bir yapı döndür.

2. request_adaptive_plan_from_llm:
   - llm_adapter.generate_json_with_gemini ile skill_summary'i user_prompt olarak gönder.
   - LLM'den şu formatta yanıt iste:
     {
       "deneme_plani": [
         {"lesson": "matematik", "topic": "karekoklu_sayilar", "difficulty": 3, "adet": 5},
         ...
       ]
     }

3. create_adaptive_exam:
   - Plandaki her blok için Questions DataFrame'inden ilgili soruları filtrele.
   - Yeterli soru yoksa graceful degrade et (daha düşük zorluk veya benzer konu).
   - exams.xlsx ve answers.xlsx yapısına uygun yeni exam kaydı oluştur.

4. streamlit_app.py:
   - "Adaptif Deneme Çöz" adlı yeni bir sekme ekle.
   - Öğrencinin son performansına göre "Adaptif Deneme Oluştur" butonu olsun.
   - Sonrasında Faz 3'teki soru çözme akışıyla aynı şekilde sorular çözdürülsün.
```


### Faz 5 – “Bu Konuyu Öğret” Akışı (Teaching Engine) [TAMAMLANDI]

**Hedef:**  
Öğrencinin yanlış yaptığı bir soruya tıklayıp **AI koçlu bir mini ders** almasını sağlayan akış.

**Çıktılar:**
- `app/teaching_engine.py` içinde LLM ile konuşan öğretim fonksiyonları.
- Streamlit’te:
  - Analiz ekranında yanlış sorular listesi
  - Her yanlış sorunun yanında “Bu konuyu öğret” butonu
  - tıklanınca açılan dialog/modal içinde chat arayüzü

**Önerilen Fonksiyonlar:**

```python
# app/teaching_engine.py

def build_teaching_prompt(question_row, student_answer_row) -> str:
    """
    Soru metni, doğru cevap, öğrencinin verdiği cevap ve soru etiketi (topic/subtopic)
    kullanılarak, Gemini'ye gönderilecek user_prompt metnini oluşturur.
    """

def get_teaching_response(question_row, student_answer_row, api_key: str) -> str:
    """
    llm_adapter.generate_json_with_gemini veya benzer chat fonksiyonunu kullanarak,
    öğrenciye yönelik açıklamayı metin olarak döndürür.
    """
```

**Gemini Prompt Taslağı (Türkçe):**

```text
Rolün: LGS öğrencilerine sınav koçluğu yapan, sabırlı ve açıklayıcı bir öğretmensin.
Öğrenci 8. sınıf seviyesinde, zaman zaman özgüvensiz fakat potansiyeli yüksek.

Sana bir LGS sorusu, doğru cevap ve öğrencinin verdiği cevap verilecek.
Görevin:
1. Önce sorunun ne istediğini sade bir dille özetle.
2. Ardından adım adım çözüm yolunu açıkla.
3. Öğrencinin büyük ihtimalle nerede hata yaptığını sezgisel olarak belirt (yargılamadan).
4. En sonunda, benzer seviyede KISA bir mini soru ver ve cevabını da açıkla.

Üslubun:
- Yargılayıcı değil, koç gibi.
- "Bak bunu nasıl yapmışsın!" yerine "Şu kısmı karıştırmış olabilirsin" tarzında ol.
- Cevapları mümkün olduğunca LGS seviyesine uygun, gereksiz teorik detay olmadan ver.

Çıktıyı sade düz metin olarak üret.
```

**AI IDE Komutu Örneği:**

```text
Görev: teaching_engine.py ve Streamlit arayüzüne "Bu konuyu öğret" özelliğini ekle.

Adımlar:
1. teaching_engine.build_teaching_prompt ve get_teaching_response fonksiyonlarını yaz.
2. analysis ekranında (Faz 1'de yaptığın ekran) her yanlış soru için bir satır veya kart göster.
3. Her satırda "Bu konuyu öğret" butonu olsun.
4. Buton tıklanınca st.dialog veya st.modal kullanarak bir pencere aç.
5. Bu pencerede:
   - Soru metnini özet halinde göster.
   - Gemini'den gelen açıklamayı ve mini soruyu chat tarzında göster.

Teknik not:
- LLM çağrıları sırasında yükleniyor göstergesi (spinner) ekle.
- Hata durumunda kullanıcıya anlaşılır mesaj ver.
```


### Faz 6 – Günlük Plan, Sayaç ve Zeigarnik Halkası [DEVAM EDİYOR]

**Hedef:**  
Pilot öğrenciyi günlük planda tutacak **interaktif saat ve progress** bileşenleri eklemek.

**Çıktılar:**
- `app/ui_components.py` içinde:
  - Günlük progress halkası (progress ring)
  - Blok içi geri sayım sayacı (timer)
- `app/schedule_engine.py` içinde:
  - Günlük tamamlanan blokları işaretleme fonksiyonları.
- Streamlit “Bugün” ekranında:
  - Günlük tamamlanma yüzdesi
  - Aktif blok için geri sayım
  - Blok bitince otomatik “Tamamlandı” işareti

**Önerilen Ek Fonksiyonlar:**

```python
# app/schedule_engine.py

def mark_block_completed(schedule_df, schedule_id: str):
    """
    Schedule sheet içinde ilgili bloğu 'tamamlandı' olarak işaretler.
    Gerekirse yeni bir kolon (is_completed_today) kullanılabilir.
    """

def compute_today_completion_percent(today_blocks_df) -> float:
    """
    Bugün için planlanan bloklardan kaçı tamamlanmış -> % hesapla.
    """
```

**AI IDE Komutu Örneği:**

```text
Görev: "Bugün" ekranını zaman ve progress açısından zenginleştir.

Adımlar:
1. schedule_engine içine mark_block_completed ve compute_today_completion_percent fonksiyonlarını ekle.
2. ui_components.py içinde şu yardımcıları yaz:
   - render_progress_ring(percentage: float)
   - render_block_timer(block_start, block_end, now)
3. "Bugün" sayfasında:
   - Üstte "Bugünkü Hedeflerin" başlığı ve progress ring.
   - Altta blok listesi.
   - Aktif blok seçiliyken yanına "Blok Çalışmasını Başlat" butonu.
   - Başlatılınca:
     - Timer çalışsın (Streamlit'te periyodik rerun yaklaşımı kullanılabilir).
     - Blok bitince kullanıcıya "Bloku tamamladın mı?" diye soran diyalog.
     - Onaylarsa mark_block_completed çağrılır, progress güncellenir.
```


### Faz 7 – Temizlik, Refaktör ve Geleceğe Hazırlık [DEVAM EDİYOR]

**Hedef:**  
Kodun modülerleştirilmesi, TODO’ların yazılması ve ileride Postgres / çoklu kullanıcıya geçiş için hazırlık yapılması.

**Çıktılar:**
- Fonksiyon seviyesinde docstring’ler
- `README.md` ve `docs/` klasöründe geliştirici dokümantasyonu
- Postgres’e migrasyon için kaba şema taslağı
- Çoklu öğrenci desteği için yapılacak işler listesi

### Faz 8 – UX & Engagement Polish [DEVAM EDİYOR]

**Hedef:**
Uygulamayı "Enterprise" seviyesinden "Premium Product" seviyesine taşımak. Kullanıcı deneyimini (UX) iyileştirmek ve nöro-eğitim ilkelerini (Zeigarnik etkisi, Dopamin döngüsü) arayüzde daha baskın hale getirmek.

**Yapılacaklar:**
1.  **Action-Oriented Ana Sayfa:**
    -   "Ana Sayfa" ve "Bugün" ekranlarını birleştir.
    -   Öğrenci uygulamayı açar açmaz dashboard yerine direkt "Sıradaki Görev" kartını görmeli.
    -   Zeigarnik etkisini tetiklemek için yarım kalan işler vurgulanmalı.

2.  **Görsel Zenginleştirme:**
    -   "Mini Deneme" seçim kartlarını dinamik ve renkli hale getir.
    -   Konu başlıklarını (örn: "Kareköklü İfadeler") kartlarda açıkça göster.
    -   Daha canlı renk paletleri ve ikonlar kullan.

**AI IDE Komutu Örneği:**

```text
Görev: UX iyileştirmelerini uygula.

Adımlar:
1. app.py'yi düzenle: Varsayılan açılış sayfasında (Ana Sayfa) bugünün özetini ve aktif bloğu göster.
2. pages/mini_deneme.py'yi düzenle: Sınav seçim kartlarını HTML/CSS ile zenginleştir, rastgele konu isimleri yerine gerçekçi başlıklar kullan.
```

**AI IDE Komutu Örneği:**

```text
Görev: Kod tabanını refaktör et ve geliştirici dokümantasyonu üret.

Adımlar:
1. Tüm app/*.py dosyalarını gözden geçir:
   - Gereksiz tekrarları kaldır.
   - Fonksiyon isimlerini anlamlılaştır.
   - Docstring ekle (parametre ve return açıklamaları).
2. Proje köküne README.md dosyasını yaz:
   - Projenin amacı
   - Kurulum adımları
   - Çalıştırma komutu (streamlit run streamlit_app.py)
   - Kısa mimari özeti
3. docs/ klasörünü oluştur ve içinde:
   - "data_model.md": Spreadsheet sütunları ve anlamları
   - "llm_prompts.md": Kullanılan Gemini prompt şablonları
   - "future_work.md": Postgres migrasyonu, çoklu kullanıcı, kurumsal sürüm notları
4. Kodun genelinde PEP8 uyumunu kontrol et.
```


---

## 5. Pilot Öğrenciye Özgü Davranışsal Tasarım Notları

Bu bölüm kod değil, ama AI IDE’ye “metin üret”, “UI yazıları üret” dediğinde referans alabileceği net maddeleri içerir.

1. **Bildirim Dili**
   - Yargılayıcı değil, koç gibi.
   - “Hadi ders çalış artık” yerine:
     - “Bugünkü 10 soruluk sprintini bitirirsen matematik borcun kapanıyor.”
     - “Bu blok 25 dakika. Sonrasında 10 dk ekran dışı mola var.”

2. **Günlük Plan Basitliği**
   - En fazla 2–3 blok / gün (özellikle ev çalışmaları).
   - Her blok = 20–30 dakika.
   - Her blok = net, ölçülebilir görev (örn: “10 soru kareköklü ifadeler”).

3. **Analog Mola Hatırlatıcı**
   - Blok bitiminde:
     - “Şimdi 10 dakika analog mola: su iç, balkona çık, telefondan uzak dur.”

4. **Zeigarnik Etkisi Kullanımı**
   - Günlük hedef halkası (progress ring) asla %0 veya %100 dışında bırakılmamalı.
   - Öğrenci bir blok bitirdiğinde:
     - “Bugünlük hedefinin %50’si tamamlandı, sadece 1 blok kaldı.” gibi metinler kullanılmalı.

5. **Ödül Çerçevesi**
   - Uygulama oyun değil ama:
     - Blok sayacı, streak mantığı, mini başarı rozetleri düşünülebilir.
   - Pilot aşamada basit tut:
     - Arka arkaya 3 gün hedefini tamamladı → küçük bir görsel rozet.


---

## 6. Geleceğe Yönelik Ek Fikirler (Şimdilik Yalnızca Not Olarak)

Bu bölüm, ileride AI IDE’ye “yeni feature yaz” dendiğinde kullanılmak üzere fikir bankasıdır.

- **Dijital Hata Defteri 2.0**
  - Yanlış yapılan soruların belirli aralıklarla tekrar karşısına çıkması (24 saat, 3 gün, 7 gün).
  - “Zombi soru” mantığı: doğru yapılana kadar sistem peşini bırakmaz.
- **Ebeveyn Kokpiti**
  - Öğrencinin günlük/haftalık blok tamamlanma oranı
  - En çok zorlandığı konular
  - Dijital detoks uyum oranı (tahmini).
- **Kendi Ürettiği Sorular**
  - Gemini 2.5’i kullanarak, yayınevlerine benzeyen ama kopya olmayan sorular üretmek.
  - Bu sorular “Neural-Koç Özel Soru Havuzu”nda tutulabilir.

---

## 7. Son Not – Bu Yol Haritasını Nasıl Kullanmalı?

- Bu .md dosyası, AI IDE (Cursor, Windsurf vb.) için bir **“proje sözleşmesi”** gibi düşünülmelidir.
- Her fazı sırayla veya ihtiyaca göre atlayarak kullanabilirsiniz, ancak:
  - Faz 0–1–2 tamamlanmadan Faz 4–5 (LLM + Teaching) tarafına geçmek önerilmez.
- Her yeni özellik eklenirken:
  - Önce bu dokümanda ilgili bölümü bulun,
  - Sonra oradaki fonksiyon imzalarını ve AI IDE komut metinlerini prompt’a yapıştırın,
  - Üretilen kodu test edip, gerektiğinde elinizle düzeltin.

Bu yol haritası, elinizdeki mevcut basit Python + spreadsheet + Gemini 2.5 + Streamlit kurulumunu:

- Pedagojik olarak daha anlamlı,
- Teknik olarak daha modüler,
- Uzun vadede Postgres + çoklu kullanıcıya taşınabilir,

bir ürüne dönüştürmeniz için tasarlanmıştır.

---

# BÖLÜM III — Ek Fikirler ve Geliştirme Analizleri (TAM METİN)

Bu bölüm, `lgs_neural_koc_ek_fikirler_ve_gelistirme.md` dosyasının **değiştirilmemiş** tam metnidir.
Motivasyon, UX, gamification, ileri analitik ve ürün fikirleri bu ek bölümde tutulur.

---
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

---

## Çakışma / Öncelik Kuralları

Aynı konu farklı bölümlerde farklı ifade edildiyse:

1) **Bölüm I (Faz Sözleşmeleri)** bağlayıcıdır.  
2) **Dosya & Klasör Sözleşmesi** teknik yapı konusunda bağlayıcıdır.  
3) Bölüm II ve III referans/örnek/ilham amaçlıdır.

---

## Kapanış

Bu v3.1 tek dosya sürümü, senin en baştan istediğin iki şeyi aynı anda sağlar:

- **Enterprise seviyede sürdürülebilir ve profesyonel bir yol haritası**
- **AI IDE’nin yorum şansı bırakmayan, DoD’li faz sözleşmeleri**
- **Üstelik eski 800+ satırlık detaylar kaybolmadan tek dosyada korunur**

Bundan sonra IDE’ye iş verirken,
yalnızca bu dosyayı “Master Context” yapman yeterli olacaktır.
