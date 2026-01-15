# LGS Neural-Koç – TEK DOSYA Enterprise Master Sözleşme Yol Haritası (v2)
## Soru Motoru + Eğitim Katmanı + Davranış Tasarımı + Operasyon + Ölçeklenebilir Mimari
### Pilot (1 öğrenci) → Çoklu Öğrenci → Ürünleşme → Enterprise-grade Platform

Bu dosya, aşağıdaki dokümanların **tamamını** tek bir “master sözleşme” çatısı altında birleştirir:

1. **Ana ürün/soru motoru yol haritası** (tam metin eklendi)  
2. **Ek fikirler ve ileri seviye geliştirmeler** (tam metin eklendi)  
3. **Eğitim katmanı + PDF içe aktarma v4 detay planı** (tam metin eklendi)  
4. **Enterprise master v1 birleşik plan** (bu dosyanın çekirdeği)

> Bu v2 sürümünün hedefi:  
> - AI IDE’nin “yorumlayıp kısaltma” davranışını engellemek,  
> - Faz kapılarını daha sert hale getirmek,  
> - Eski dokümanların hiçbir detayını kaybetmeden tek yerde toplamak,  
> - “Eğitim katmanı hangi fazda devreye giriyor?” sorusunu net ve bağlayıcı hale getirmek.

---

## NASIL KULLANILIR (Zorunlu Kullanım Protokolü)

### 1) Master Context
Bu dosyayı IDE’de proje klasörünün köküne koy ve her iş paketinde “master context” olarak referans ver.

### 2) Faz-kapılı ilerleme
Bu dosyada tanımlanan **DoD** sağlanmadan bir sonraki faza geçilmez.

### 3) SERT KURAL SETİ
Aşağıdaki global kurallar tüm fazlarda bağlayıcıdır:

- **LLM çağrıları tek kapı:** `app/llm_adapter.py`  
- **Veri erişimi tek kapı:** `app/data_access.py`  
- **Sheet kolonları DB-ready tutulur.**  
- **Soru kaynağı zorunlu etiket:** `question_origin`  
- **İçerik kaynağı zorunlu etiket:** `source_type`  
- **UI 3 kart kuralı:** Öğrenci ekranında aynı anda en fazla 3 ana odak.

### 4) Pilot gerçekliği
Pilot öğrenci “zor profil” olduğu için:
- “başlama sürtünmesini” azaltan özellikler önceliklidir.
- Üst üste büyük feature yüklenmez; feature flags zorunludur.

---

## Bölüm I — Enterprise Master v1 Çekirdek Plan (Güncellenmiş)
Aşağıdaki bölüm, v1 master sözleşmenin tam metnidir ve v2 içinde **normatif çekirdek** olarak geçerlidir.


# LGS Neural-Koç – Enterprise Sözleşme Yol Haritası (Tek Dosya)
## Pilot → Ürünleşme → Ölçeklenebilir Platform
### Mevcut Stack: Python + Google Sheets (geçici) + Gemini 2.5 + Streamlit
### Hedef: AI IDE’nin yorum yapmadan uygulayabileceği, faz-kapılı ve DoD’li master plan

> Bu doküman, daha önce oluşturulan:
> - **Uçtan uca teknik + pedagojik yol haritasını**
> - **ek fikirler / davranış tasarımı geliştirmelerini**
> - **eğitim katmanı + PDF içe aktarım planını**
> tek bir “enterprise düzeyi proje sözleşmesine” dönüştürür.
>
> Bu dokümanı AI IDE’ye “Master Context” olarak verip,
> her iş paketini ayrı ayrı komut bloklarıyla uygulatman hedeflenir.

---

## 0) Vizyon, Amaç ve Başarı Tanımı

### 0.1 Vizyon
**LGS Neural-Koç**, tek bir öğrenciden başlayıp çoklu kullanıcıya evrilebilecek şekilde tasarlanmış;
**Tanı → Reçete → Müdahale** döngüsüyle çalışan adaptif bir öğrenme koçu/ERP yaklaşımıdır.  
Bu yaklaşım, mimari dokümanda tanımlanan “Diagnosis → Prescription → Intervention” çekirdeğinin ürünleştirilmiş halidir.

### 0.2 Ürünün 3 Değer Sütunu
1. **Soru-temelli koçluk**
   - Deneme/mini deneme üretimi
   - Mikro-kazanç (micro-skill) bazlı zayıflık tespiti  
2. **Eğitim-temelli koçluk**
   - Yanlış sorudan “tam zamanında” mini ders  
   - PDF’lerden yarı-otomatik içerik çıkarımı ve kişiselleştirme  
3. **Davranış-temelli sürdürülebilirlik**
   - Günlük rutin, kısa bloklar, analog mola
   - Streak, küçük zafer özetleri, moral setleri

### 0.3 Pilot Başarı Kriterleri (Ölçülebilir)
Pilot öğrenci için 4 haftalık ölçekte:

- Haftada en az 4 gün sistem kullanımı
- Günlük blokların %60+ tamamlama oranı
- Matematik doğruluk oranında istikrarlı artış trendi
- “Bu konuyu öğret” kullanımının haftada en az 3 kez gerçekleşmesi

### 0.4 Ürünleşme Başarı Kriterleri
- Çoklu öğrenci desteği
- Verinin Sheets → Postgres/Supabase’e taşınabilmesi
- LLM sağlayıcısının değiştirilebilir olması
- Güvenlik, loglama, sürümleme ve test altyapısının oturması

---

## 1) Kapsam, Varsayımlar, Sınırlar

### 1.1 Kapsam
- LGS düzeyi (8. sınıf)
- İlk etapta **tek pilot öğrenci**
- Matematik + Türkçe öncelikli
- Streamlit üzerinde hızlı iterasyon

### 1.2 Varsayımlar
- Gemini 2.5 multimodal kullanılacak.
- Başlangıçta Google Sheets “geçici veri katmanı”.
- Soru havuzunda farklı yayınevlerinden (zorluk profili farklı) içerikler bulunacak.
- Aynı zamanda **AI üretimi** ve **MEB kazanım tabanlı** içerikler için ayrı etiket alanları olacaktır.

