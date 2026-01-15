# FAZ D FAST-TRACK — IDE’ye Verilecek Açıklamalı Master Komut
## “Bu dosyayı neden veriyoruz?” + “Tam olarak ne yaptırıyoruz?”

Bu dosyayı IDE’ye veriyoruz çünkü pilot aşamada **öğretici içerik** kısmını hızla çalışır hale getirmek istiyoruz.  
Soru motoru tek başına yetmiyor; öğrencinin yanlış yaptığı sorudan sonra hızlıca toparlanmasını sağlayan **mikro ders fişleri** gerekiyor.

### Bu görevdeki tek amaç
**PDF’den seçtiğimiz sayfa aralığına dayanarak Gemini 2.5 ile 10–20 içerik fişi üretmek** ve  
bu fişleri öğrencide **“İlgili Konuyu Öğren”** butonuna bağlamak.

### Bu neden en doğru pilot hamlesi?
- Tam otomatik kitap işleme hattı kurmak çok zaman alır.
- Pilot için değer kanıtı daha önemlidir.
- Bu yaklaşım 80/20 ile en hızlı “yanlış → öğren” döngüsünü çalıştırır.

### Bilerek kapsam dışı bıraktık
- Sheets → Supabase (FAZ F)
- Otomatik sayfa keşfi
- Kitabın tamamını fişleme
- Gelişmiş kalite/analitik

### IDE’den beklenen davranış
Aşağıdaki komutu **aynen** uygula:
- Dosya/klasör yapısını değiştirme.
- Ekstra mimari genişletme yapma.
- Sadece listelenen fonksiyonları, UI’ları ve testleri sırayla tamamla.

---


