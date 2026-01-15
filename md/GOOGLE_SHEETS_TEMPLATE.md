# Google Sheets Veri Şablonu

Bu dosya, LGS-Zeka platformu için Google Sheets'te oluşturulması gereken tabloların yapısını açıklar.

## 📋 Spreadsheet Yapısı

Google Sheets'te aşağıdaki sheet'leri (sekmeleri) oluşturun:

---

## 1️⃣ Sheet: `deneme_sonuclari`

**Açıklama:** Öğrencilerin deneme sınav sonuçlarını içerir.

### Sütun Yapısı

| Sütun Adı | Veri Tipi | Açıklama | Örnek Değer |
|-----------|-----------|----------|-------------|
| `Tarih` | Date | Deneme tarihi | 2024-12-01 |
| `Ders` | String | Ders adı | Matematik |
| `Konu` | String | Alt konu | Üslü İfadeler |
| `Dogru` | Integer | Doğru sayısı | 8 |
| `Yanlis` | Integer | Yanlış sayısı | 2 |
| `Bos` | Integer | Boş sayısı | 0 |
| `Net` | Float | Hesaplanan net | 7.33 |
| `Gorsel_URL` | String | Soru görseli linki (opsiyonel) | https://... |

### Örnek Veriler

```
Tarih       | Ders       | Konu              | Dogru | Yanlis | Bos | Net  | Gorsel_URL
------------|------------|-------------------|-------|--------|-----|------|------------
2024-12-01  | Matematik  | Üslü İfadeler     | 8     | 2      | 0   | 7.33 | 
2024-12-01  | Matematik  | Denklemler        | 6     | 3      | 1   | 5.00 |
2024-12-01  | Fen        | Kuvvet ve Hareket | 7     | 1      | 2   | 6.67 |
2024-12-01  | Türkçe     | Sözcükte Anlam    | 9     | 0      | 1   | 9.00 |
2024-12-02  | Matematik  | Geometri          | 5     | 4      | 1   | 3.67 |
```

---

## 2️⃣ Sheet: `ogrenciler` (Opsiyonel)

**Açıklama:** Öğrenci bilgilerini içerir.

### Sütun Yapısı

| Sütun Adı | Veri Tipi | Açıklama | Örnek Değer |
|-----------|-----------|----------|-------------|
| `ogrenci_id` | Integer | Benzersiz ID | 1 |
| `ad_soyad` | String | Öğrenci adı | Ahmet Yılmaz |
| `hedef_puan` | Integer | Hedef LGS puanı | 450 |
| `kayit_tarihi` | Date | Kayıt tarihi | 2024-09-01 |
| `sinif` | String | Sınıf seviyesi | 8 |

### Örnek Veriler

```
ogrenci_id | ad_soyad      | hedef_puan | kayit_tarihi | sinif
-----------|---------------|------------|--------------|------
1          | Ahmet Yılmaz  | 450        | 2024-09-01   | 8
2          | Ayşe Demir    | 480        | 2024-09-05   | 8
3          | Mehmet Kaya   | 420        | 2024-09-10   | 8
```

---

## 3️⃣ Sheet: `soru_analiz` (Gelecek için)

**Açıklama:** AI ile analiz edilen soruların detaylarını içerir.

### Sütun Yapısı

| Sütun Adı | Veri Tipi | Açıklama | Örnek Değer |
|-----------|-----------|----------|-------------|
| `soru_id` | Integer | Benzersiz ID | 1 |
| `tarih` | Date | Analiz tarihi | 2024-12-01 |
| `ders` | String | Ders adı | Matematik |
| `konu` | String | Konu başlığı | Üslü İfadeler |
| `soru_metni` | String | Sorunun metni | 2^3 × 2^5 = ? |
| `zorluk_seviyesi` | Integer | 1-5 arası | 3 |
| `dogru_cevap` | String | Doğru cevap | 256 |
| `ogrenci_cevabi` | String | Öğrenci cevabı | 128 |
| `ai_ipucu` | String | AI'ın verdiği ipucu | Üslü ifadelerde çarpma... |
| `gorsel_url` | String | Soru görseli | https://... |

---

## 🔧 Kurulum Adımları

### 1. Google Sheets Oluşturma