### 1.3 Sınırlar / Non-Goals (MVP’de)
- Tam otomatik OCR/HTR pipeline’ının kusursuzluğu
- Tam ölçekli mobil uygulama
- Kurumsal satılabilir SaaS lisanslama

---

## 2) Hukuki ve Etik Kullanım Notu (Pilot-odaklı, sade)
Pilot seviyesinde kapalı kullanım çoğu zaman pratikte düşük riskli algılansa da,
**ölçekleme** düşünülürse:

- Yayınevi sorularıyla **fine-tune** yerine  
  **veriyi kendi depolayıp seçim/analiz/planlama yaptıran** yaklaşım daha güvenlidir.
- Soru kaynağı mutlaka etiketlenmelidir:
  - `publisher`
  - `meb`
  - `ai_original`
  - `ai_variant_of_pool` (kontrollü varyант)

Bu alanlar, ileride ürünleşirken hukuki temizlik için kritik olacaktır.

---

## 3) Sistem Mimarisi (Pilot → Enterprise Taşınabilir)

### 3.1 Katmanlar
1. **UI** (Streamlit, sonra React)
2. **Uygulama Servisleri (Python)**
   - `data_access`
   - `analysis_engine`
   - `exam_engine`
   - `teaching_engine`
   - `content_engine` (Eğitim katmanı)
   - `schedule_engine`
   - `llm_adapter`
3. **Veri**
   - Şimdi: Google Sheets
   - Sonra: Supabase/Postgres
4. **LLM & ML**
   - Gemini 2.5
   - Gelecekte opsiyonel lokal LLM
5. **Observability & QA**
   - Event log
   - Prompt/version kontrolü
   - Eval setleri

### 3.2 Çekirdek Döngü
1. **Veri Girişi**
   - Deneme sonuçları
   - Soru çözümü kayıtları
   - PDF içerikleri (çözümlü kitapçık vb.)  
2. **Tanı**
   - Konu/alt konu/zorluk bazlı performans
   - Trend analizi
   - Dikkat/işlem/okuma hatası sınıfları
3. **Reçete**
   - Zorluk dengeli mini deneme planı
   - Günlük çalışma blokları
   - Mikro ders önerileri
4. **Müdahale**
   - Soru çözümü
   - “Bu konuyu öğret”
   - Moral booster
5. **Geri Besleme**
   - Mastery skorları
   - Plan adaptasyonu

---

## 4) Veri Modeli (Sheets V1 → DB-Ready V2)

> Bu bölüm “tek sefer doğru tasarla, sonra taşı” mantığıyla yazıldı.

### 4.1 Zorunlu Tablolar / Sheets

#### 4.1.1 Students
- `student_id`
- `name`
- `grade`
- `school`
- `profile_notes`
- `active`

#### 4.1.2 Questions
Zenginleştirilmiş şema:

- `question_id`
- `lesson`
- `topic`
- `subtopic`
- `difficulty_label` (1-5)
- `type`
- `publisher` (nullable)
- `source_book` (nullable)
- `page_ref` (nullable)
- `stem_text` (nullable)
- `options_json`
- `correct_option`
- `media_ref` (nullable)
- `question_origin`  
  - `publisher`
  - `meb`
  - `ai_original`
  - `ai_variant_of_pool`
- `origin_parent_question_id` (nullable)  
  - varyant üretildiyse kök soru id
- `active`

> **Not:** Bu alanlar, hibrit soru stratejini temiz şekilde yönetebilmek için tasarlandı.

#### 4.1.3 Exams
- `exam_id`
- `student_id`
- `title`
- `mode`  
  - `fixed`
  - `adaptive`
  - `topic_scan`
  - `moral_booster`
- `created_at`
- `status`
- `meta_json`  
  - hedef konu-zorluk dağılımı
  - soru seçim kuralı
  - plan kaynağı (LLM/kurallar)

#### 4.1.4 ExamQuestions (Yeni – ilişki tablosu)
Sheets’te ayrı sheet olarak önerilir.

- `exam_id`
- `question_id`
- `order_index`

> Böylece `meta_json` karmaşası azalır.

#### 4.1.5 Answers
- `answer_id`
- `exam_id`
- `question_id`
- `student_id`
- `given_option`
- `is_correct`
- `time_spent_sec`
- `attempt_type`
- `created_at`

#### 4.1.6 Schedule
- `schedule_id`
- `student_id`
- `date` (opsiyonel; olmayanlar “template” kabul edilir)
- `day_of_week`
- `block_start`
- `block_end`
- `block_type`
- `task_type`
- `target_desc`
- `is_active`
- `is_completed`

### 4.2 Eğitim Katmanı İçin Ek Tablolar

#### 4.2.1 ContentItems
PDF’den veya manuel girdiden türetilen atomik içerik birimi.

- `content_id`
- `lesson`
- `topic`
- `subtopic`
- `content_type`  
  - `concept_card`
  - `worked_example`
  - `mini_lesson`
  - `strategy_note`
- `source_origin`
  - `publisher_summary`
  - `meb`
  - `ai_original`
- `source_ref` (kitap, sayfa, link)
- `summary_text` (kısa)
- `core_points_json`
- `difficulty_hint`
- `active`

#### 4.2.2 CurriculumMap
- `curriculum_id`
- `lesson`
- `topic`
- `subtopic`
- `meb_outcome_text` (kısa)
- `priority_weight` (1-5)
- `recommended_order`

#### 4.2.3 StudentContentProgress
- `student_id`
- `content_id`
- `status`  
  - `not_seen`
  - `seen`
  - `practiced`
  - `mastered`
- `last_seen_at`

---

## 5) LLM Stratejisi (Gemini 2.5 Odaklı)

### 5.1 LLM Adapter Zorunluluğu
Tüm LLM çağrıları **tek kapıdan** geçer:

- `llm_generate_json(task, payload)`
- `llm_chat(task, payload)`

Bu sayede provider değişimi sadece adapter dosyasında çözülür.

### 5.2 PromptOps
- Her task için version’lı prompt şablonları
- Prompt çıktısı + input payload loglanır
- Pilot boyunca “prompt regression” kontrolleri yapılır