```text
MASTER CONTEXT:
Bu görev, LGS Neural-Koç projesinde FAZ D “Eğitim Katmanı” için PILOT seviyesinde 80/20 hız çözümüdür.
Amaç: "PDF → Fiş Üret" mini admin aracı + öğrencide "Yanlıştan Öğrenmeye Tek Tık" akışını 1-2 günde çalışır hale getirmek.
Mükemmel OCR/pipeline beklenmiyor. Seçili sayfa aralığıyla Gemini multimodal kullanılacak.

DOSYA SÖZLEŞMESİ (DEĞİŞTİRİLEMEZ):
Aşağıdaki dosyaların adı/konumu değiştirilemez, taşınamaz, bölünemez:
- streamlit_app.py
- app/data_access.py
- app/llm_adapter.py
- app/analysis_engine.py
- app/exam_engine.py
- app/schedule_engine.py
- app/content_engine.py
- app/curriculum_engine.py
- app/teaching_engine.py
- app/content_ingest_engine.py
- config/settings.yaml
- config/feature_flags.yaml
- tests/

SERT KURALLAR:
1) LLM çağrıları sadece app/llm_adapter.py üzerinden.
2) Google Sheets erişimi sadece app/data_access.py üzerinden.
3) Bu fazda otomatik sayfa keşfi YOK; kullanıcı sayfa aralığı girer.
4) Gemini 2.5 multimodal, SAYFA GÖRSELLERİNDEN fiş üretir.
5) Çıktı SADECE strict JSON olacak; parse/schema doğrulaması zorunlu.
6) Content’e yazılan her yeni fiş önce status="draft" olacak.
7) Admin ekranda her fiş için Approve / Reject (ve opsiyonel Quick Edit) olacak.
8) Öğrenci ekranında yanlış soru sonrası "İlgili Konuyu Öğren" butonu zorunlu.
9) UI öğrenci tarafında 3 kart kuralı: aynı anda en fazla 3 ana odak.
10) En az 3 pytest senaryosu yazılacak.

ÖN KOŞUL 1 — SHEETS TABLARI:
Google Sheets’te aşağıdaki iki tab mevcut değilse oluştur; varsa kolonları EKLE ve uyumlu hale getir.

A) Curriculum_Map (minimum kolonlar)
- lesson
- topic
- subtopic
- learning_objective
- active

B) Content (minimum kolonlar)
- content_id
- status               (draft/approved/rejected)
- source_type          (publisher/ai_generated)
- publisher
- lesson
- topic
- subtopic
- content_type         (micro_lesson/worked_example)
- difficulty_band      (1-5)
- estimated_time_min
- summary_bullets
- strategy_steps
- common_mistakes
- mini_check_stem
- mini_check_options_json
- mini_check_correct_option
- page_ref
- active
- created_at

NOT: summary_bullets / strategy_steps / common_mistakes / mini_check_* alanları bu fazın “fiş yaklaşımı” omurgasıdır.

ÖN KOŞUL 2 — QUESTIONS ETİKETLERİ:
Öğrenci yanlış sorudan doğru alt konuya bağlanacak.
Questions sheet’te aşağıdaki kolonlar yoksa ekle:
- lesson, topic, subtopic

GÖREV PAKETİ (SIRASI DEĞİŞTİRİLEMEZ):

1) app/data_access.py
   1.1) Sheets bağlantı ayarlarını config/settings.yaml üzerinden okuyacak şekilde doğrula.
   1.2) Aşağıdaki fonksiyonları EKLE veya tamamla:
        - load_curriculum_map() -> DataFrame
        - load_content() -> DataFrame
        - append_content_rows(rows: list[dict]) -> None
        - update_content_status(content_id: str, status: str, fields: dict | None = None) -> None
        - get_approved_content(lesson, topic, subtopic, limit=2) -> DataFrame
   1.3) append_content_rows içine:
        - content_id otomatik üretimi: CNT-0001 formatı
        - created_at otomatik set
        - status default "draft"
        - active default FALSE
        kurallarını koy.

2) app/content_ingest_engine.py
   2.1) Aşağıdaki yardımcı fonksiyonları yaz:
        - parse_page_range(page_range_str: str) -> list[int]
          Örn: "12-20" -> [12,13,...,20]
        - pdf_pages_to_images(pdf_path: str, page_numbers: list[int]) -> list[bytes]
          Not: pdf2image veya uygun bir yöntemle sayfaları PNG/JPG bytes üret.
        - build_fiche_rows_from_llm_output(output_json: dict, meta: dict) -> list[dict]
          meta = {lesson, topic, subtopic, publisher}
          Bu fonksiyon Content sheet kolonlarına birebir map eder.

3) app/llm_adapter.py
   3.1) Gemini 2.5 multimodal çağrısı için tek fonksiyon ekle:
        - generate_content_fiches_from_images(images: list[bytes], lesson: str, topic: str, subtopic: str, publisher: str | None) -> dict
   3.2) Bu fonksiyon şu PROMPT’u KULLANACAK ve SADECE JSON döndürecek:

        GÖREV: PDF sayfalarından LGS düzeyi öğretici fişler üret.
        KURALLAR:
        - Sadece şu alt konu için üret: {lesson}/{topic}/{subtopic}
        - En fazla 15 fiş üret. Kalite > adet.
        - Tam metin kopyalama yapma.
        - Çıktı SADECE JSON olacak.

        JSON ŞEMASI:
        {
          "fiches": [
            {
              "content_type": "micro_lesson|worked_example",
              "difficulty_band": 1-5,
              "estimated_time_min": 3-8,
              "summary_bullets": ["5-8 madde"],
              "strategy_steps": ["3-6 adım"],
              "common_mistakes": ["2-5 madde"],
              "mini_check_stem": "tek soru",
              "mini_check_options_json": {"A":"..","B":"..","C":"..","D":".."},
              "mini_check_correct_option": "A|B|C|D",
              "page_ref": "PDF s.xx"
            }
          ]
        }

   3.3) Strict JSON doğrulaması yap:
        - Parse hatasında 1 kez retry
        - İkinci hata -> kullanıcıya anlaşılır error

4) app/content_engine.py
   4.1) Basit seçim fonksiyonları:
        - get_recommended_content(lesson, topic, subtopic, source_filter=None, limit=2)
          Varsayılan: status=approved AND active=TRUE filtrele.

5) app/curriculum_engine.py
   5.1) Tag doğrulama:
        - validate_tags(lesson, topic, subtopic) -> bool
          Curriculum_Map’te yoksa False döndür.

6) app/teaching_engine.py
   6.1) Yanlıştan öğrenmeye köprü:
        - suggest_content_for_wrong_question(question_id, student_id) -> dict
          Adımlar:
          a) Questions’tan lesson/topic/subtopic bul
          b) validate_tags
          c) Content’ten 1 micro_lesson + 1 worked_example çek
          d) UI’ye uygun payload döndür

7) streamlit_app.py — ADMIN UI
   7.1) Yeni menü/sekme ekle:
        - "Admin" -> "PDF → Fiş Üret"
   7.2) Bu ekranda 3 input + 1 buton olacak:
        - PDF upload
        - Subtopic dropdown (Curriculum_Map’ten)
        - Page range text input ("12-20")
        - "Fişleri Üret (Taslak)"
   7.3) Buton akışı:
        a) PDF’i temp’e kaydet
        b) parse_page_range
        c) pdf_pages_to_images
        d) llm_adapter.generate_content_fiches_from_images
        e) build_fiche_rows_from_llm_output
        f) append_content_rows (status="draft")

   7.4) Aynı ekranda “Taslak Fişler” listesi:
        - seçili alt konuya ait status="draft"
        - her satırda:
          Approve -> update_content_status(..., "approved", {"active": True})
          Reject  -> update_content_status(..., "rejected", {"active": False})
          (Opsiyonel Quick Edit: summary_bullets alanını tek text area ile düzelt)

8) streamlit_app.py — ÖĞRENCİ UI
   8.1) Soru çözme ekranında:
        - öğrenci yanlış yaptığında görünür:
          "İlgili Konuyu Öğren"
   8.2) Buton tıklanınca:
        a) teaching_engine.suggest_content_for_wrong_question çağır
        b) 1 micro_lesson + 1 worked_example göster
        c) mini_check’i aynı ekranda göster
        d) (Opsiyonel) "Hemen 5 soru uygula" butonu:
           - aynı alt konu + kolay/orta karışık fixed mini set oluştur

9) tests/
   9.1) tests/test_phase_d_fast_track.py oluştur ve min 3 test yaz:
        T1) parse_page_range doğru çalışıyor
        T2) LLM çıktısı mock ile -> build_fiche_rows -> Content kolon map doğru
        T3) update_content_status ile draft->approved geçişi çalışıyor

KABUL KRİTERLERİ (DoD):
- Admin ekranda seçili 8-10 sayfadan en az 10 adet "draft" fiş Content sheet’e yazılıyor.
- Admin 1 tıkla en az 5 fişi "approved" yapabiliyor.
- Öğrenci bir soruyu yanlış yaptığında "İlgili Konuyu Öğren" ile aynı alt konudaki approved içerik açılıyor.
- JSON parse/schema hatasında sistem çökmeden kullanıcıya uyarı veriyor.
- 3 pytest yeşil.

ÇIKTI BEKLENTİSİ:
Bu görev sonunda pilot için öğretici içerik motorunun minimum çalışan sürümü hazır olacak.
Faz F (DB göçü) ve tam otomatik PDF hattı bu görev kapsamı dışındadır.
```
