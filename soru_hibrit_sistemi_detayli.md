# LGS Neural-Koç — **Soru Hibrit Sistemi** (Ayrı ve Detaylı Sözleşme)
## Pilot odaklı, yayın evi + MEB + AI karma soru stratejisi
### Kullanım amacı: Adaptif deneme, hedefli mini setler, kalite kontrollü AI üretimi

Bu doküman, LGS Neural-Koç projesinde **soru havuzu ve deneme üretimi** için hibrit yaklaşımı
net kurallara bağlar.  
Önceki master planlarda geçen **question_origin** fikrini burada “tam işletim modeli”ne çeviriyoruz.

> Bu doküman, **pilot** için hızlı değer üretirken ileride ürünleşmede kontrol ve ölçeklenebilirlik sağlar.

---

## 1) Hibrit yaklaşımın hedefi

Tek kaynağa bağlı kalmadan:

- **Yayın evi soruları** (farklı zorluk profilleri)  
- **MEB/Açık kaynak tarzı sorular**  
- **AI özgün sorular**  
- **AI havuz varyantları**

ile **tek bir standart veri düzeni** üzerinden:

1) hedefli mini deneme  
2) adaptif plan  
3) öğrenciye özel tekrar seti  
4) moral booster

üretebilmek.

---

## 2) Zorunlu etiket standardı (Question Metadata Contract)

### 2.1 `Questions` tablosu minimum kolonlar

- `question_id`
- `question_text`
- `options_json`
- `correct_option`
- `lesson`
- `topic`
- `subtopic`
- `difficulty_label` *(1-5)*
- `question_type` *(mcq, multi_step, reasoning, graph, table vb.)*
- `question_origin` *(zorunlu)*
- `origin_detail` *(yayın evi adı / “meb” / “ai”)*
- `derivation_ref` *(opsiyonel: varyantın hangi soru_id’den türediği)*
- `quality_state` *(draft, active, retired)*
- `active`
- `created_at`
- `updated_at`

### 2.2 `question_origin` sözlüğü

Bu alan **boş bırakılamaz**:

- `publisher`
- `meb`
- `ai_original`
- `ai_variant_of_pool`

> Pilot aşamasında bile bu etiket zorunlu tutulursa, ileride analitik ve harmanlama çok kolaylaşır.

---

## 3) Hibrit soruların 4 çalışma modu

### Mod A — **Saf Havuz Seçimi** (En güvenli ve hızlı)
Sistem yeni soru üretmez.

- `publisher` + `meb` sorularından
- zorluk ve konu dağılımına göre
- Python kural motoru ile seçim yapar.

**Ne zaman?**  
Pilotun ilk haftaları.

### Mod B — **AI Özgün Soru** (Kalite kontrollü)
AI, **kazanım tabanlı** yeni soru üretir.

**Kural:**
- Örnek sorular “stil ve seviye referansı” olarak verilir.
- Çıktı mutlaka `ai_original` olarak etiketlenir.
- İnsan/AI kalite filtresi olmadan `active` olmaz.

**Ne zaman?**  
Havuzda konu boşluğu varsa.

### Mod C — **AI Havuz Varyantı** (Senin özellikle istediğin hibrit)
AI, mevcut havuzdan seçilen soruların **varyantını** üretir.

**Önerilen kullanım:**
- Varyant oranı pilotta düşük tutulur.
- Varyantlar, orijinal sorunun yerini almaz; “pekiştirme” amaçlı kullanılır.

**Zorunlu etiketler:**
- `question_origin = ai_variant_of_pool`
- `derivation_ref = <orijinal question_id>`

**Ne zaman?**  
Yanlış tekrarında çok etkili.

### Mod D — **Karma Deneme**
Tek bir denemede:
- %50-70 `publisher/meb`
- %10-30 `ai_variant_of_pool`
- %0-10 `ai_original`

oranına göre harman.

Bu oranlar `config/question_mix.yaml` ile kontrol edilir.

---

## 4) Zorluk modelini hibritte nasıl oturtacağız?

### 4.1 “Yayın evi = zorluk profili” yaklaşımı
Farklı yayınevleri zaten farklı zorluk bandı sunar.

Bu yüzden iki katmanlı etiket önerilir:

1) **soru bazlı:** `difficulty_label`  
2) **kaynak bazlı:** `publisher_difficulty_profile` *(config’te tutulur)*

Örn:
- yayınevi_A: orta-üst
- yayınevi_B: kolay-orta
- yayınevi_C: zor

Bu ikisi çakışırsa **soru bazlı etiket önceliklidir**.

### 4.2 İlk pilot için pratik kural
İstatistiksel IRT’ye girmeden:

- `difficulty_label` öğretmen/manuel
- sonra öğrenci çözüm oranına göre güncelleme

yeterli.

---

## 5) Hibrit deneme üretim algoritması (Basit ama sağlam)

### Girişler
- `student_id`
- hedef ders(ler)
- zayıf `topic/subtopic` listesi
- `question_mix` oranları
- `difficulty_mix` oranları