### 5.3 Hibrit Soru Kullanımı (Yayınevi + AI)
Soru havuzunda:

- Yayınevi soruları
- MEB örnek soruları
- AI üretimi özgün sorular
- AI kontrollü varyantlar

**Kural:**  
AI varyant üretimi **her zaman** şu 3 güvenlik filtresinden geçer:
1. **Kazanım uyumu**
2. **Sayısal/bağlamsal değişim zorunluluğu**
3. **Benzerlik kontrolü (manuel veya ikinci AI)**

---

## 6) Davranışsal Tasarım (Pilot Öğrenci için “Zor Profil” Modu)

### 6.1 İlkeler
- Ev çalışması **saat odaklı değil, görev odaklı ve kısa**  
- Günde en fazla 2–3 ev bloğu
- Her blok 20–30 dakika
- Blok sonrası analog mola

### 6.2 Dijital Nudging Araçları
- Uygulama içi:
  - “Bugünlük Küçük Zafer”
  - Streak göstergesi
  - Progress ring
- Uygulama dışı (hafif entegre):
  - Bilgisayar bildirimleri
  - Takvim hatırlatmaları
  - Basit masaüstü widget/overlay (opsiyonel)

### 6.3 Kriz Müdahaleleri
- **Moral Booster Denemesi**
- **Warmup Mode**
  - Çok kolay başlangıç
  - düşük sürtünmeyle tekrar sisteme bağlama

---

## 7) Faz-Kapılı Master Yol Haritası

> Bu bölüm, önceki faz planlarını tek bir enterprise sıralamasında birleştirir.
> Her fazda:
> - Amaç
> - Bağımlılıklar
> - Teslimatlar
> - Definition of Done
> - AI IDE Komut Paketi

### FAZ A — Mevcut MVP’yi Stabilize Et (ŞİMDİ)
**Amaç:**  
Halihazırda kurduğun Python + Sheets + Gemini + Streamlit yapısını  
“kırılmayan, ölçülebilir ve modüler” hale getirmek.

**Bağımlılık:** yok

**Teslimatlar:**
- Standart klasör yapısı
- data_access okunur/yazılır
- basic analiz ekranı
- sabit mini deneme akışı (en az Matematik)
- LLM adapter v1

**DoD:**
- Yeni bir exam oluşturulup Answers’a 10+ kayıt düşebiliyor.
- Analiz ekranı son 5 oturumu doğru gösteriyor.
- Kod modüllerinin her biri docstring içeriyor.
- `config/settings.yaml` ile çalışma yolu değiştirilebiliyor.

**AI IDE Komut Paketi:**
```text
MASTER SÖZLEŞME — FAZ A

Rolün: Kıdemli Python/Streamlit mimarı.
Amaç: LGS Neural-Koç MVP stabilizasyonu.

SERT KURALLAR:
1) Yeni dosya açma/isim değiştirme yapma; yalnızca bu listede geçen dosyaları kullan.
2) Her fonksiyonun docstring'i ve type hint’i olacak.
3) Her modülde en az 1 basit unit test stub’ı yaz (pytest).
4) Sheets erişimi tek bir data_access katmanında olacak.
5) LLM çağrısı yalnızca llm_adapter üzerinden yapılacak.

Dosyalar:
- streamlit_app.py
- app/data_access.py
- app/analysis_engine.py
- app/exam_engine.py
- app/llm_adapter.py
- config/settings_example.yaml
- requirements.txt

Görev:
A1) data_access okuma/yazma fonksiyonlarını tamamla.
A2) Sabit mini deneme oluştur + çözme UI akışını bitir.
A3) Analiz sayfasında ders bazlı özet ve son 5 deneme tablosu göster.
A4) LLM adapter içine JSON üretim yardımcı fonksiyonunu ekle (provider=Gemini 2.5).
A5) Basit pytest iskeletini oluştur.

Kabul Kriterleri:
- “Mini Deneme Oluştur” → sorular sırayla çözülür → Answers sheet’e kayıt düşer.
- Uygulama errorsız çalışır.
```

---

### FAZ B — Günlük Rutin Motoru + Engagement
**Amaç:**  
Pilot öğrencinin sisteme tutunması.

**Bağımlılık:** Faz A

**Teslimatlar:**
- “Bugün” ekranı
- Aktif blok + sıradaki blok
- Progress ring + timer
- Gün sonu küçük zafer özeti

**DoD:**
- Schedule sheet’e göre bugünün blokları listeleniyor.
- En az 1 blok manuel “tamamlandı” işaretlenebiliyor.
- Progress yüzdesi anlık güncelleniyor.
- Gün sonu özet metni veriye dayanarak üretiliyor.

**AI IDE Komut Paketi:**
```text
MASTER SÖZLEŞME — FAZ B

SERT KURALLAR:
1) UI sade; öğrenci ekranında aynı anda en fazla 3 ana kart göster.
2) Timer, Streamlit rerun döngüsünü kilitlemeyecek şekilde yazılacak.
3) “Bugün” ekranı veri yoksa fallback metinleri gösterecek.

Dosyalar:
- app/schedule_engine.py
- app/ui_components.py
- app/analysis_engine.py
- streamlit_app.py

Görev:
B1) get_today_blocks / find_active_block / find_next_block yaz.
B2) mark_block_completed + compute_today_completion_percent ekle.
B3) compute_daily_summary fonksiyonunu ekle.
B4) “Bugün” ekranına:
    - timeline tablo
    - aktif blok vurgusu
    - progress ring
    - gün sonu küçük zafer kutusu

Kabul Kriterleri:
- Pilot öğrenci için bugünün planı 10 sn içinde yükleniyor.
- 1 tıkla blok tamamlandı işaretlenebiliyor.
```

---

### FAZ C — Adaptif Soru Motoru (CAT-Lite)
**Amaç:**  
Mikro-skill bazlı, zorluk dengeli adaptif mini deneme.

**Bağımlılık:** Faz A-B

**Teslimatlar:**
- Mastery skorları
- LLM planlayıcı + kural tabanlı seçim
- Moral booster akışı

