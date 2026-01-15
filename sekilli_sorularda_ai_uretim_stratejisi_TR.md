# Şekilli Sorularda AI Varyant / Yeni Soru Üretimi Stratejisi (TR)
## LGS Neural-Koç — Detaylı, pratik ve pilot-öncelikli yaklaşım

En net gerçek: **Şekilli sorularda AI varyant veya yeni soru üretimi tek tip bir işlem olamaz.**  
Doğru ve güvenli yol, şekli bir **asset (varlık)** olarak yönetmek ve her soru için bir **şekil politikası** tanımlayıp bunu Python kural motoruyla zorunlu kılmaktır.

Bu doküman:
- pilotta hız + güvenilirlik,
- ileride ölçeklenebilir şekilli hibrit motor

için uygulanabilir bir çerçeve sunar.

---

## 1) Pilot için en doğru kural (en hızlı + en güvenli)

**Şekilli sorularda otomatik AI varyant üretimini kapat.**

Eğer:

- `has_figure = true`

ise:

- **AI varyant üretimi = KAPALI**
- Sistem **yalnız mevcut havuzdan seçer** (publisher/MEB)
- AI yine de şunları yapabilir:
  - çözüm anlatımı
  - hata analizi
  - mikro ders / konu fişi üretimi

**Pilot DoD mantığı:**  
“Şekilli sorularda soru sabit; kalite riski kontrol altına alınmıştır.”

---

## 2) Şekilli sorular için 3 seviyeli üretim politikası

Bu üç modu sistemde açıkça tanımla:

### Seviye 0 — No-Variant (Varyant Yok)
- Soru havuzdan seçilir ve kullanılır.
- **Asla değiştirilmez.**
- AI sadece açıklama/öğretim destekler.

✅ Pilot default.

---

### Seviye 1 — Text-Only Variant (Şekle dokunma)
Bu seviye sadece şu durumda güvenlidir:
- Şekil **dekoratif** veya
- metinle **sayısal/etiket eşleşmesi gerektirmeyen** bir destek görselidir.

Ne değişebilir?
- hikâye bağlamı
- metin dili
- metindeki sayılar **yalnız şekil ile çelişmeyecekse**

Ne değişemez?
- görselin kendisi

✅ Hızlı  
⚠️ Şekil içinde sayı/etiket varsa genelde yasak.

---

### Seviye 2 — Programatik Yeniden Çizim (Önerilen uzun vadeli model)
Bu seviyede AI **resim üretmez.**  
Bunun yerine **Figure Spec JSON** üretir.

Sonra:

- **Python** bu spesifikasyondan şekli çizer (ör. matplotlib).

En uygun alanlar:
- grafikler
- daire grafikleri
- tablo + grafik kombinasyonları
- basit geometri şemaları

✅ En iyi kalite kontrol  
✅ En otomatiklenebilir alan  
✅ Görsel doğruluğu sende

---

## 3) “AI görsel üretsin mi?”

**Pilot aşamada: hayır.**

Sebep:
- generatif görsellerde:
  - yanlış etiket,
  - yanlış oran/ölçek,
  - metin-görsel çelişkisi

riski yüksektir.

**Doğru pilot paterni:**

- AI ⇒ `figure_spec JSON`
- Python ⇒ `render_figure(figure_spec)`

---

## 4) Minimum veri modeli güncellemesi

`Questions` tablosuna şu alanları ekle:

- `has_figure` *(bool)*
- `figure_type`
  - `chart`
  - `geometry`
  - `schematic`
  - `decorative`
  - `table_graph_combo`
- `figure_policy`
  - `no_variant`
  - `text_only`
  - `programmatic`

**Pilot default eşlemesi:**  
`has_figure=true` ⇒ `figure_policy=no_variant`

---

## 5) Şekil politikasını yarı otomatik belirleme

Gemini’ye küçük bir sınıflandırma görevi ver:

**Input:**
- soru metni + görsel

**Output örneği:**
```json
{
  "has_figure": true,
  "figure_type": "chart",
  "figure_policy_suggestion": "programmatic",
  "reason": "Grafikte sayısal dağılım var; metin değişirse görsel de güncellenmeli."
}
```

**Kural motoru ilkesi:**
- LLM önerir,
- **Python karar verir** (kabul/override).

---

## 6) Figure Spec örnekleri

### Daire grafiği (drone benzeri sorular)
AI çıktısı:

```json
{
  "figure_spec": {
    "type": "pie",
    "labels": ["2 pervaneli", "3 pervaneli", "4 pervaneli"],
    "angles": [80, 120, 160],
    "title": "Pervane Sayısına Göre Dağılım"
  }
}
```

Python bu spec ile yeni grafiği üretir.

---

### Basit geometri/şema
```json
{
  "figure_spec": {
    "type": "geometry",
    "elements": [
      {"shape": "rectangle", "label": "Kutu", "width": 10, "height": 6},
      {"shape": "circle", "label": "Madeni Para", "radius": 1.5}
    ],
    "notes": ["Ölçek temsili olabilir."]
  }
}
```

---

## 7) AI varyant üretimi için sert kurallar

### Kural 1
Eğer:
- `has_figure=true`
- `figure_policy=no_variant`

ise:
- **AI varyantı otomatik RET**

---

### Kural 2
Eğer:
- `figure_policy=text_only`

ise:
- LLM sadece metni yeniden yazar,
- Python şu kontrolü zorunlu yapar:
  - şekil üzerinde **eşleşmesi gereken sayı/etiket** var mı?

