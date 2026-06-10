# LGS-Zeka

**LGS-Zeka**, 8. sınıf öğrencilerinin LGS (Liselere Geçiş Sistemi) sınavına hazırlanmasına yardımcı olan, yapay zeka destekli bir platformdur.

---

## İçindekiler

- [Hızlı Başlangıç (3 Adımda)](#hızlı-başlangıç-3-adımda)
- [Özellikler](#özellikler)
- [Ne Gerekli, Ne Değil?](#ne-gerekli-ne-değil)
- [Kurulum Detaylı](#kurulum-detaylı)
- [İlk Çalıştırma](#ilk-çalıştırma)
- [AI Özelliklerini Aktifleştirme](#ai-özelliklerini-aktifleştirme)
- [Secrets Yapılandırması](#secrets-yapılandırması)
- [Docker ile Çalıştırma](#docker-ile-çalıştırma)
- [Dosya Referansları (Geliştiriciler İçin)](#dosya-referansları-geliştiriciler-için)
- [Proje Yapısı](#proje-yapısı)
- [Sorun Giderme](#sorun-giderme)

---

## Hızlı Başlangıç (3 Adımda)

Hiçbir API anahtarı olmadan, sadece CSV dosyalarıyla çalışır:

```bash
# 1. Sanal ortam oluşturup bağımlılıkları yükle
python -m venv venv
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

# 2. Secrets dosyası oluştur (isteğe bağlı, boş olabilir)
echo '' > .streamlit/secrets.toml

# 3. Çalıştır
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` açılır. Dashboard, Mini Deneme, Öğren, Çalışma Programı, Ayarlar **kutudan çıktığı gibi çalışır**.

---

## Özellikler

| Sayfa | Ne İşe Yarar | AI Gerektirir? |
|-------|-------------|----------------|
| **Bugün** | Günlük ders blokları, zaman takibi, odak modu | Hayır |
| **Mini Deneme** | Sabit/adaptatif deneme, zamanlayıcı, optik form çıktısı, otomatik puanlama | Hayır |
| **Öğren** | Konu/kazanım bazlı içerik, flash kartlar, Sokratik ders | Hayır (içerik görüntüleme) / Evet (AI ders) |
| **Dashboard** | Performans analizi, master haritası, sınav geçmişi, haftalık rapor | Hayır |
| **AI Koç** | Kişiselleştirilmiş sohbet tabanlı rehberlik | Evet (Gemini API) |
| **Soru Analizi** | Soru görseli yükleme, AI çözüm, akış şeması, sesli anlatım | Evet (Gemini API) |
| **Çalışma Programı** | Haftalık ders programı, takvim dışa aktarma, veli PIN koruması | Hayır |
| **Admin PDF** | Yayın PDF'lerinden AI ile soru ve içerik çıkarma | Evet (Gemini API) |
| **Ayarlar** | Profil, veritabanı seçimi, API anahtarı yönetimi, veli paneli | Hayır |
| **Oyunlaştırma** | XP puanı, seri, seviye, başarımlar (her sayfada gösterilir) | Hayır |

---

## Ne Gerekli, Ne Değil?

### Hiçbir şey gerekmez (CSV ile çalışır)
- Dashboard, Mini Deneme, Öğren (içerik görüntüleme), Çalışma Programı, Ayarlar
- Tüm veriler `curriculum_map.csv`, `questions.csv`, `exams.csv` vb. dosyalardan okunur
- Bu dosyalar repo ile birlikte gelir, **ekstra hiçbir şey yapmanız gerekmez**

### Gemini API anahtarı gerekir (AI özellikleri için)
- Soru Analizi (görsel yükleme -> AI çözüm)
- AI Koç (sohbet)
- AI ders anlatımı (Öğren sayfasında)
- Admin PDF (içerik çıkarma)
- **Nasıl alınır:** [Google AI Studio](https://makersuite.google.com/app/apikey) — ücretsiz, dakikada 60 istek

### Supabase gerekir (bulut kayıt için)
- Analiz geçmişi kaydetme
- Flashcard kaydetme
- Programı buluta kaydetme
- Profil güncelleme
- **Zorunlu değil.** Bunlar olmazsa uygulama çalışmaya devam eder, sadece kayıtlar oturum boyunca kalır

### Google Sheets gerekir (alternatif veritabanı)
- Ayarlar sayfasından "Google Sheets" seçilirse kullanılır
- Varsayılan olarak kapalıdır

---

## Kurulum Detaylı

### Gereksinimler

- Python 3.9 veya üzeri
- pip (Python paket yöneticisi)
- İnternet bağlantısı (AI özellikleri için)
- (Önerilen) Git

### Adım Adım

**Windows:**
```powershell
# 1. Klasöre gidin
cd C:\Users\...\lgs-zeka

# 2. Sanal ortam oluşturun
python -m venv venv

# 3. Sanal ortamı aktifleştirin
.\venv\Scripts\activate

# 4. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 5. Secrets dosyası oluşturun (boş dosya da yeter)
echo $null >> .streamlit/secrets.toml

# 6. Uygulamayı başlatın
streamlit run app.py
```

**Linux / Mac:**
```bash
cd /path/to/lgs-zeka
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch .streamlit/secrets.toml
streamlit run app.py
```

---

## İlk Çalıştırma

Uygulama açıldığında:

1. Sol kenar çubuğunda sayfalar listelenir
2. **Bugün** sayfası ana sayfadır (günlük program)
3. Sağ üst köşede XP puanı ve seviye gösterilir
4. **Ayarlar** sayfasından:
   - PIN kodu ile veli paneline giriş (varsayılan: `1234`)
   - Veritabanı tipi değiştirilebilir (Supabase / Google Sheets / Yerel CSV)
   - API anahtarları girilebilir

**Not:** Varsayılan olarak veritabanı "Supabase" modundadır. Bağlantı yoksa hiçbir hata vermez, CSV'ye düşer. Bunu Ayarlar sayfasından "Yerel (CSV/Excel)" olarak değiştirebilirsiniz.

---

## AI Özelliklerini Aktifleştirme

**Yöntem 1 — secrets.toml (önerilen):**
```toml
[gemini]
api_key = "AIzaSy..."  # Google AI Studio'dan alın
```

**Yöntem 2 — Uygulama içinden:**
1. Ayarlar sayfasına gidin
2. PIN ile veli paneline girin (`1234`)
3. "Kendi API Anahtarını Kullan" bölümüne anahtarı yazıp kaydedin
4. Bu yöntemde anahtar `config/user_settings.json` dosyasına kaydedilir

API anahtarı olmadan Soru Analizi ve AI Koç sayfaları hata mesajı gösterir, uygulamanın geri kalanı etkilenmez.

### OpenAI / GPT ile Çalıştırma

Sistem sadece Gemini'ye bağlı değildir. `utils/llm_adapter.py` katmanı sayesinde OpenAI (GPT-4, GPT-4o) ve diğer LLM sağlayıcılarına geçiş için hazır altyapı vardır.

**Mevcut durum:** `LLMAdapter` sınıfı `provider="gemini"` parametresi ile çalışır. OpenAI desteği eklemek için:

1. `utils/openai_helper.py` oluşturun — OpenAI API'yi sarmalayan sınıf (GeminiHelper ile aynı arayüzde)
2. `utils/llm_adapter.py` içinde `if self.provider == "openai"` dallarını ekleyin
3. `utils/config_manager.py` içinde OpenAI API anahtarı yükleme mantığını ekleyin
4. `.streamlit/secrets.toml.example` dosyasına OpenAI bölümünü ekleyin:

```toml
[openai]
api_key = "sk-proj-..."            # OpenAI API anahtarı
api_key_secondary = "sk-proj-..."  # Yedek (opsiyonel)
model = "gpt-4o"                   # Varsayılan model
```

Kod yapısı:

```
utils/
├── gemini_helper.py      # Mevcut: Gemini API sarmalayıcı
├── openai_helper.py      # Eklenecek: OpenAI API sarmalayıcı
├── llm_adapter.py        # Mevcut: soyutlama katmanı (provider seçimi)
└── config_manager.py     # Mevcut: API anahtarı yönetimi (provider bazlı)
```

`LLMAdapter`'daki her metod (`generate_json`, `chat`, `vision_analyze` vb.) `if provider == "gemini"` / `elif provider == "openai"` şeklinde dallanmıştır. Yeni bir provider eklemek için her metoda yeni bir `elif` dalı ve ilgili implementasyonu eklemeniz yeterlidir.

Perplexity API (beta "Critic" modu) ise sağlayıcıdan bağımsız çalışır — doğrudan `requests` ile API'yi çağırır.

---

## Secrets Yapılandırması

`.streamlit/secrets.toml` dosyası tüm API anahtarlarını ve hassas bilgileri içerir. Bu dosya `.gitignore` ile korunur, GitHub'a push edilmez.

Örnek bir yapılandırma (`.streamlit/secrets.toml.example` dosyasında detaylı halini bulabilirsiniz):

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project"
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "..."

[gemini]
api_key = "AIzaSy..."              # Zorunlu (AI özellikleri için)
api_key_secondary = "AIzaSy..."    # Yedek (opsiyonel)

[perplexity]
api_key = "pplx-..."               # Beta modu (opsiyonel)

SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJ..."

[app]
database_type = "supabase"         # supabase / google_sheets / local

# Veli paneli PIN kodu (varsayılan: 1234)
# parent_pin = "5678"
```

---

## Docker ile Çalıştırma

```bash
# Build
docker build -t lgs-zeka .

# Çalıştır (secrets dosyasını mount et)
docker run -p 8501:8501 -v "$(pwd)/.streamlit/secrets.toml:/app/.streamlit/secrets.toml" lgs-zeka
```

---

## Dosya Referansları (Geliştiriciler İçin)

Bu dosyalar AI yapısını anlamak ve geliştirme yapmak isteyenler için hazırlanmıştır:

| Dosya | İçerik |
|-------|--------|
| [`aikomut.md`](aikomut.md) | **AI Prompt Kataloğu** — Hangi sayfa hangi prompt'u kullanır, hangi JSON formatında çıktı üretir, tüm roller ve örnek çıktılar |
| [`konu_fis_hibrit_sistemi_detayli.md`](konu_fis_hibrit_sistemi_detayli.md) | **Content Metadata Contract** — AI içerik fişi şeması, `content_type` standardı, kaynak etiketleme kuralları |
| [`soru_hibrit_sistemi_detayli.md`](soru_hibrit_sistemi_detayli.md) | **Question Metadata Contract** — Soru şeması, `question_origin` etiketleme, zorluk derecelendirme standardı |

Bu dokümanlar `prompts/` klasöründeki Python dosyalarında kullanılan formatları ve kuralları açıklar. Yeni bir AI özelliği eklerken veya mevcut prompt'ları değiştirirken bu sözleşmelere uyulması gerekir.

---

## Proje Yapısı

```
├── app.py                      # Ana giriş noktası (streamlit run app.py)
├── pages/                      # Sayfa modülleri (her biri bir show() fonksiyonu içerir)
│   ├── bugun.py                #   Bugünkü plan
│   ├── mini_deneme.py          #   Mini deneme sınavı
│   ├── ogren.py                #   Öğrenme modülü
│   ├── ai_koc.py               #   AI Koç sohbet
│   ├── soru_analiz.py          #   Soru analizi (görsel yükleme)
│   ├── calisma_programi.py     #   Çalışma programı oluşturucu
│   ├── dashboard.py            #   Performans kokpiti
│   ├── ayarlar.py              #   Ayarlar paneli
│   └── admin_pdf.py            #   PDF içerik yükleme
├── utils/                      # İş mantığı
│   ├── gemini_helper.py        #   Gemini API sarmalayıcı + anahtar rotasyonu
│   ├── llm_adapter.py          #   LLM soyutlama katmanı
│   ├── db_manager.py           #   3 katmanlı veritabanı (Supabase -> Sheets -> CSV)
│   ├── supabase_client.py      #   Supabase bağlantı fabrikası
│   ├── config_manager.py       #   Merkezi yapılandırma yükleyici
│   ├── exam_engine.py          #   Sınav oluşturma motoru
│   ├── scoring.py              #   LGS puan hesaplama
│   ├── scheduler_engine.py     #   Haftalık program oluşturucu
│   ├── analysis_engine.py      #   Performans analizi
│   ├── gamification.py         #   Oyunlaştırma (XP, seviye, başarım)
│   ├── content_engine.py       #   İçerik yönetimi
│   └── ...
├── components/                 # Tekrar kullanılabilir UI bileşenleri
│   ├── socratic_chat.py        #   Sokratik ders sohbeti
│   ├── flashcard_viewer.py     #   Flash kart gösterici
│   ├── mermaid_renderer.py     #   Mermaid.js akış şeması
│   └── error_tagger.py         #   Hata etiketleme arayüzü
├── prompts/                    # AI sistem promptları
│   ├── analysis_prompts.py     #   Soru analizi promptları
│   ├── teaching_prompts.py     #   Ders anlatımı promptları
│   ├── content_generation_prompts.py  # İçerik üretimi promptları
│   └── beta_prompts.py         #   Beta / DeepTutor promptları
├── config/                     # Yapılandırma dosyaları
│   ├── app_config.yaml         #   Uygulama ana yapılandırması
│   ├── feature_flags.yaml      #   Özellik açma/kapama
│   ├── content_mix.yaml        #   İçerik dağılım oranları
│   └── question_mix.yaml       #   Soru kaynak dağılımı
├── assets/                     # Statik dosyalar (görseller, şekiller)
├── data/                       # Çalışma zamanı verileri (gitignore)
├── tests/                      # Testler
├── sql/supabase_lgs_tables.sql # Supabase veritabanı şeması
├── aikomut.md                  # AI prompt kataloğu (dokümantasyon)
├── konu_fis_hibrit_sistemi_detayli.md  # İçerik şema sözleşmesi
├── soru_hibrit_sistemi_detayli.md      # Soru şema sözleşmesi
├── .streamlit/
│   ├── config.toml             #   Streamlit sunucu ayarları
│   └── secrets.toml.example    #   API anahtarı şablonu
├── requirements.txt            # Python bağımlılıkları
├── Dockerfile                  # Docker imaj tanımı
└── .gitignore                  # Git koruma listesi
```

---

## Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` çalıştırın, sanal ortamın aktif olduğundan emin olun |
| Sayfalar yüklenmiyor / hata gösteriyor | `.streamlit/secrets.toml` dosyasının var olduğundan emin olun (boş olabilir) |
| "API key not configured" hatası | AI özelliklerini kullanmak için Gemini API anahtarı gerekir. Ayarlar sayfasından girebilirsiniz |
| "Supabase bağlantısı bulunamadı" | Önemli değil. Uygulama CSV ile devam eder. Ayarlar'dan "Yerel (CSV)" seçeneğini seçebilirsiniz |
| Port 8501 dolu | `streamlit run app.py --server.port=8502` ile farklı port kullanın |
| Değişiklikler kaydedilmiyor | Varsayılan olarak Supabase modundadır. CSV'de kalıcı kayıt için Ayarlar > "Yerel (CSV)" seçin |
| PIN kodu ne? | Varsayılan: `1234`. Değiştirmek için `secrets.toml` dosyasına `parent_pin = "yeniPin"` ekleyin |
| `FileNotFoundError: data/...` | `data/` klasörü `.gitignore`'da. Elle oluşturun: `mkdir data` |

---

## Dış Servisler

| Servis | Kullanım Amacı | Zorunlu? |
|--------|----------------|----------|
| OpenAI GPT | AI sohbet, soru analizi, içerik üretimi (henüz implementasyonu yapılmadı, README'deki kılavuza bakın) | Hayır |
| Google Gemini AI | Soru analizi, sohbet, içerik üretimi, Sokratik ders (şu an aktif sağlayıcı) | Hayır (AI özellikleri için gerekli) |
| Supabase | PostgreSQL veritabanı (kalıcı kayıt) | Hayır (CSV yeterli) |
| Google Sheets | Alternatif veritabanı | Hayır |
| Perplexity API | Beta "Critic" doğrulama modu | Hayır (opsiyonel) |

---

## Geliştirme

```bash
# Testleri çalıştırma
pytest tests/

# Özellikleri açıp kapama
# config/feature_flags.yaml dosyasını düzenleyin
```

---

## Lisans

MIT License. Detaylı bilgi için [LICENSE](LICENSE) dosyasına bakın.