**DoD:**
- `compute_mastery_scores` çalışıyor.
- Adaptif plan JSON’u kaydediliyor.
- Sorular `lesson/topic/difficulty` ile gerçekten filtreleniyor.
- Negatif trend → moral set önerisi UI’da çıkıyor.

**AI IDE Komut Paketi:**
```text
MASTER SÖZLEŞME — FAZ C

SERT KURALLAR:
1) LLM yalnız plan üretir; soru seçimi Python kurallarıyla finalize edilir.
2) Zorluk etiketi veri tabanında tek kaynak doğruluktur.
3) Yetersiz soru durumunda “graceful degrade” kuralı zorunlu.

Dosyalar:
- app/analysis_engine.py
- app/exam_engine.py
- app/llm_adapter.py
- streamlit_app.py

Görev:
C1) compute_mastery_scores ekle.
C2) build_student_skill_summary → request_adaptive_plan_from_llm → create_adaptive_exam yaz.
C3) detect_negative_trend + create_moral_booster_exam yaz.
C4) UI:
   - “Adaptif Deneme Oluştur”
   - “Moral Denemesi Oluştur” banner

Kabul Kriterleri:
- Adaptif deneme 1 dakika altında oluşturuluyor.
- En az 3 konu + 2 zorluk seviyesi dağılımı sağlanıyor.
```

---

### FAZ D — Eğitim Katmanı (V4 Planının Resmi Devreye Girişi)
**Amaç:**  
Soru-temelli sistemin yanına **müfredat/konsept/örnek-temelli** öğrenme katmanı eklemek.

**Bağımlılık:** Faz B-C  
> Çünkü eğitim içerikleri, **hangi konunun zayıf olduğuna dair** güvenilir tanı olmadan kişiselleşemez.

**Teslimatlar:**
- ContentItems + CurriculumMap sheets
- PDF içe aktarım v1  
  - OCR → bölümleme → kısa özet → konsept fişi
- “Öğren” sekmesi
  - yanlış sorudan içerik önerisi
  - mini ders listesi

**DoD:**
- Tek bir çözümlü PDF’den 10+ ContentItem çıkarılabiliyor.
- İçerikler topic/subtopic ile etiketleniyor.
- Öğrenci yanlış yaptığı konudan 1 tıkla ilgili konsept kartına geçebiliyor.

**AI IDE Komut Paketi:**
```text
MASTER SÖZLEŞME — FAZ D

SERT KURALLAR:
1) Tam metin depolama yerine:
   - kısa özet
   - adım adım öğretim fişi
   - kişiselleştirilmiş açıklama
2) ContentItems mutlaka topic/subtopic ile bağlanacak.
3) PDF pipeline v1 “yarı-otomatik” kabul edilir; manuel doğrulama adımı yazılacak.

Dosyalar:
- app/content_engine.py
- app/teaching_engine.py
- app/analysis_engine.py
- app/data_access.py
- streamlit_app.py

Görev:
D1) ContentItems ve CurriculumMap için okuma/yazma fonksiyonlarını ekle.
D2) content_engine:
   - ingest_pdf_metadata()
   - extract_candidate_sections()
   - summarize_to_concept_cards()
   - save_content_items()
D3) UI:
   - “Öğren” sekmesi
   - konu bazlı içerik listesi
   - yanlış sorudan “İlgili Konsept Kartı” önerisi

Kabul Kriterleri:
- En az 1 PDF için uçtan uca içerik üretimi demo ediliyor.
- İçerikler öğrenciye 3 dakikalık mikro ders akışı şeklinde sunuluyor.
```

---

### FAZ E — Ürün Kalitesi, Güvenlik, Gözlemlenebilirlik
**Amaç:**  
Pilot projeyi “tek kişilik hobi”den çıkarıp  
**bakımı yapılabilir bir ürün** haline getirmek.

**Bağımlılık:** Faz A-D

**Teslimatlar:**
- Feature flags
- Event log (analytics-lite)
- Prompt sürümleme
- Hata raporlama
- Test coverage min %30

**DoD:**
- `feature_flags.yaml` ile major özellikler aç/kapa çalışıyor.
- En az 10 kritik event loglanıyor:
  - exam_created
  - answer_submitted
  - teaching_opened
  - block_completed …
- Prompt şablonları tek dosyada versionlı tutuluyor.

---

### FAZ F — Veri Taşıma ve Çoklu Öğrenci
**Amaç:**  
Sheets → Supabase/Postgres  
Tek öğrenci → çoklu öğrenci

**Bağımlılık:** Faz E

**Teslimatlar:**
- DB şeması
- Migration script
- Basit auth (email + magic link veya admin listesi)
- Çoklu öğrenci seçimi

**DoD:**
- Aynı fonksiyon imzalarıyla
  `data_access` sadece backend değiştirerek çalışabiliyor.
- En az 3 öğrenci ile izole veri testleri geçiyor.

---

### FAZ G — “Enterprise-Grade” Analitik ve Ebeveyn Kokpiti
**Amaç:**  
Ebeveyn/koç görünürlüğü + KPI’lar

**Bağımlılık:** Faz F

**Teslimatlar:**
- Haftalık rapor ekranı
- Mastery heatmap
- Net trendleri ve normalize başarı metrikleri

---

## 8) Kalite Kapıları (Quality Gates)

### 8.1 Kod Kalitesi
- PEP8
- type hints
- modül sınırları net

### 8.2 Veri Kalitesi
- Boş topic/subtopic kabul edilmez
- difficulty_label 1-5 dışı değer reddedilir
- question_origin zorunlu

### 8.3 Pedagojik Kalite
- Her yeni feature, şu üç soruya cevap vermeli:
  1) Öğrenciye **hemen** ne kazandırıyor?
  2) Motivasyon sürtünmesini azaltıyor mu?
  3) Öğrenme transferini artırıyor mu?

---

## 9) Pilot Operasyon Planı (4 Haftalık Sprint)

### Hafta 1 — Stabilizasyon + Basit Rutin
- Faz A tamamlayıcı işler
- 2–3 günlük blok şablonu
- 10 soruluk fixed mini denemeler

### Hafta 2 — Bugün ekranı + Küçük Zafer
- Faz B odak
- Streak v1
- Gün sonu özet