### Adımlar
1) **Python** öğrenci mastery özetini çıkarır.  
2) **LLM (Gemini)** yalnızca **plan JSON** üretir.  
3) **Python** planı doğrular.  
4) **Python** havuzdan soru seçer.  
5) Oran hedefi varsa:
   - önce `publisher/meb`
   - sonra `ai_variant_of_pool`
   - en son `ai_original`

### Çıkışlar
- `Exams`
- `ExamQuestions`
- plan metadata

---

## 6) Kalite güvence (Pilot bile olsa şart)

### 6.1 AI soru kalite filtresi
`ai_original` ve `ai_variant_of_pool` için:

- seçenek sayısı 4 mü?
- tek doğru cevap kontrolü
- çözüme giden adım tutarlılığı
- konu etiketi uyumu

**Fail olursa:** `quality_state = draft`

### 6.2 Benzerlik riski için pratik önlem
Pilot özelinde bile:

- varyant üretiminde
  - sayı/veri/bağlam değişimi
  - soru kökü yeniden yazım

kuralını uygula.

---

## 7) Google Sheets ile yönetim (Faz F ertelenmişken)

### 7.1 Önerilen sheet düzeni
- `Questions`
- `Exams`
- `ExamQuestions`
- `Answers`
- `QuestionMixConfig` *(opsiyonel küçük config sheet)*

### 7.2 Config dosyası (kod tarafı)
`config/question_mix.yaml`

```yaml
default_mix:
  publisher: 0.60
  meb: 0.20
  ai_variant_of_pool: 0.15
  ai_original: 0.05

by_mode:
  adaptive:
    publisher: 0.55
    meb: 0.25
    ai_variant_of_pool: 0.15
    ai_original: 0.05
  revision:
    publisher: 0.40
    meb: 0.20
    ai_variant_of_pool: 0.35
    ai_original: 0.05
  moral:
    publisher: 0.70
    meb: 0.20
    ai_variant_of_pool: 0.10
    ai_original: 0.00
```

---

## 8) Pilot işletim protokolü

### 8.1 İlk 2 hafta
- Mod A + az Mod C
- `ai_original` kapalı olabilir.

### 8.2 3-4. hafta
- yanlış tekrarlarında Mod C oranını artır.

### 8.3 Ölçüm
- AI varyant sorularında doğruluk artışı  
- tekrar çözüm süresi düşüşü  
- motivasyon geri bildirimi

---

## 9) IDE’ye tek parça komut (Soru hibrit sistemi)

```text
HEDEF:
LGS Neural-Koç için "Soru Hibrit Sistemi"ni uygulanabilir hale getir.
Yayın evi + MEB + AI özgün + AI havuz varyantlarını tek etiket standardında yönet ve deneme üretiminde harmanla.

SERT KURALLAR:
1) Questions sheet’te question_origin zorunlu.
2) ai_variant_of_pool için derivation_ref zorunlu.
3) LLM sadece PLAN üretir, final soru seçimi Python ile.
4) AI sorular default draft; kalite kontrol geçmeden active olmaz.
5) Oranlar config/question_mix.yaml ile kontrol edilecek.

DOSYALAR:
- app/data_access.py
- app/analysis_engine.py
- app/exam_engine.py
- app/llm_adapter.py
- config/question_mix.yaml
- tests/test_hybrid_questions.py

GÖREVLER:
1) Questions kolon şemasını doğrula/eksikleri ekle (question_origin, derivation_ref, quality_state).
2) config/question_mix.yaml oluştur ve default oranları ekle.
3) exam_engine içinde:
   - select_questions_by_mix(plan, mix_config)
   - validate_ai_question_quality(question_row)
   fonksiyonlarını yaz.
4) LLM plan JSON’una "origin_mix_hint" alanını ekle.
5) revision ve moral modlarında mix overrides’ı uygula.
6) 3 pytest yaz:
   - mix oranına uyum
   - derivation_ref validasyonu
   - AI kalite filtresi

KABUL KRİTERLERİ:
- Aynı subtopic için karma kaynaklı 15 soru deneme üretilebiliyor.
- ai_variant_of_pool soruları derivation_ref olmadan seçilmiyor.
- Konfigürasyon değişince oranlar gerçek seçimde değişiyor.
```

---

## 10) Kısa not (telif/ürünleşme için)
Pilot kişisel kullanımda düşük risk olsa da,  
bu hibrit yapıyı ürünleştirirken ve üçüncü kişilere açarken
yayın evi içerikleri için izin/lisans konusunu ayrıca ele almanız gerekebilir.

---

## Sonuç
Bu hibrit sistem:
- “farklı yayınevleri zaten farklı zorluk profili” yaklaşımını bozmadan,
- AI’yı **doğru yerde** (planlayıcı + varyant + boşluk doldurucu) konumlandırır,
- pilotta hızlı değer üretirken gelecekteki ölçeklemeyi temiz tutar.
