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