### Hafta 3 — Adaptif Deneme + Moral Booster
- Faz C odak
- Mastery skorları

### Hafta 4 — Eğitim Katmanı denemesi (V4’ün Minimum Dilimi)
- Faz D’nin “mini pilot” hali:
  - 1 PDF
  - 1 konu
  - 10 içerik kartı

---

## 10) Risk Kayıtları ve Önlemler

### 10.1 Teknik Riskler
- Sheets performans sınırı
  - Önlem: cache + batch yazma
- LLM JSON sapmaları
  - Önlem: strict schema validation
- OCR hataları
  - Önlem: “insan onay ekranı”

### 10.2 Davranışsal Riskler
- Pilot öğrencinin motivasyon kırılması
  - Önlem: warmup + moral booster + küçük zafer

### 10.3 Ürün Riskleri
- Çok fazla feature ile karmaşa
  - Önlem: Feature flags + “3 kart kuralı”

---

## 11) AI IDE İçin Global Master Kurallar (Bu bloğu her görevde başa yapıştır)

```text
LGS NEURAL-KOÇ MASTER KURALLAR (GLOBAL)

1) Bu proje bir pilot öğrenciyi 4–12 hafta içinde ölçülebilir şekilde ileri taşıma hedefiyle yazılıyor.
2) Öncelik sırası:
   a) Veri doğru kaydedilsin
   b) Analiz doğru çalışsın
   c) Öğrenci günlük rutinde tutulsun
   d) Adaptif seçim devreye girsin
   e) Eğitim katmanı kişiselleşsin

3) “Soru-temelli” motor bitmeden “tam otomatik içerik üretimi”ne geçme.
4) LLM:
   - önce planlayıcı
   - sonra açıklayıcı
   - en son üretici
5) LLM çağrıları tek kapı: llm_adapter.
6) Sheets erişimi tek kapı: data_access.
7) Yeni tablo/kolon ekliyorsan:
   - migration notu yaz
   - örnek satır ekle
8) Her faz için DoD sağlanmadan bir sonraki faza geçme.
9) Kod:
   - type hints
   - docstring
   - hata mesajları kullanıcı dostu
10) UI:
   - aynı ekranda en fazla 3 ana odak
   - metinler koç tonu
```

---

## 12) Ek Özellik Havuzu (Sadece Faz E sonrası seçilerek)
- Dijital Hata Defteri 2.0
- Otomatik tekrar aralıkları (1-3-7)
- Basit ebeveyn rapor e-postası
- Zorluk normalize başarı puanı

---

## 13) Kapanış

Bu master doküman,
pilot seviyede hızlı sonuç üretirken
**enterprise düzeyi sürdürülebilirliğe** açık bir tasarım sunar.

Önerilen uygulama disiplini:
- Her hafta sonunda:
  - KPI kontrolü
  - hangi feature öğrenciyi gerçekten tutuyor analizi
  - gereksiz olanı kapatma (feature flag)

Bu sayede proje,
“çok özellikli ama dağınık” değil,
“az ama etkili, büyümeye hazır” bir platforma evrilir.


---

## Bölüm II — Faz Eşleştirme Haritası (v2 Netleştirme)

Bu tablo, önceki dokümanların hangi fazda devreye gireceğini bağlayıcı şekilde tanımlar.

### 1) Soru Motoru Yol Haritası (orijinal doküman)
- **Faz A-B-C** içerisine dağılmış şekilde uygulanır.
- “Adaptif seçim + mastery + moral booster” parçaları **Faz C** ile kilitlenir.

### 2) Ek Fikirler Dokümanı
- Çoğu özellik **Faz E sonrası** açılabilir.
- Pilot motivasyonuna doğrudan hizmet eden 3 madde **erken istisna** alır:
  - **Warmup Mode** → Faz B  
  - **Gün Sonu Küçük Zafer** → Faz B  
  - **Moral Booster** → Faz C

### 3) Eğitim Katmanı v4 Planı
- **Resmi devreye giriş fazı: Faz D**
- Faz D öncesi yalnızca “mini dilim” pilot yapılabilir:
  - 1 subtopic
  - 10-20 manuel içerik fişi
  - Öğren sekmesi MVP akışı

> Bu eşleştirme kuralları, AI IDE’ye verilecek görevlerde “faz kapısı” kontrolü olarak kullanılacaktır.

---

## Bölüm III — Orijinal Ana Yol Haritası (TAM METİN EK)
Bu bölüm, önceki **lgs_neural_koc_yol_haritasi.md** dokümanının **değiştirilmemiş** tam metnidir.
Bu metin, v2 master sözleşmenin “detay ekleri” niteliğindedir.

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

## Bölüm IV — Ek Fikirler ve Geliştirme Notları (TAM METİN EK)
Bu bölüm, önceki **lgs_neural_koc_ek_fikirler_ve_gelistirme.md** dokümanının **değiştirilmemiş** tam metnidir.

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

## Bölüm V — Eğitim Katmanı + PDF İçe Aktarım v4 (TAM METİN EK)
Bu bölüm, önceki **lgs_neural_koc_egitim_katmani_ana_plan_v4_detayli.md** dokümanının **değiştirilmemiş** tam metnidir.

---
# LGS Neural-Koç – Eğitim Katmanı + PDF İçe Aktarım  
## Aşırı Detaylı Uygulama Planı (v4)  
### “AI IDE atlamasın” sürümü

Bu doküman, önceki **“Basitleştirilmiş, Kademeli ve Pilot Odaklı Ana Plan (v3)”** belgesinin **çok daha detaylı** ve **neden/niçin gerekçeleriyle** genişletilmiş halidir.  
Amaç, Cursor/Windsurf gibi AI destekli IDE’lerde bu planın **yorumlanmadan, atlama yapılmadan** uygulanabilmesini sağlamaktır.

Bu nedenle dokümanda:
- Sert kurallar,
- Kabul kriterleri (Definition of Done),
- Dosya/fonksiyon seviyesinde görevler,
- Veri şemaları,
- Edge-case kontrolleri,
- “Pilot gerçekliği”ne uygun iş parçalama

özellikle ayrıntılandı.