1. [Google Sheets](https://sheets.google.com) adresine gidin
2. Yeni bir spreadsheet oluşturun
3. Spreadsheet'i `LGS-Zeka-Data` olarak adlandırın
4. Yukarıdaki sheet'leri oluşturun

### 2. Sheet'leri Yapılandırma

Her sheet için:
1. İlk satıra sütun başlıklarını yazın (tam olarak yukarıdaki gibi)
2. Örnek verileri girin (test için)
3. Veri doğrulama kuralları ekleyin (opsiyonel)

### 3. Google Cloud Console Kurulumu

1. [Google Cloud Console](https://console.cloud.google.com/) gidin
2. Yeni proje oluşturun: `lgs-zeka-project`
3. **Google Sheets API**'yi etkinleştirin:
   - API & Services > Library
   - "Google Sheets API" arayın
   - Enable'a tıklayın

4. **Service Account** oluşturun:
   - API & Services > Credentials
   - Create Credentials > Service Account
   - Adı: `lgs-zeka-service`
   - Role: Editor
   - Create and Continue

5. **JSON Key** indirin:
   - Service Account'a tıklayın
   - Keys sekmesi > Add Key > Create New Key
   - JSON seçin ve Create
   - İndirilen dosyayı güvenli bir yere kaydedin

### 4. Spreadsheet'i Paylaşma

1. Google Sheets dosyanızı açın
2. Sağ üstteki "Share" butonuna tıklayın
3. Service Account email adresini ekleyin:
   - Format: `lgs-zeka-service@lgs-zeka-project.iam.gserviceaccount.com`
4. "Editor" yetkisi verin
5. Send

### 5. Secrets.toml Yapılandırması

1. `.streamlit/secrets.toml` dosyasını açın
2. İndirdiğiniz JSON key içeriğini `[gcp_service_account]` bölümüne yapıştırın
3. Spreadsheet URL'sinden key'i kopyalayın:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_KEY_BURASI/edit
   ```
4. `spreadsheet_key` değerine yapıştırın

---

## 📊 Veri Formatı Notları

### Tarih Formatı
- Format: `YYYY-MM-DD` (örn: 2024-12-01)
- Google Sheets'te Date formatında olmalı

### Net Hesaplama
- Formül: `Net = Doğru - (Yanlış / 3)`
- Manuel girebilir veya Google Sheets formülü kullanabilirsiniz:
  ```
  =D2-(E2/3)
  ```
  (D: Doğru, E: Yanlış sütunları)

### Ders İsimleri (Standart)
- Matematik
- Fen Bilimleri
- Türkçe
- İnkılap Tarihi
- Din Kültürü
- İngilizce

### Konu İsimleri Örnekleri

**Matematik:**
- Üslü İfadeler
- Denklemler
- Geometri
- Olasılık
- İstatistik

**Fen Bilimleri:**
- Kuvvet ve Hareket
- Madde ve Doğası
- Elektrik
- DNA ve Genetik

**Türkçe:**
- Sözcükte Anlam
- Cümlede Anlam
- Paragraf
- Yazım Kuralları

---

## 🧪 Test Verisi Oluşturma

Hızlı test için aşağıdaki Python scriptini kullanabilirsiniz:

```python
import pandas as pd
from datetime import datetime, timedelta
import random

# Ders ve konular
dersler = {
    'Matematik': ['Üslü İfadeler', 'Denklemler', 'Geometri', 'Olasılık'],
    'Fen Bilimleri': ['Kuvvet ve Hareket', 'Madde', 'Elektrik', 'DNA'],
    'Türkçe': ['Sözcükte Anlam', 'Cümlede Anlam', 'Paragraf'],
}

# Test verisi oluştur
data = []
base_date = datetime.now() - timedelta(days=30)

for i in range(50):
    ders = random.choice(list(dersler.keys()))
    konu = random.choice(dersler[ders])
    dogru = random.randint(3, 10)
    yanlis = random.randint(0, 5)
    bos = random.randint(0, 2)
    net = round(dogru - (yanlis / 3), 2)
    
    data.append({
        'Tarih': (base_date + timedelta(days=i)).strftime('%Y-%m-%d'),
        'Ders': ders,
        'Konu': konu,
        'Dogru': dogru,
        'Yanlis': yanlis,
        'Bos': bos,
        'Net': net,
        'Gorsel_URL': ''
    })

df = pd.DataFrame(data)
df.to_csv('test_data.csv', index=False)
print("Test verisi oluşturuldu: test_data.csv")
```

---

## ✅ Doğrulama

Kurulumu doğrulamak için:

1. `setup_check.py` scriptini çalıştırın:
   ```bash
   python setup_check.py
   ```

2. Streamlit uygulamasını başlatın:
   ```bash
   streamlit run app.py
   ```

3. Dashboard'da verilerin göründüğünü kontrol edin

---

## 🔒 Güvenlik Notları

- ✅ Service Account JSON dosyasını asla Git'e eklemeyin
- ✅ `.gitignore` dosyasında `secrets.toml` olduğundan emin olun
- ✅ Spreadsheet'i sadece gerekli kişilerle paylaşın
- ✅ Production'da Supabase kullanmayı düşünün

---

## 📞 Sorun Giderme

### "Permission Denied" Hatası
- Service Account email'inin Spreadsheet'e Editor yetkisiyle eklendiğinden emin olun

### "Spreadsheet Not Found" Hatası
- `spreadsheet_key` değerinin doğru olduğunu kontrol edin
- Spreadsheet URL'sinden doğru kısmı kopyaladığınızdan emin olun

### "API Quota Exceeded" Hatası
- `db_manager.py` içinde cache sürelerini artırın
- Google Cloud Console'da quota limitlerini kontrol edin

---

**Son Güncelleme:** 4 Aralık 2024
