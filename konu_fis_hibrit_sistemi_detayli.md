# LGS Neural-Koç — **Konu Fiş Hibrit Sistemi** (Ayrı ve Detaylı Sözleşme)
## Yayın evi çözümlü kitapçıklar + AI fiş + PDF’den hızlı üretim
### Kullanım amacı: “Yanlıştan öğrenmeye tek tık”, mikro ders ve mini-check

Bu doküman, öğretici içerik tarafında **hibrit fiş stratejisini**
tam işletim modeline çevirir.

Amaç:
- yayın evi anlatım/çözüm kaynaklarını **fiş formatına** indirgemek,
- AI’nın bunu hızlı taslaklaştırmasını sağlamak,
- içerikleri **kaynak ve türetim etiketleriyle** yönetmek,
- öğrencide **yanlış → konu fişi → mini-check → 5 soru** döngüsünü kurmak.

---

## 1) Hibrit yaklaşımın hedefi

Tek bir kaynağa bağlı kalmadan:

1) **Yayın evi çözümlü içerik fişleri**  
2) **AI özgün mikro ders fişleri**  
3) **AI yayın evi-türevi fişler** *(aynı alt konuya yeni anlatım/örnek)*

ile **tek standart sözlük** üzerinden öğretim yapabilmek.

---

## 2) Zorunlu etiket standardı (Content Metadata Contract)

### 2.1 `Content` tablosu minimum kolonlar

- `content_id`
- `status` *(draft, approved, rejected)*
- `active`
- `lesson`
- `topic`
- `subtopic`
- `content_type` *(micro_lesson, worked_example, strategy_card, mistake_card)*
- `source_type` *(zorunlu)*
- `source_detail` *(yayın evi adı / “ai”)*
- `derivation_ref` *(opsiyonel: türediği content_id veya book_ref)*
- `difficulty_band` *(1-5)*
- `estimated_time_min` *(3-8 önerilir)*
- `summary_bullets`
- `strategy_steps`
- `common_mistakes`
- `mini_check_stem`
- `mini_check_options_json`
- `mini_check_correct_option`
- `page_ref`
- `created_at`
- `updated_at`

### 2.2 `source_type` sözlüğü

- `publisher`
- `ai_generated`
- `ai_variant_of_publisher`

> Bu üçlü, “hibrit fiş sistemi”nin kalbidir.

---

## 3) Fişin atomik tanımı (tek ekran kuralı)

Bir fiş:
- **3–8 dakikalık** tek dikkat dilimi,
- **tek alt konu**,
- **tek mini-check**,
- 5–8 maddelik özet + 3–6 strateji adımı + 2–5 tipik hata

içermelidir.

---

## 4) Hibrit fişlerin 3 üretim modu

### Mod A — **Manuel yayın evi fişi**
Kısa vadede en kontrollü yöntem.

- Çözümlü kitaptan
- 1 sayfa → 1 fiş

### Mod B — **PDF → Gemini Taslak Fiş** (Fast-Track)
Pilot için ana otomasyon.

- Admin, PDF yükler.
- Sayfa aralığı seçer.
- Gemini multimodal
  - 10–15 fişlik JSON array döndürür.
- Sistem `status=draft` yazar.
- 1 tıkla onay.

### Mod C — **AI yayın evi varyant anlatım**
Aynı alt konu için:

- farklı örnek
- farklı anlatım sırası
- farklı mini-check

ürettirerek pekiştirme sağlar.

**Zorunlu etiketler:**
- `source_type = ai_variant_of_publisher`
- `derivation_ref = <book_ref veya content_id>`

---

## 5) Curriculum_Map ile kilitleme

`Curriculum_Map` olmayan tag ile:
- fiş eklenmez,
- fiş önerilmez.

---

## 6) Öğrenci kullanım akışı (hibrit fiş)