---

## 0) Kapsam ve Felsefe

### 0.1 Neden Eğitim Katmanı?
Soru motoru tek başına şunları yapabilir:
- zayıf konuyu bulur,
- adaptif deneme seçer,
- yanlış üzerinden koçluk verir.

Ama **müfredat/öğrenme omurgası** olmadan:
- öğrenci hatayı “düzeltir” ama **konuyu yapılandırılmış şekilde öğrenmez**,
- sistem “analiz aracı” gibi kalır,
- pilot öğrenci gibi zor profilde sürdürülebilir motivasyon zorlaşır.

**Eğitim katmanı**, sistemi “analiz + öğretim + tekrar + ölçüm” döngüsüne taşır.

### 0.2 Neden “tam metin değil fiş” yaklaşımı?
Çözümlü PDF’leri birebir taşımak:
- ürünü ağırlaştırır,
- veri yönetimini zorlaştırır,
- pedagojik olarak öğrenciyi metin boğulmasına sürükler.

**Fiş (learning fiche)** yaklaşımı:
- 5–8 maddede özü verir,
- tipik hata ve çözüm stratejisini netleştirir,
- öğrenci için “kısa ve uygulanabilir” bir öğrenme objesi üretir.

### 0.3 Neden 4 Seviye PDF Planı?
PDF işleme otomasyonu **yüksek belirsizlik** içerir:
- PDF’lerin yapısı standardize değildir,
- bazısı görüntü bazlıdır (OCR gerekir),
- sayfa içeriği karışıktır (anlatım + örnek + test).

Bu yüzden:
- ürünü önce “fiş veri modeli + öğrenme UI” ile canlı yapıp,
- otomasyonu sonra **verim artırıcı** olarak eklemek
pilot riski düşürür.

---

## 1) Nihai Hedef Mimari (Pilot Perspektifi)

### 1.1 İki Motor
1) **Soru Motoru**  
2) **Eğitim/İçerik Motoru**

### 1.2 Tek Harita
**Curriculum_Map**, iki motorun ortak koordinat sistemi olacak.

> Kural:  
> Her soru ve her içerik parçası mutlaka `lesson + topic + subtopic` ile etiketlenecek.  
> Etiket yoksa sistemde “aktif içerik” olarak kullanılmayacak.

Bu kural, adaptif önerilerin tutarlılığını korur ve ileride Supabase’e geçişi çok kolaylaştırır.

---

## 2) Google Sheets Veri Modeli (DB-ready tasarım)

Aşağıdaki tablo adları Google Sheets içinde ayrı sayfalar (tabs) olacak şekilde planlanmalıdır.  
İleride Supabase’e geçişte aynı isimler snake_case ile tabloya çevrilebilir.

### 2.1 Mevcut Tablolar
- `Students`
- `Questions`
- `Exams`
- `Answers`
- `Schedule`

### 2.2 Yeni Tablolar (Bu planın konusu)
- `Content`
- `Curriculum_Map`
- (opsiyonel) `Learning_Events`

---

## 3) Content Sheet (İçerik Havuzu) – Detay Şema

**Amaç:** Çözümlü kitapçıklardan veya AI üretiminden gelen eğitim içeriklerini standartlaştırmak.

### 3.1 Minimum Kolonlar ve Tanımlar

| Kolon | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| content_id | string | ✅ | Benzersiz ID (örn: CNT-MAT-0001) |
| source_type | enum | ✅ | `publisher`, `ai_generated`, `coach_created` |
| publisher | string | 🔶 | source_type=publisher ise zorunlu |
| lesson | string | ✅ | Matematik/Türkçe/Fen/... |
| topic | string | ✅ | Ünite/tema |
| subtopic | string | ✅ | Mikro kazanım |
| content_type | enum | ✅ | `micro_lesson`, `worked_example`, `concept_card`, `misconception_fix` |
| difficulty_band | enum | ✅ | `easy`, `medium`, `hard` |
| estimated_time_min | int | ✅ | 3–10 arası önerilir |
| summary_bullets | string | ✅ | `;` ile ayrılmış 5–8 madde |
| strategy_steps | string | ✅ | `;` ile ayrılmış 3–6 adım |
| common_mistakes | string | ✅ | `;` ile ayrılmış 2–5 hata |
| mini_check_stem | string | ✅ | 1 mini kontrol sorusu kökü |
| mini_check_options_json | string | ✅ | {"A":"", "B":"",...} |
| mini_check_correct_option | string | ✅ | A/B/C/D |
| page_ref | string | 🔶 | PDF sayfa referansı (örn: “YayınX s.34”) |
| active | bool | ✅ | Varsayılan True |

**Kural:**  
Pilot için `summary_bullets/strategy_steps/common_mistakes` alanları boş bırakılamaz.  
Boş içerik fişi, UI’de gösterilmez.

### 3.2 Neden bu alanlar?
- **summary_bullets**: öğrenciye “konu özeti” verir.  
- **strategy_steps**: “nasıl çözmeliyim?” davranışını öğretir.  
- **common_mistakes**: yanlış kalıp düzeltme için kritiktir.  
- **mini_check**: öğrenmenin anında ölçümünü sağlar.

Bu dörtlü, eğitim katmanını “metin deposu” olmaktan çıkarıp **öğrenme objesi** yapar.

---

## 4) Curriculum_Map Sheet – Detay Şema

**Amaç:** Sistem için “tek kaynak gerçek” müfredat koordinatları.

| Kolon | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| lesson | string | ✅ | |
| topic | string | ✅ | |
| subtopic | string | ✅ | |
| learning_objective | string | ✅ | Tek cümle hedef |
| prerequisites | string | 🔶 | `;` ile ayrılmış subtopic listesi |
| default_content_mix | string | ✅ | Örn: `1 micro_lesson + 1 worked_example` |
| default_question_mix | string | ✅ | Örn: `3 easy + 4 medium + 3 hard` |
| notes | string | 🔶 | Koç notları |

**Kural:**  
`Curriculum_Map`’te olmayan `(lesson, topic, subtopic)` kombinasyonu:
- soru seçiminde,
- içerik önerisinde
**aktif olarak kullanılmayacak.**

