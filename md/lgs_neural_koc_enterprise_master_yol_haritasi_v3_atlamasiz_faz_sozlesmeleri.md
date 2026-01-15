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

- **FAZ A:** MVP Stabilizasyonu ve Temel Veri Omurgası  
- **FAZ B:** Günlük Rutin + Motivasyon Çekirdeği  
- **FAZ C:** Gerçek Adaptif Soru Motoru (CAT-Lite)  
- **FAZ D:** Eğitim Katmanı (Content/Curriculum) + Manuel → Yarı Otomatik PDF  
- **FAZ E:** Ürün Kalitesi, Observability, PromptOps, Feature Ops  
- **FAZ F:** Sheets → Supabase + Çoklu Öğrenci  
- **FAZ G:** Enterprise Analitik + Ebeveyn/Koç Kokpiti  

---

# FAZ A — MVP Stabilizasyonu ve Temel Veri Omurgası

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

# FAZ B — Günlük Rutin + Motivasyon Çekirdeği

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

# FAZ C — Gerçek Adaptif Soru Motoru (CAT-Lite)

## Amaç
Mikro-skill bazlı, zorluk dengeli **gerçek adaptif mini deneme** üretimini çalışır hale getirmek.  
Bu faz, eski planlardaki “Faz 4 Fix (Gerçek Adaptif Mantık)” adımının karşılığıdır.

## Bağımlılık
FAZ A-B

## Pre-DoD
**Questions** zorunlu kolonları dolu:
- `lesson, topic, subtopic, difficulty_label, question_origin, options_json, correct_option, active`

**Answers** zorunlu kolonları dolu:
- `is_correct, created_at`

## SERT KURALLAR
1) **LLM sadece PLAN üretir.** Final seçim Python ile.  
2) `difficulty_label` yoksa adaptif seçim devreye alınmaz.  
3) `question_origin` boşsa soru pasif kabul edilir.  
4) Yetersiz soru fallback zinciri zorunlu:
   - subtopic içi zorluk kaydır → topic genişlet → ders geneli kontrollü aç

## Dosya/Modül Sınırı
- `app/data_access.py`
- `app/analysis_engine.py`
- `app/exam_engine.py`
- `app/llm_adapter.py`
- `streamlit_app.py`

## Fonksiyon Paketi
- `compute_mastery_scores(student_id)`  
- `build_student_skill_summary(student_id)`  
- `request_adaptive_plan_from_llm(summary)`  
- `create_adaptive_exam(student_id, plan)`  
- `detect_negative_trend(student_id)`  
- `create_moral_booster_exam(student_id)`

## UI Paketi
- “Adaptif Deneme Oluştur”  
- Negatif trend banner → “Moral Denemesi”

## Test Paketi (Min)
1) Normal veri → adaptif exam oluşuyor.  
2) Yetersiz subtopic soru → fallback çalışıyor.  
3) LLM JSON parse hatası → rule-based fallback.

## DoD
- 15 soruluk adaptif deneme 60 sn altında.  
- Plan JSON kaydediliyor.  
- Moral banner tetikleniyor.  
- 3 pytest yeşil.

## AI IDE Komut Paketi
```text
MASTER SÖZLEŞME — FAZ C

SERT KURALLAR:
1) LLM sadece PLAN üretir; final soru seçimi Python ile yapılır.
2) difficulty_label ve question_origin zorunlu.
3) Yetersiz soru fallback zinciri zorunlu.
4) Plan JSON strict schema ile doğrulanacak.
5) 3 pytest yazılacak.

Dosyalar:
- app/data_access.py
- app/analysis_engine.py
- app/exam_engine.py
- app/llm_adapter.py
- streamlit_app.py
- tests/test_phase_c.py

Görev:
C1) Mastery + skill summary.
C2) LLM planlayıcı (schema strict).
C3) create_adaptive_exam + fallback.
C4) Moral booster.
C5) UI buton + banner.
C6) 3 test.

Kabul Kriterleri:
- Adaptif exam < 60 sn.
- Fallback çökmeden çalışıyor.
```

---

# FAZ D — Eğitim Katmanı (Content/Curriculum) + Manuel → Yarı Otomatik PDF

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

# FAZ E — Ürün Kalitesi, Observability, PromptOps, Feature Ops

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

# FAZ F — Sheets → Supabase + Çoklu Öğrenci

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

# FAZ G — Enterprise Analitik + Ebeveyn/Koç Kokpiti

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