1) Öğrenci soruyu yanlış yapar.  
2) Sistem sorunun `lesson/topic/subtopic` etiketini okur.  
3) `Content` içinden öneri seçer:
   - 1 `micro_lesson`
   - 1 `worked_example`
4) Fiş açılır.  
5) Mini-check çözülür.  
6) “Hemen Uygula” ile 5 soruluk mini set gelir.

---

## 7) Kalite güvence

### 7.1 Otomatik kontroller
- `summary_bullets` boş olamaz
- `mini_check_correct_option` seçeneklerde var mı?
- `estimated_time_min` 3–8 aralığında mı?

### 7.2 Onay kapısı
`publisher` ve `ai_variant_of_publisher` fişleri:
- pilotta bile önce `draft`,
- onaydan sonra `approved`.

---

## 8) Sheets ile pratik yönetim

### 8.1 İlk pilot hedefi
- 2 alt konu
- alt konu başına 10–20 fiş
- toplam 30–40 fiş

### 8.2 Hız kuralı
“Kitabı komple çevirmek” yok.  
Sadece zayıf alt konular için sayfa aralığı.

---

## 9) IDE’ye tek parça komut (Konu fiş hibrit sistemi)

```text
HEDEF:
LGS Neural-Koç öğretici içerik tarafında "Konu Fiş Hibrit Sistemi"ni uygula.
Yayın evi + AI özgün + AI yayın evi varyant fişlerini tek etiket standardında yönet.
Pilot için PDF → Gemini taslak fiş üretimini ana üretim modu yap.

SERT KURALLAR:
1) Content sheet’te source_type zorunlu.
2) ai_variant_of_publisher için derivation_ref zorunlu.
3) Curriculum_Map tag doğrulaması olmadan içerik ekleme/önerme.
4) Yeni fişler default status=draft.
5) Mini-check alanları boş olamaz.

DOSYALAR:
- app/data_access.py
- app/curriculum_engine.py
- app/content_engine.py
- app/teaching_engine.py
- app/content_ingest_engine.py
- app/llm_adapter.py
- streamlit_app.py
- config/content_mix.yaml
- tests/test_hybrid_fiches.py

GÖREVLER:
1) Content kolon şemasını doğrula/eksikleri ekle (source_type, derivation_ref, status).
2) config/content_mix.yaml oluştur:
   - default öneri: 1 publisher + 1 ai_variant_of_publisher (varsa)
3) content_ingest_engine içinde:
   - sayfa aralığı -> görüntü -> Gemini -> draft fiş yazma akışını tamamla.
4) llm_adapter:
   - generate_content_fiches_from_images fonksiyonunu strict JSON ile uygula.
5) teaching_engine:
   - suggest_content_for_wrong_question içinde
     source_type öncelik sırası uygula:
       publisher -> ai_variant_of_publisher -> ai_generated
6) Admin UI:
   - PDF → Fiş Üret ekranında Approve/Reject akışını tamamla.
7) 3 pytest yaz:
   - source_type zorunluluğu
   - derivation_ref validasyonu
   - wrong-to-learn öneri sırası

KABUL KRİTERLERİ:
- Seçili sayfalardan 10+ draft fiş Content’e yazılıyor.
- Admin 1 tıkla approved yapabiliyor.
- Yanlış sorudan tek tıkla doğru alt konu fişi açılıyor.
```

---

## 10) Kısa not (ürünleşme için)
Pilot kişisel kullanımda düşük risk olsa da,
yayın evi içeriklerinden türetilen fişlerin
ürünleştirilmesi veya geniş dağıtımı planlanırsa
lisans/izin süreçlerini ayrıca ele almak gerekir.

---

## Sonuç
Bu hibrit fiş sistemi:
- yayın evi çözüm/konu anlatımı gücünü korur,
- AI ile **çok hızlı fiş üretimi** sağlar,
- öğrencide “yanlıştan öğrenme” değerini somutlaştırır,
- Faz F ertelenmişken Sheets üzerinde bile sürdürülebilir şekilde yürür.