Varsa:
- **RET**

---

### Kural 3
Eğer:
- `figure_policy=programmatic`

ise:
- LLM şunları üretmek zorunda:
  - yeni soru metni
  - yeni sayıları
  - `figure_spec`
- Python:
  - yeni görseli render eder
  - yeni soruya `figure_id` bağlar

---

## 8) Pilot için en gerçekçi devreye alma

### Bugün yapılacak en basit uygulama
1) `has_figure` kolonunu ekle.
2) Şekilli soruları etiketle.
3) `figure_policy=no_variant` ata.
4) AI varyant motorunda:
   - `has_figure==true` ise **çık (skip)**.

Bu tek adım riskin çoğunu bitirir.

---

### En hızlı değerli upgrade
Sadece şu tiplerde `programmatic` aç:

- `chart`
- `table_graph_combo`

Çünkü:
- sık çıkar,
- spec ile temiz yönetilir,
- doğrulaması kolaydır.

---

## 9) Senin örnek tiplerine pratik sınıflama

1) **Drone + daire grafiği + fiyat tablosu**  
   - `figure_type=table_graph_combo`  
   - Pilot: `no_variant`  
   - Sonra: **programmatic için ideal**

2) **Asansör şeması**  
   - `figure_type=schematic`  
   - çoğu durumda metin ağırlıklı olduğu için ileride `text_only` denenebilir

3) **Madeni para kutusu görseli**  
   - `schematic/decorative`  
   - ileride `text_only` denenebilir  
   - şekil üzerinde zorunlu sayı/etiket yoksa

---

## 10) Çok önemli sorunun cevabı:
## “Yayınevi sorusunu direkt kullandığımız seçenekte görseli de aynen almak gerekir mi? Bunu yapabilir mi?”

**Evet, kesinlikle söylemelisin.**  
Hatta bunu “LLM’e söylenecek bir rica” değil, **Python’un zorunlu kuralı** yapmalısın.

### Neden?
`publisher` origin’de amaç şudur:
- Soru **metni + görseli + şıkları** ile **tek bir atom** gibi kullanılsın.
- AI görseli “yeniden üretmeye” çalışmasın.
- Metin/görsel tutarsızlığı doğmasın.

### Sistem bunu yapabilir mi?
**Evet, çok kolay.**

Doğru teknik desen:
- Her soruya bir `figure_id` bağla.
- Görsel dosyasını (veya sayfa kırpımını) `assets/figures/` altında sakla.
- `publisher` soru seçildiğinde:
  - aynı `figure_id` aynen referanslanır.
  - görsel **asla değiştirilmez**.

Minimum açıklık kuralı:
- `question_origin = publisher` ise:
  - `figure_policy` otomatik `no_variant`
  - `figure_id` zorunlu (boş olamaz)

### Pilot için pratik kısa çözüm
OCR/görsel parçalama ile uğraşmak istemiyorsan:
- PDF’den ilgili soru sayfasını **görüntü olarak** kaydet.
- Bu görüntüyü “question_image_asset” olarak soruya bağla.
- Böylece derslik kalite kaybı olmadan “aynı görseli kullanma” kuralı sağlanır.

---

## 11) Özet karar

Kilit strateji:

- **Pilot**
  - şekilli sorularda AI varyant yok
  - yayın evi sorusu seçildiyse görsel **aynı asset** olarak kullanılır
- **Sonra**
  - chart türlerinde
    - AI spec üretir
    - Python çizer

Bu yaklaşım:
- hızını düşürmez,
- kaliteyi korur,
- ileride gerçek “şekilli hibrit” motoruna temiz geçiş sağlar.

---

## 12) İstersen IDE’ye tek blok komut olarak

```text
HEDEF:
Şekilli sorular için güvenli hibrit soru davranışı ekle.
Yayın evi sorularında görselin aynen kullanılması zorunlu olsun.
Pilot için AI varyant üretimi şekilli sorularda kapalı kalsın.

SERT KURALLAR:
1) Questions’a has_figure, figure_type, figure_policy, figure_id kolonlarını ekle.
2) Varsayılan: has_figure=true -> figure_policy=no_variant.
3) question_origin=publisher ise figure_id zorunlu ve görsel aynen reuse edilir.
4) AI varyant motoru:
   - figure_policy=no_variant ise otomatik RET.
5) LLM sadece figure_policy önerir; son karar Python’da.
6) Programmatic scope şimdilik sadece chart ve table_graph_combo için tanımlı (opsiyonel MVP).

DOSYALAR:
- app/data_access.py
- app/exam_engine.py
- app/llm_adapter.py
- config/question_mix.yaml
- tests/test_figure_policy.py

GÖREVLER:
1) Questions şemasını genişlet.
2) Publisher soru seçimi akışında figure_id reuse zorunluluğunu uygula.
3) AI varyant üretiminde figure_policy kontrol kapısını ekle.
4) (Opsiyonel) chart için figure_spec kabul edecek altyapı taslağı hazırla.
5) 3 test yaz:
   - publisher + has_figure -> figure_id zorunlu
   - no_variant -> AI varyant bloklanıyor
   - text_only -> numeric sync gerektiren figürde reddediliyor

DoD:
- Şekilli publisher soruları görselsiz kalmıyor.
- Şekilli sorularda kontrolsüz AI varyant üretimi yok.
```