Bu, etiket karmaşasını engeller.

---

## 5) Öğrenme Döngüsü (Ürün Mantığı)

Eğitim katmanının temel akışı:

1) **Zayıf alt konuyu tespit et** (Answers → topic/subtopic).  
2) **Önce içerik öner** (Content).  
3) **Hemen mini kontrol çalıştır** (mini_check).  
4) **Ardından 5–10 soruluk uygulama seti** (Questions).  
5) **Sonuçları kaydet** (Answers + Learning_Events).  
6) **3 gün sonra kısa tekrar öner** (Unutma eğrisi).

Bu döngü ile sistem “koç + öğretmen + ölçme motoru” birlikte çalışır.

---

## 6) Streamlit UI – Zorunlu Ekranlar

### 6.1 “Öğren” Sekmesi (MVP)
MVP ekranı şu bileşenleri içermeli:

- Topic/Subtopic seçimi  
- Kaynak filtresi:
  - `publisher`
  - `ai_generated`
  - `hybrid`
- İçerik kartı:
  - summary bullet list
  - strategy steps
  - common mistakes
- “Mini Kontrol Sorusu” bloğu
- “Hemen Uygula” butonu (5 soruluk mini set)

**Kural:**  
Bu sayfa, PDF otomasyonu olmadan da **tam çalışır** olmalı.  
İlk veriler manuel girilmiş varsayılacak.

### 6.2 Analiz Sekmesi – İçerik Etkisi
Pilot için minimum metrik:

- “Öğrenme öncesi mini check doğruluk”  
- “Öğrenme sonrası mini check doğruluk”  
- Delta (%)  

Basit bir tablo yeterli.

---

## 7) Python Modülleri – Detay Görev Listesi

Yeni modüller:

```text
app/
  curriculum_engine.py
  content_engine.py
  content_ingest_engine.py   # Seviye 2-3
  learning_metrics.py        # opsiyonel ama önerilir
```

### 7.1 curriculum_engine.py
Zorunlu fonksiyonlar:

- `load_curriculum_map()`  
- `validate_tags(lesson, topic, subtopic) -> bool`  
- `get_default_content_mix(...)`  
- `get_default_question_mix(...)`  

**Kabul kriteri:**  
Her içerik/soru önerisi çağrısı önce `validate_tags` ile doğrulanmalı.

### 7.2 content_engine.py
Zorunlu fonksiyonlar:

- `load_content_df()` (data_access üzerinden)  
- `filter_content(student_id, lesson, topic, subtopic, source_filter)`  
- `select_best_content(...)`  
  - Basit kural: önce `micro_lesson`, sonra `worked_example`  
- `build_learning_packet(...) -> dict`  
  - `{content_items: [...], mini_check: {...}, practice_question_ids: [...]}`

**Kabul kriteri:**  
build_learning_packet çıktısı JSON-serializable olmalı ve UI’de direkt kullanılmalı.

### 7.3 content_ingest_engine.py (Seviye 2)
Zorunlu fonksiyonlar:

- `extract_pdf_text_by_page(pdf_path) -> dict[int, str]`
- `select_candidate_pages(text_by_page) -> list[int]`
  - Heuristic: “Örnek”, “Çözüm”, “Soru çözümü” keyword’leri  
- `request_content_fiche_from_llm(page_text, meta) -> dict`
- `append_content_fiche_to_sheet(fiche_dict)`

**Kabul kriteri:**  
Bu modül, seçilen 5 sayfa üzerinde demo çalıştırıldığında Content sheet’e **en az 5 geçerli satır** eklemeli.

### 7.4 content_ingest_engine.py (Seviye 3)
Ek fonksiyonlar:

- `group_fiches_by_subtopic(fiches)`  
- `merge_fiches_into_micro_lesson(fiche_group) -> dict`

**Kabul kriteri:**  
Bir subtopic için 3 fiche varsa micro_lesson türetilip Content’e yazılmalı.

---

## 8) PDF Otomasyonu – “Atlamasız” Seviye Planı

### Seviye 0 (Zorunlu)
**Kritik neden:** Eğitim motoru UI ve metrikleri önce doğrulanmalı.

**Görevler:**
- Content sheet’i aç  
- 10–20 manuel fiş gir  
- Öğren sekmesini çalıştır

**Done:**
- Öğren sekmesinde en az 2 subtopic için içerik gösteriliyor  
- Mini check çalışıyor  
- 5 soruluk uygulama seti açılabiliyor

### Seviye 1 (Zorunlu)
**Kritik neden:** PDF’de otomasyona girmeden iş akışının hızlanması.

**Görevler:**
- PDF’den sayfa_ref listesi çıkar  
- Fişleri “sayfa referanslı” yap

**Done:**
- Content fişlerinin %80’inde page_ref dolu

### Seviye 2 (Opsiyonel ama güçlü öneri)
**Kritik neden:** Manuel iş yükünü ciddi azaltır.

**Görevler:**
- PyMuPDF ile metin çıkar  
- Heuristic sayfa seç  
- Gemini’den JSON fiş al  
- Content sheet’e yaz

**Done:**
- Tek PDF’den en az 30 otomatik fiş üretilebiliyor

### Seviye 3 (Opsiyonel)
**Kritik neden:** “müfredat hissi”ni güçlendirir.

**Done:**
- 3–5 fişten 1 micro_lesson derlenip kaydediliyor

---

## 9) Pilot A/B Tasarımı – İçerik ve Soru Aynı Mantıkta

### 9.1 Soru A/B
- publisher_only  
- ai_only  
- hybrid (ai_ratio=0.1–0.2)

### 9.2 İçerik A/B
- publisher_content_only  
- ai_content_only  
- hybrid_content

**Kural:**  
Her deneme/öğrenme paketi meta_json içinde kaynak modunu taşımalı.

Örn:
```json
{
  "question_source_mode": "hybrid",
  "ai_ratio": 0.2,
  "content_source_mode": "publisher_content_only"
}
```

**Done:**
- Analiz ekranında topic bazlı “kaynak karşılaştırma” tablosu görülebiliyor

---

## 10) Google Sheets → Supabase Geçiş Notu

