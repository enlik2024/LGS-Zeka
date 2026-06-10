# LGS-Zeka

**LGS-Zeka**, 8. sınıf öğrencilerinin LGS (Liselere Geçiş Sistemi) sınavına hazırlanmasına yardımcı olan, yapay zeka destekli bir platformdur.

## Özellikler

- **Mini Deneme** — Sabit veya adaptatif deneme sınavları, zamanlayıcı, optik form çıktısı, otomatik puanlama
- **Öğren** — Konu/kazanım bazlı içerik keşfi, Sokratik yapay zeka ders anlatımı, flash kartlar
- **AI Koç** — Kişiselleştirilmiş sohbet tabanlı rehberlik (destekleyici/analitik/motive edici/arkadaş canlısı kişilik)
- **Soru Analizi** — Soru görseli yükleme, AI çözüm, akış şeması, sesli anlatım, benzer soru üretimi
- **Dashboard** — Performans analizi, master haritası, sınav geçmişi, haftalık rapor
- **Çalışma Programı** — AI tarafından oluşturulmuş haftalık ders programı, takvim dışa aktarma
- **Admin PDF** — Yayın PDF'lerinden AI ile soru ve içerik çıkarma
- **Oyunlaştırma** — XP puanı, seri, seviye, başarımlar
- **Veli Paneli** — PIN korumalı ebeveyn kontrol paneli

## Teknolojiler

| Bileşen | Teknoloji |
|---------|-----------|
| Platform | Python 3.10+, Streamlit |
| Yapay Zeka | Google Gemini API (gemini-3-flash, gemini-2.5-flash) |
| Veritabanı | Supabase (PostgreSQL) |
| Alternatif DB | Google Sheets (yedek), CSV (yerel) |
| Görsel İşleme | Pillow, PyMuPDF |
| Seslendirme | gTTS, Gemini TTS |
| Konfigürasyon | YAML, TOML, dotenv |
| Konteyner | Docker |

## Kurulum

### Gereksinimler

- Python 3.10 veya üzeri
- Google Gemini API anahtarı ([Google AI Studio](https://makersuite.google.com/app/apikey))
- (İsteğe bağlı) Supabase projesi
- (İsteğe bağlı) Google Sheets erişimi

### Adımlar

```bash
# 1. Depoyu klonlayın
git clone https://github.com/kullanici/lgs-zeka.git
cd lgs-zeka

# 2. Sanal ortam oluşturun
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
.\venv\Scripts\activate   # Windows

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Secrets dosyasını yapılandırın
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.toml dosyasını düzenleyerek API anahtarlarınızı girin
```

### Secrets Yapılandırması

`.streamlit/secrets.toml` dosyasına aşağıdaki bilgileri girin:

```toml
[gcp_service_account]
# Google Service Account JSON (Google Sheets için)
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "..."
# ...

[gemini]
api_key = "AIza..."          # Google Gemini API anahtarı
api_key_secondary = "AIza..." # Yedek API anahtarı (opsiyonel)

[perplexity]
api_key = "pplx-..."          # Perplexity API anahtarı (opsiyonel, beta)

SUPABASE_URL = "https://....supabase.co"
SUPABASE_KEY = "eyJhbGciOiJ..."

[app]
database_type = "supabase"    # "google_sheets" veya "supabase"
```

PIN kodu (varsayılan: `1234`) değiştirmek için `parent_pin` ekleyin.

### Docker ile Çalıştırma

```bash
docker build -t lgs-zeka .
docker run -p 8501:8501 -v $PWD/.streamlit/secrets.toml:/app/.streamlit/secrets.toml lgs-zeka
```

### Çalıştırma

```bash
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` adresine gidin.

## Proje Yapısı

```
├── app.py                      # Ana giriş noktası
├── pages/                      # Streamlit sayfa modülleri
│   ├── bugun.py                #   Bugünkü plan
│   ├── mini_deneme.py          #   Mini deneme sınavı
│   ├── ogren.py                #   Öğrenme modülü
│   ├── ai_koc.py               #   AI Koç sohbet
│   ├── soru_analiz.py          #   Soru analizi
│   ├── calisma_programi.py     #   Çalışma programı
│   ├── dashboard.py            #   Performans kokpiti
│   ├── ayarlar.py              #   Ayarlar
│   └── admin_pdf.py            #   PDF içerik yükleme
├── utils/                      # İş mantığı katmanı
│   ├── gemini_helper.py        #   Gemini API sarmalayıcı
│   ├── llm_adapter.py          #   LLM soyutlama katmanı
│   ├── db_manager.py           #   Veritabanı yöneticisi
│   ├── supabase_client.py      #   Supabase istemcisi
│   ├── exam_engine.py          #   Sınav motoru
│   ├── scoring.py              #   LGS puan hesaplama
│   ├── scheduler_engine.py     #   Program oluşturucu
│   ├── analysis_engine.py      #   Analiz motoru
│   ├── gamification.py         #   Oyunlaştırma
│   └── ...                     #   Diğer modüller
├── components/                 # Yeniden kullanılabilir UI
├── prompts/                    # AI sistem promptları
├── config/                     # Yapılandırma dosyaları
├── sql/                        # Supabase DDL
├── assets/                     # Statik dosyalar
├── tests/                      # Testler
├── .streamlit/secrets.toml.example  # Secrets şablonu
└── requirements.txt
```

## Dış Servisler

| Servis | Kullanım Amacı |
|--------|----------------|
| Google Gemini AI | Soru analizi, sohbet, içerik üretimi, Sokratik ders |
| Supabase | PostgreSQL veritabanı (öğrenci verileri, sorular) |
| Google Sheets | Alternatif/yedek veritabanı (isteğe bağlı) |
| Perplexity API | Beta "Critic" doğrulama modu (isteğe bağlı) |
| Google TTS | Sesli anlatım |

## Geliştirme

Testleri çalıştırmak için:

```bash
pytest tests/
```

Özellikleri etkinleştirmek/kapatmak için `config/feature_flags.yaml` dosyasını düzenleyin.

## Lisans

Bu proje özel bir lisans altındadır.
