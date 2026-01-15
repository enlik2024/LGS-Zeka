
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