Evet, şema örneklerini .xlsx gibi yazmamız sadece “tablo tasarımı” içindi.  
Senin planın doğru:

- xlsx şemasını Google Sheets’e kopyala  
- Python’da Sheets API ile bağlan  
- Supabase’e geçerken CSV export/import yap

**Kural:**  
Kolon adlarını şimdiden stabil tut.  
Bu, migrasyonda en büyük zaman kazancı.

---

## 11) AI IDE İçin “Sözleşme Promptu” (Kopyala/Yapıştır)

Aşağıdaki prompt’u her eğitim katmanı görevinde başa koy:

```text
SERT KURAL SETİ (ATLANMAYACAK):

1. Bu görevde "yorum yapma", "öneri bırakma" veya "sonra yapılabilir" deme.
   Her maddeyi SOMUT kod veya SOMUT yapılandırma ile uygula.

2. Aşağıdaki dosya ve fonksiyon isimleri aynen kullanılacak:
   - app/curriculum_engine.py
   - app/content_engine.py
   - app/content_ingest_engine.py
   - app/data_access.py
   - streamlit_app.py

3. Google Sheets şemaları bu kolonları zorunlu kabul edilecek:
   Content:
     content_id, source_type, publisher, lesson, topic, subtopic,
     content_type, difficulty_band, estimated_time_min,
     summary_bullets, strategy_steps, common_mistakes,
     mini_check_stem, mini_check_options_json, mini_check_correct_option,
     page_ref, active

   Curriculum_Map:
     lesson, topic, subtopic, learning_objective,
     default_content_mix, default_question_mix

4. validate_tags kullanılmadan hiçbir içerik/soru önerisi yapılmayacak.

5. İlk sürümde PDF otomasyonu YOK.
   içerik verileri MANUEL GİRİLMİŞ varsayılacak.
   Bu kural Seviye 0-1 tamamlanmadan değiştirilmeyecek.

6. Her modül için docstring ve hata kontrolü yazılacak.
```

---

## 12) Pilot İçin Net Haftalık Plan (Küçük risk, büyük öğrenme)

### Hafta 1 – Eğitim Motoru Canlandırma
- Content + Curriculum_Map oluştur  
- 10–20 manuel fiş  
- Öğren sekmesi  
- Mini check + 5 soru uygulama

### Hafta 2 – İçerik A/B
- Aynı subtopic için:
  - 1 publisher fişi  
  - 1 AI fişi  
- Öğrenme öncesi/sonrası delta tablosu

### Hafta 3 – Seviye 1
- page_ref listeleri  
- fişlerin sayfa referanslarını doldurma

### Hafta 4 – Seviye 2 (isteğe bağlı)
- 1 PDF üzerinden yarı otomatik fiş üretimi

---

## 13) Bu Planın “AI atlamasını” nasıl önlediği?

- Her bölümde **Zorunlu–Opsiyonel** ayrımı var.  
- Her seviyenin **Done kriteri yazıldı**.  
- Fonksiyon isimleri ve kolon isimleri “sözleşme” gibi sabitlendi.  
- Seviye 0–1 tamamlanmadan Seviye 2’ye geçiş “kural” olarak işaretlendi.

Bu, IDE AI’nin “kendi bildiği gibi optimize edip” kritik basamakları atlamasını ciddi ölçüde engeller.

---

## 14) Kapanış

Bu v4 planı ile:

- Eğitim katmanı, soru motoruna eşdeğer bir ikinci omurga olur.  
- PDF otomasyonu korkutucu bir “tek büyük proje” değil,  
  ürün çalışırken devreye giren “verim katmanları”na dönüşür.  
- Pilot öğrencide hem motivasyon hem ölçümlenebilir öğrenme etkisi sağlanır.  
- Supabase geçişi için şema bugün doğru kurulur.

Bu doküman, doğrudan AI IDE’ye verilerek modül modül uygulanacak şekilde yazılmıştır.

---

## Bölüm VI — Çakışma ve Öncelik Kuralları

Bu v2 master dokümanda aynı konu farklı bölümlerde farklı şekilde tanımlanıyorsa:

1. **Bölüm I (Enterprise Master v1 çekirdek plan)** önceliklidir.  
2. **Bölüm II (Faz Eşleştirme Haritası)** zamanlama konusunda bağlayıcıdır.  
3. Bölüm III-IV-V, detay/örnek/alternatif uygulama rehberi olarak kullanılır.

---

## Bölüm VII — “AI IDE Atlamasın” Kısa Kontrol Listesi

Her PR/commit sonrası şu 10 madde doğrulanır:

1. LLM çağrıları yalnız adapter üzerinden mi?  
2. Sheets erişimi yalnız data_access üzerinden mi?  
3. Yeni kolon eklendiyse migration notu var mı?  
4. `question_origin` boş kalan soru var mı?  
5. `source_type` boş kalan içerik var mı?  
6. `topic/subtopic` etiketsiz kayıt var mı?  
7. UI 3 kart kuralı bozuldu mu?  
8. Feature flags güncellendi mi?  
9. DoD koşulları commit mesajında referanslandı mı?  
10. Pilot öğrenci için “başlama sürtünmesi” artıyor mu?

---

## Bölüm VIII — Supabase’e Geçiş İçin Net Hazırlık

Sheets’te bugün yapılacak 3 kritik hazırlık:

- Tüm sheet adlarını DB’ye uygun isimlerle sabitle:  
  `students, questions, exams, exam_questions, answers, schedule, content_items, curriculum_map, student_content_progress`
- ID formatlarını standardize et.  
- `created_at`/`updated_at` alanlarını şimdiden ekle.

> Bu düzenleme, Faz F’de migrasyonu dramatik şekilde kolaylaştırır.

---

## Kapanış

Bu v2 master sözleşme, artık:
- “tek dosyada tüm detaylar” isteğini karşılayacak şekilde,
- önceki dokümanların **tam metinlerini** içerir,
- üzerine enterprise faz-kapıları ve DoD katmanı ekler.

Bu dosyayı tek başına kullandığında dahi,
projenin teknik, pedagojik ve operasyonel bütün resmini kaybetmeden ilerleyebilirsin.
