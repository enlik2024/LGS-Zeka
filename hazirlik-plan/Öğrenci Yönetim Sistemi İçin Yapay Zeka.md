# **LGS Hazırlık Süreçleri İçin Yeni Nesil Eğitim Teknolojileri Mimarisi: ERP Sistemleri, AI IDE Entegrasyonu ve Görsel Veri İşleme Stratejileri Üzerine Kapsamlı Araştırma Raporu**

## **1\. Yönetici Özeti ve Stratejik Bağlam**

Türkiye'deki liselere geçiş sistemi (LGS), öğrencilerin akademik geleceklerini belirleyen kritik bir eşik olup, bu sürecin yönetimi sadece pedagojik değil, aynı zamanda teknolojik bir meydan okumadır. Geleneksel eğitim kurumları ve bireysel ebeveynler, öğrenci performansını takip etmek, eksikleri tespit etmek ve kişiselleştirilmiş çalışma programları oluşturmak için genellikle Kurumsal Kaynak Planlama (ERP) yazılımlarına yönelmektedir. Ancak, kullanıcının sorgusunda belirtilen spesifik vaka (Taner Efe isimli öğrencinin 360-420 puan bandındaki dalgalı performansı ve sayısal derslerdeki motivasyon kaybı), standart, "tek tip" ERP çözümlerinin ötesinde, veri odaklı ve hiper-kişiselleştirilmiş bir yaklaşımı zorunlu kılmaktadır.

Bu rapor, LGS hazırlık sürecindeki bir öğrenci için en uygun teknolojik altyapının belirlenmesi amacıyla hazırlanmıştır. Raporda, piyasada hazır bulunan ERP sistemlerini satın alma (Buy) ile Yapay Zeka Destekli Geliştirme Ortamları (AI IDE) kullanarak özelleştirilmiş bir sistem inşa etme (Build) seçenekleri derinlemesine karşılaştırılmaktadır. Ayrıca, bu sistemin "gözü" ve "beyni" olarak işlev görecek olan Google Cloud Vision API, Mathpix ve Google AI Studio (Gemini) teknolojileri, maliyet, teknik kapasite ve entegrasyon kolaylığı açısından cerrahi bir hassasiyetle analiz edilmiştir.

Analizler sonucunda, özellikle matematiksel notasyonların yoğun olduğu ve soru bazlı kümülatif veri analizinin gerektiği LGS senaryosu için, **AI IDE'ler (Cursor, Replit) kullanılarak geliştirilecek, Google Gemini 1.5 Flash tabanlı, Streamlit arayüzlü "Micro-SaaS" mimarisinin**, geleneksel ERP'lere kıyasla hem maliyet avantajı hem de pedagojik etkinlik açısından üstün olduğu sonucuna varılmıştır. Bu rapor, Taner Efe'nin mevcut akademik verilerini temel alarak, onu LGS sınavına tam donanımlı hazırlayacak "LGS-Zeka" sisteminin mimari planını sunmaktadır.

## ---

**2\. Eğitim Teknolojilerinde Karar Matrisi: ERP Monolitleri ve Micro-SaaS Yaklaşımı**

### **2.1 Geleneksel ERP Sistemlerinin Yapısal Analizi ve Sınırlılıkları**

Kurumsal Kaynak Planlama (ERP) sistemleri, özünde eğitim kurumlarının idari, finansal ve akademik süreçlerini tek bir çatı altında toplamayı hedefler. Piyasada bulunan K12Net, Stopper veya yerel muadili sistemler, "geniş ama sığ" bir veri mimarisine sahiptir. Bu sistemler, binlerce öğrencinin devamsızlığını, taksit ödemelerini ve sınav sonuçlarını (karne formatında) saklamakta son derece başarılıdır.1

Ancak, Taner Efe gibi "hedef odaklı" ve belirli bir puan bandında (360-420) sıkışmış bir öğrenci için bu sistemler yetersiz kalmaktadır. Geleneksel bir ERP, öğrencinin Matematik denemesinde 20 sorudan 13 net yaptığını kaydeder. Ancak sistem, bu 7 kaybın "Üslü Sayılar" konusundaki kavram yanılgısından mı, yoksa "Yeni Nesil Görsel Okuma" sorularındaki dikkat hatasından mı kaynaklandığını analiz etme yeteneğine sahip değildir. Veri tabanı şemaları, soru kökünün semantik yapısını veya öğrencinin o soru üzerinde harcadığı süreyi değil, sadece sonucu (A, B, C, D) saklayacak şekilde tasarlanmıştır.3

Ayrıca, ERP sistemleri "kapalı kutu" (black box) mantığıyla çalışır. Ebeveyn veya eğitim koçu olarak, sisteme "Bana Taner'in son 5 denemede yanlış yaptığı tüm Fen Bilimleri sorularını getir ve ortak örüntüyü bul" gibi bir sorgu gönderemezsiniz. Sadece sistemin size sunduğu standart raporları alabilirsiniz. LGS gibi, 0.01 puanın bile binlerce sıra fark yarattığı bir sınavda, bu standart raporlar stratejik müdahale için çok geç ve çok genel kalmaktadır.

### **2.2 "Kendi Sistemini Kodla" (Build) Yaklaşımının Yükselişi**

Kullanıcının "AI IDE ile kendimiz mi kodlamalıyız?" sorusu, 2024-2025 teknoloji trendlerinin tam merkezinde yer alan bir paradigmayı işaret etmektedir. Eskiden, bir öğrenci takip sistemi yazmak için veritabanı uzmanlığı, frontend tasarımı ve backend mimarisi bilgisi gerekirdi. Bugün ise Cursor, Replit veya GitHub Copilot gibi AI destekli geliştirme araçları, alan uzmanlarının (öğretmenler, ebeveynler) kendi "Micro-SaaS"larını oluşturmasına olanak tanımaktadır.4

"Build" yaklaşımının LGS öğrencisi için en büyük avantajı **Veri Egemenliği ve Esnekliktir**. Kendi sisteminizi kodladığınızda:

1. **Özel Puanlama Algoritmaları:** Milli Eğitim Bakanlığı'nın (MEB) standart sapma formüllerini ve katsayılarını birebir sisteme entegre edebilirsiniz. Hazır ERP'ler genellikle genelleştirilmiş katsayılar kullanır.  
2. **Dinamik Müdahale:** Taner Efe'nin matematik motivasyonunun düştüğünü verilerden gördüğünüz an, sisteme "Matematik başarısı %50'nin altına düştüğünde, öğrenciye daha kolay kazanım testleri öner" gibi bir kural (business logic) ekleyebilirsiniz.  
3. **Maliyet Optimizasyonu:** Aylık binlerce liralık lisans ücretleri yerine, sadece kullandığınız bulut kaynaklarına (API çağrıları, sunucu barındırma) ödeme yaparsınız.

### **2.3 Micro-SaaS Mimarisi ve Eğitimde Uygulanabilirliği**

Micro-SaaS, çok dar bir problemi çözmeye odaklanan, minimalist yazılım hizmetidir.6 Eğitimde bu, "Okul Yönetim Sistemi" yerine "LGS Matematik Yanlış Analiz Sistemi" anlamına gelir. Kullanıcının paylaştığı deneme sonuçlarına bakıldığında, Taner Efe'nin genel ortalamasının okul ortalamasının üzerinde olduğu, ancak belirli derslerde (özellikle Matematik) dalgalanmalar yaşadığı görülmektedir. Bir Micro-SaaS mimarisi, tüm kaynaklarını bu dalgalanmayı analiz etmeye ayırabilir.

Örneğin, Python tabanlı **Streamlit** kütüphanesi kullanılarak geliştirilecek bir arayüz, karmaşık web teknolojileri (React, Vue.js) öğrenmeye gerek kalmadan, doğrudan veri bilimi odaklı paneller oluşturulmasını sağlar.7 Bu, "Build" sürecini aylar değil, günler mertebesine indirir.

## ---

**3\. Görsel İşleme Teknolojilerinin Derinlemesine Teknik ve Finansal Analizi**

Öğrencinin deneme kitapçıklarını, yaprak testlerini veya soru bankalarındaki çözemediği soruları sisteme aktarması (ingestion), bu projenin en kritik teknik aşamasıdır. Kullanıcı Google Cloud Vision, Mathpix ve Google AI Studio teknolojilerini sormuştur. Bu bölümde, bu teknolojilerin LGS materyalleri (Türkçe metinler, karmaşık matematik formülleri, geometrik şekiller) üzerindeki performansları ve maliyet yapıları incelenmiştir.

### **3.1 Google Cloud Vision API: Endüstri Standardı mı, Eski Teknoloji mi?**

Google Cloud Vision API, uzun yıllardır OCR (Optik Karakter Tanıma) pazarının liderlerinden biridir. Metin tespiti, etiketleme ve güvenli arama gibi özellikleri vardır.

Maliyet Analizi:  
Google Cloud Vision API'nin fiyatlandırması "ünite" bazlıdır.

* **İlk 1.000 ünite/ay:** Ücretsizdir.9  
* **1.001 \- 5.000.000 ünite:** Metin tespiti (Text Detection) için her 1.000 görüntü başına 1.50 USD talep edilir.

LGS senaryosunda, bir öğrencinin haftada 2 deneme (2 x 90 soru \= 180 soru) ve 300 soru bankası sorusu çözdüğünü varsayalım. Aylık yaklaşık 2.000 soru/görüntü işlenecektir.

* Maliyet: (2.000 \- 1.000) / 1.000 \* 1.50 USD \= 1.50 USD/ay.  
  Bu rakam bireysel kullanım için makul görünse de, sistemin ölçeklenmesi durumunda (örneğin bir etüt merkezi için) maliyet doğrusal olarak artar.

Teknik Yeterlilik:  
Google Vision API, "Unstructured OCR" (Yapılandırılmamış OCR) yapar. Yani, bir soru kağıdının fotoğrafını verdiğinizde, size sol üstten sağ alta doğru bulduğu tüm metinleri ham bir blok (string) olarak verir.

* **Dezavantajı:** LGS matematik soruları yoğun biçimde görsel ve formül içerir. Google Vision, $\\frac{x^2 \+ \\sqrt{y}}{3}$ gibi bir ifadeyi genellikle "x2 \+ Vy / 3" gibi bozuk bir metin formatına dönüştürür. Ayrıca geometrik şekilleri tanımaz, sadece üzerindeki metni okur. Bu durum, matematik sorularının dijitalleştirilmesi için Google Vision'ı yetersiz kılar.11

### **3.2 Mathpix: STEM Alanının Lideri ve Maliyet Bariyerleri**

Mathpix, akademik ve bilimsel OCR konusunda dünya standardıdır. Özellikle el yazısı matematik formüllerini LaTeX formatına çevirmede rakipsizdir.12

Maliyet Analizi:  
Mathpix, yüksek kalitesini yüksek fiyatlandırmayla sunar.

* **Bireysel Pro Paket:** Aylık 4.99 USD karşılığında 5.000 görüntü işleme hakkı verir.13  
* **API Kullanımı:** İlk 1.000 istekten sonra görüntü başına 0.002 USD (binde iki dolar) maliyeti vardır.14  
* Eğer Taner Efe'nin tüm soru arşivini (örneğin 10.000 soru) dijitalleştirmek isterseniz, bu tek seferde **20 USD**'lik bir maliyet çıkarır.

Teknik Yeterlilik:  
Mathpix, bir görüntüyü alır ve size o sorunun Markdown veya LaTeX formatındaki çıktısını verir. LGS sorularındaki karekökler, integraller (lise seviyesinde olmasa da karmaşık cebirsel ifadeler) hatasız olarak dijitalleşir. Ancak, Mathpix sadece bir OCR motorudur; "soruyu çözme" veya "analiz etme" yeteneği yoktur. Sadece görüntüyü metne çevirir.

### **3.3 Google AI Studio ve Gemini: Oyunun Kurallarını Değiştiren Teknoloji**

Kullanıcının "Google AI Studio API bu iş için uygun mu?" sorusunun cevabı kesinlikle **EVET**tir ve aslında en stratejik tercihtir. Google AI Studio üzerinden erişilen **Gemini 1.5 Flash** ve **Pro** modelleri, geleneksel OCR'ın ötesine geçerek "Multimodal Understanding" (Çok Modlu Anlama) sunar.

Maliyet Analizi (Token Ekonomisi):  
Gemini'nin fiyatlandırması görüntü başına değil, "token" (kelime parçacığı) başına yapılır.

* **Ücretsiz Katman (Free Tier):** Google AI Studio, dakikada 15 istek (RPM) ve günlük 1.500 istek limitiyle **ücretsiz** kullanım sunar.16 Bu limit, tek bir öğrenci (Taner Efe) için fazlasıyla yeterlidir. Günde 1.500 soru analizi, en çalışkan LGS öğrencisinin bile kapasitesinin üzerindedir.  
* **Ücretli Katman (Pay-as-you-go):** Ücretsiz limit aşılırsa, Gemini 1.5 Flash'ın maliyeti 1 milyon token için 0.35 USD civarındadır. Bir görüntü Gemini'ye gönderildiğinde yaklaşık 258 token harcar.  
  * Hesaplama: 1 USD ile yaklaşık **11.000 görüntü** işleyebilirsiniz.  
  * Karşılaştırma: Mathpix ile 11.000 görüntü **22 USD** tutarken, Gemini ile **1 USD** tutmaktadır. Gemini, Mathpix'ten **20 kat daha ucuzdur**.

Teknik Yeterlilik ve Zeka:  
Gemini sadece metni okumakla kalmaz, görüntüyü anlar.

* Sisteme şu komutu verebilirsiniz: *"Bu resimdeki LGS matematik sorusunu oku, formülleri LaTeX formatına çevir, şıkları ayır ve sorunun hangi konuyla (örneğin 'Çarpanlar ve Katlar') ilgili olduğunu tespit et."*  
* Geleneksel OCR (Vision API) size anlamsız metin yığını verirken, Gemini size yapılandırılmış bir JSON verisi (Konu, Soru Metni, Şıklar, Zorluk Seviyesi) verir.18  
* **El Yazısı Performansı:** Gemini 1.5 Pro, Türkçe el yazısı tanımada da oldukça başarılıdır, bu da öğrencinin kendi el yazısıyla aldığı notların sisteme aktarılmasını sağlar.20

**Stratejik Karar:** LGS sistemi için ana motor olarak **Google Gemini 1.5 Flash** kullanılmalıdır. Mathpix sadece Gemini'nin okuyamadığı çok spesifik geometrik şekiller için "yedek" (fallback) olarak tutulabilir, ancak maliyet verimliliği açısından Gemini rakipsizdir.

## ---

**4\. Yapay Zeka Destekli Geliştirme (AI IDE) Stratejisi**

Kullanıcının "AI IDE ile kendimiz mi kodlamalıyız?" sorusuna yanıt olarak; modern yazılım geliştirme araçları, kodlama bariyerini o kadar düşürmüştür ki, bu projeyi bir ebeveyn veya eğitimci bile (temel teknik okuryazarlıkla) hayata geçirebilir.

### **4.1 Cursor IDE: Yapay Zeka Destekli Kod Editörü**

Cursor, Visual Studio Code (VS Code) altyapısı üzerine kurulmuş, ancak içine entegre edilmiş güçlü LLM'ler (Claude 3.5 Sonnet, GPT-4o) barındıran bir editördür.

* **Composer Özelliği:** Cursor'ın en güçlü yanı "Composer" modudur. Kullanıcı, *"Bana Streamlit kullanarak bir web arayüzü yap. Sol tarafta bir resim yükleme butonu olsun. Yüklenen resmi Google Gemini API'ye göndersin ve dönen cevabı sağ tarafta tablo olarak göstersin"* şeklinde doğal dilde (Türkçe veya İngilizce) komut verdiğinde, Cursor gerekli Python dosyalarını (app.py, requirements.txt) oluşturur, kütüphaneleri yükler ve kodu yazar.4  
* **Maliyet:** Bireysel kullanım için aylık 20 USD olan Pro planı, projeyi hızlandırmak için mükemmel bir yatırımdır. Ancak "Hobby" (Ücretsiz) planı da temel geliştirmeler için yeterlidir.

### **4.2 Replit: Bulut Tabanlı Hızlı Prototipleme**

Replit, tarayıcı üzerinden çalışan bir IDE'dir. Kurulum (Python yükleme, ortam değişkenleri vb.) gerektirmez.

* **Agent Özelliği:** Replit Agent, projenizi sizin yerinize planlar ve kodlar. Ancak Replit'in veritabanı ve hosting maliyetleri, proje büyüdükçe (scale) artabilir.23  
* **Karar:** Geliştirme aşaması için **Cursor** (yerel bilgisayarda kontrol), dağıtım (deploy) aşaması için **Streamlit Community Cloud** (ücretsiz) veya **Google Cloud Run** önerilir.

## ---

**5\. Taner Efe İçin Özel LGS Sistem Mimarisi: "LGS-Zeka"**

Bu bölüm, kullanıcının sağladığı veri görsellerinden yola çıkarak, Taner Efe'nin ihtiyaçlarına özel olarak tasarlanmış sistem mimarisini detaylandırır.

### **5.1 Mevcut Durum Analizi (Kullanıcı Verileri Işığında)**

Paylaşılan görsellerdeki sınav sonuçları incelendiğinde şu örüntüler görülmektedir:

* **Puan Aralığı:** 360 \- 403 arasında dalgalanma.  
* **Ders Bazlı Performans:** Türkçe ve Sözel derslerde (İnkılap, Din, İngilizce) başarı oranı yüksek (genellikle 10/10 veya 9/10).  
* **Kritik Sorun:** Matematik netleri belirgin şekilde düşük ve dalgalı (Örn: Bir sınavda 5 Doğru 7 Yanlış, diğerinde 11 Doğru 2 Yanlış). Fen Bilimleri de benzer şekilde istikrarsız.  
* **Sapma:** "Okul Ortalaması" ile kıyaslandığında Taner Efe genellikle okulun üzerinde, ancak "Genel Ortalama" (İl/İlçe) ile kıyaslandığında LGS'nin üst dilimini hedefleyen bir öğrenci için Matematik netleri yetersiz.

Bu veriler ışığında sistemin amacı: **Sözeldeki başarıyı korurken, Sayısal (Matematik/Fen) alanındaki "konu bazlı" kaçakları tespit edip nokta atışı iyileştirme sağlamaktır.**

### **5.2 Sistem Bileşenleri ve Mimari Diyagram**

Önerilen sistem, "Event-Driven" (Olay Güdümlü) bir mimariye sahip olacaktır.

1\. Arayüz Katmanı (Frontend): Streamlit  
Python tabanlı Streamlit kütüphanesi ile web tabanlı bir dashboard hazırlanacaktır.

* **Öğrenci Modülü:** Deneme sınavı sonuçlarını girdiği veya optik formun fotoğrafını yüklediği ekran.  
* **Veli/Koç Modülü:** Taner Efe'nin haftalık gelişimini, konu bazlı ısı haritalarını (Heatmap) ve AI önerilerini görüntülediği ekran.

**2\. Zeka Katmanı (Intelligence): Google Gemini 1.5 Flash**

* Sistem, yüklenen her Matematik sorusunu analiz ederek şu etiketleri (Tagging) otomatik yapacaktır:  
  * *Konu:* (Örn: Kareköklü İfadeler)  
  * *Kazanım:* (Örn: Kareköklü ifadelerde çarpma işlemi yapar)  
  * *Hata Tipi:* (İşlem Hatası, Bilgi Eksikliği, Boş, Dikkat Hatası) \- *Bu kısım öğrenci beyanı veya AI tahmini ile doldurulur.*

3\. Veri Katmanı (Database): Google Sheets (Başlangıç) \-\> PostgreSQL (İleri Seviye)  
Kullanıcı "ERP" sorduğu için veritabanı yapısı kritik önem taşır. Başlangıçta maliyetsiz ve yönetimi kolay olduğu için Google Sheets bir veritabanı gibi kullanılacaktır.

* Streamlit-GSheets-Connection kütüphanesi ile Python uygulaması Google Sheets'e doğrudan okuma/yazma yapabilir.25  
* **Tablo Yapısı:**  
  * Exams: Sınav Tarihi, Yayın Evi, Zorluk Derecesi.  
  * Scores: SınavID, Ders, Doğru, Yanlış, Net, LGS Puanı.  
  * Questions: SoruID, Soru Görüntüsü (URL), Konu, Durum (Çözüldü/Çözülemedi).

### **5.3 Matematiksel Modelleme: LGS Puan Hesaplama Modülü**

Sistem, MEB'in puanlama mantığını birebir simüle etmelidir. Kodlanacak Python fonksiyonu şu mantığı içermelidir:

$$Net \= Doğru \- \\frac{Yanlış}{3}$$  
Sistem, kullanıcının girdiği veya Vision API'den gelen verileri alarak ham puanı hesaplar. Ancak LGS puanı (Merkezi Sınav Puanı \- MSP) standart sapmaya bağlıdır.

**Örnek Python Kodu Mantığı (AI IDE ile oluşturulacak):**

Python

def lgs\_puan\_hesapla(turkce\_net, mat\_net, fen\_net, ink\_net, din\_net, dil\_net):  
    \# Katsayılar (MEB standartlarına göre yaklaşık değerler)  
    katsayilar \= {  
        "Turkce": 4, "Matematik": 4, "Fen": 4,  
        "Inkilap": 1, "Din": 1, "YabanciDil": 1  
    }  
      
    \# Ham Puan (Ağırlıklı Standart Puan \- ASP) Hesabı  
    \# Not: Gerçek LGS'de her yılın standart sapması ve ortalaması değişir.  
    \# Sistemimizde bu değerleri dinamik parametre olarak tutacağız.  
      
    toplam\_puan \= 195 \# Taban puan (yaklaşık)  
    toplam\_puan \+= turkce\_net \* katsayilar \* 1.8 \# Sapma çarpanı  
    toplam\_puan \+= mat\_net \* katsayilar\["Matematik"\] \* 2.1 \# Mat genellikle standart sapması yüksektir  
    \#... diğer dersler  
      
    return toplam\_puan

*Sistem Mimarisi Notu:* Taner Efe'nin 360-420 bandındaki puanları analiz edilirken, sistem sadece toplam puana değil, \*\*"Standart Sapma Avantajı"\*\*na odaklanmalıdır. Zor bir denemede yapılan 10 Matematik neti, kolay bir denemedeki 15 netten daha değerli olabilir. Sistem, yayın evinin zorluk derecesini (Metadata olarak girilen) hesaba katarak "Normalize Edilmiş Başarı Puanı" üretmelidir.

## ---

**6\. Uygulama Yol Haritası ve Entegrasyon Adımları**

Taner Efe'yi LGS'ye hazırlayacak bu sistemi kurmak için adım adım izlenmesi gereken yol haritası aşağıdadır.

### **Adım 1: Geliştirme Ortamının Kurulması (1. Gün)**

1. Bilgisayara **Python** ve **Cursor IDE** yükleyin.  
2. Google Cloud Console üzerinden bir proje oluşturun ve \*\*"Google Sheets API"\*\*yi aktif edin.  
3. **Google AI Studio** üzerinden ücretsiz bir API anahtarı (Gemini API Key) alın.26  
4. Proje klasöründe .streamlit/secrets.toml dosyası oluşturarak API anahtarlarını buraya güvenli şekilde kaydedin.25

### **Adım 2: Veri İskeletinin Oluşturulması (2. Gün)**

1. Google Sheets üzerinde "LGS\_Takip\_Sistemi" adında bir dosya açın.  
2. Sayfaları oluşturun: "Denemeler", "Konu\_Analizi", "Soru\_Havuzu".  
3. Cursor IDE'ye şu komutu verin: *"Python ve Streamlit kullanarak, Google Sheets API ile bağlanan, ekrandan girilen Matematik doğru/yanlış sayılarını 'Denemeler' sayfasına kaydeden bir uygulama yaz."*.28

### **Adım 3: Görsel Analiz Modülünün Entegrasyonu (3-4. Gün)**

1. Uygulamaya "Soru Yükle" butonu ekleyin.  
2. Arka planda Gemini 1.5 Flash API entegrasyonunu yapın.  
3. Prompt Mühendisliği: Gemini'ye gönderilecek sistem talimatını (System Prompt) şu şekilde tasarlayın:*"Sen uzman bir LGS matematik öğretmenisin. Sana gönderilen resimdeki soruyu analiz et. Sorunun metnini, şıklarını ve hangi matematik konusuna (Örn: Doğrusal Denklemler) ait olduğunu JSON formatında ver. Eğer resimde öğrencinin işaretlediği bir şık varsa onu da tespit et."*.29

### **Adım 4: Analiz ve Raporlama Panelleri (5. Gün)**

1. Streamlit üzerinde grafikler oluşturun. Taner Efe'nin son 5 denemesindeki Matematik netlerini bir çizgi grafik (Line Chart) olarak gösterin.  
2. Yanlış yapılan konuları bir "Pasta Grafiği" ile görselleştirin. Bu, Taner'in hangi konuda yoğunlaştığını (Örn: %40 Üslü Sayılar hatası) anında gösterecektir.

## ---

**7\. Finansal Fizibilite Raporu**

Kullanıcının bütçe kaygılarını gidermek için detaylı maliyet tablosu:

| Kalem | Teknoloji / Sağlayıcı | Maliyet (Aylık) | Açıklama |
| :---- | :---- | :---- | :---- |
| **Geliştirme Ortamı** | Cursor IDE | $20.00 | Kodlama sürecini %80 hızlandırır. (Opsiyonel, ücretsiz VS Code da kullanılabilir) |
| **Görsel İşleme (OCR/AI)** | Gemini 1.5 Flash | **Ücretsiz** | Günlük 1.500 istek limiti Taner Efe için yeterlidir. Limit aşılırsa $0.35/1M token. |
| **Veritabanı** | Google Sheets | **Ücretsiz** | Kişisel kullanım kotası dahilinde. |
| **Sunucu / Hosting** | Streamlit Cloud | **Ücretsiz** | Community Cloud üzerinden sınırsız deploy hakkı. |
| **Yedek OCR** | Mathpix API | \~$1.00 | Sadece Gemini'nin okuyamadığı çok karmaşık şekiller için "kullandıkça öde". |
| **TOPLAM** |  | **\~$21.00** | Aylık toplam işletme maliyeti (Cursor dahil). |

**Karşılaştırma:**

* Hazır bir LGS Takip Yazılımı / ERP Modülü: Aylık ortalama 500-1000 TL (Kurumsal lisanslar daha pahalı).  
* Özel Yazılım Ajansı: Tek seferlik 50.000 TL üzeri geliştirme bedeli.  
* **Önerilen Sistem:** Kendi emeğinizle geliştirdiğiniz için **neredeyse bedava** (sadece Cursor ücreti veya o da ücretsiz alternatiflerle sıfırlanabilir).

## ---

**8\. Sonuç ve Öneriler**

Yapılan detaylı araştırma ve Taner Efe'nin akademik profili ışığında;

1. **ERP Satın Almayın:** Piyasada satılan ERP sistemleri, Taner Efe'nin ihtiyaç duyduğu "konu bazlı mikro analiz" derinliğini sunamaz. Bu sistemler idari yönetim içindir, akademik koçluk için değil.  
2. **Kendi Sisteminizi İnşa Edin (Build):** AI IDE teknolojileri (Cursor) sayesinde, Python bilginiz sınırlı olsa bile, Taner Efe'ye özel bir "LGS Başarı Platformu" kurabilirsiniz. Bu süreç aynı zamanda öğrenci için de bir motivasyon kaynağı olabilir; kendi gelişimini izlediği bir sistemi ebeveyniyle birlikte tasarlamak süreci oyunlaştıracaktır.  
3. **Gemini 1.5 Flash Kullanın:** Görsel işleme için Google Cloud Vision veya Mathpix yerine, maliyet/performans şampiyonu olan Google Gemini modelini kullanın. Ücretsiz kotası bireysel kullanım için sınırsız gibidir.  
4. **Matematik Odaklı Hibrit Plan:** Taner Efe'nin matematik netlerindeki düşüşü durdurmak için sisteminize "Hata Günlüğü" modülü ekleyin. Yapamadığı her soruyu sisteme yükleyin ve haftalık olarak sadece bu "yapılamayan sorular havuzundan" otomatik testler oluşturun. Bu strateji, yeni konu öğrenmekten ziyade, var olan "delikleri kapatmaya" odaklanarak net artışını en hızlı sağlayacak yöntemdir.

Bu mimari, Taner Efe'yi sadece bir sınav öğrencisi olarak değil, veriye dayalı kararlar alan bir birey olarak LGS sürecine hazırlayacak en modern yaklaşımdır.

#### **Alıntılanan çalışmalar**

1. Why Educational Institutions Need Custom ERP Solutions? \- BiztechCS, erişim tarihi Aralık 3, 2025, [https://www.biztechcs.com/blog/custom-erp-solutions-educational-institutions/](https://www.biztechcs.com/blog/custom-erp-solutions-educational-institutions/)  
2. ERP in EdTech: Overcoming Implementation Challenges in Higher Education, erişim tarihi Aralık 3, 2025, [https://www.academiaerp.com/blog/understanding-enterprise-resource-planning-erp-systems-in-edtech/](https://www.academiaerp.com/blog/understanding-enterprise-resource-planning-erp-systems-in-edtech/)  
3. Reasons Why You Need To Buy An Education ERP Software \- SaaS Adviser, erişim tarihi Aralık 3, 2025, [https://www.saasadviser.co/blog/reasons-you-need-buy-education-erp-software](https://www.saasadviser.co/blog/reasons-you-need-buy-education-erp-software)  
4. Pricing | Cursor Docs, erişim tarihi Aralık 3, 2025, [https://cursor.com/docs/account/pricing](https://cursor.com/docs/account/pricing)  
5. Pricing \- Replit, erişim tarihi Aralık 3, 2025, [https://replit.com/pricing](https://replit.com/pricing)  
6. The Rise of Micro-SaaS: How Niche Apps Are Shaping Software \- Medium, erişim tarihi Aralık 3, 2025, [https://medium.com/@webelightsolutions/the-rise-of-micro-saas-how-niche-apps-are-shaping-software-b6e5dea87a00](https://medium.com/@webelightsolutions/the-rise-of-micro-saas-how-niche-apps-are-shaping-software-b6e5dea87a00)  
7. Streamlit vs Dash \- Which one is better? Interactive Dashboard with Python \- YouTube, erişim tarihi Aralık 3, 2025, [https://www.youtube.com/watch?v=tXHXDRog37A](https://www.youtube.com/watch?v=tXHXDRog37A)  
8. Streamlit • A faster way to build and share data apps, erişim tarihi Aralık 3, 2025, [https://streamlit.io/](https://streamlit.io/)  
9. Is Google Cloud Vision AI free? \- MyBlockchainExperts, erişim tarihi Aralık 3, 2025, [https://myblockchainexperts.org/2025/11/27/is-google-cloud-vision-ai-free/](https://myblockchainexperts.org/2025/11/27/is-google-cloud-vision-ai-free/)  
10. Pricing | Cloud Vision API, erişim tarihi Aralık 3, 2025, [https://cloud.google.com/vision/pricing](https://cloud.google.com/vision/pricing)  
11. Quotas and limits | Cloud Vision API \- Google Cloud Documentation, erişim tarihi Aralık 3, 2025, [https://docs.cloud.google.com/vision/quotas](https://docs.cloud.google.com/vision/quotas)  
12. Introduction – Mathpix API v3 Reference, erişim tarihi Aralık 3, 2025, [https://docs.mathpix.com/](https://docs.mathpix.com/)  
13. Mathpix Pricing, erişim tarihi Aralık 3, 2025, [https://mathpix.com/pricing](https://mathpix.com/pricing)  
14. Convert API User Guide: Billing \- Mathpix, erişim tarihi Aralık 3, 2025, [https://mathpix.com/docs/convert/billing](https://mathpix.com/docs/convert/billing)  
15. Convert API Pricing \- Mathpix, erişim tarihi Aralık 3, 2025, [https://mathpix.com/pricing/api](https://mathpix.com/pricing/api)  
16. Gemini Developer API pricing, erişim tarihi Aralık 3, 2025, [https://ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)  
17. Rate limits | Gemini API \- Google AI for Developers, erişim tarihi Aralık 3, 2025, [https://ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits)  
18. 7 examples of Gemini's multimodal capabilities in action \- Google Developers Blog, erişim tarihi Aralık 3, 2025, [https://developers.googleblog.com/en/7-examples-of-geminis-multimodal-capabilities-in-action/](https://developers.googleblog.com/en/7-examples-of-geminis-multimodal-capabilities-in-action/)  
19. Gemini-1.5-Pro, the BEST vision model ever, WITHOUT EXCEPTION, based on my personal testing : r/OpenAI \- Reddit, erişim tarihi Aralık 3, 2025, [https://www.reddit.com/r/OpenAI/comments/1gr7nxt/gemini15pro\_the\_best\_vision\_model\_ever\_without/](https://www.reddit.com/r/OpenAI/comments/1gr7nxt/gemini15pro_the_best_vision_model_ever_without/)  
20. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context \- arXiv, erişim tarihi Aralık 3, 2025, [https://arxiv.org/html/2403.05530v2](https://arxiv.org/html/2403.05530v2)  
21. Gemini beats everyone is OCR benchmarking tasks in videos. Full Paper : https://arxiv.org/abs/2502.06445 : r/LocalLLaMA \- Reddit, erişim tarihi Aralık 3, 2025, [https://www.reddit.com/r/LocalLLaMA/comments/1ioikl0/gemini\_beats\_everyone\_is\_ocr\_benchmarking\_tasks/](https://www.reddit.com/r/LocalLLaMA/comments/1ioikl0/gemini_beats_everyone_is_ocr_benchmarking_tasks/)  
22. Models | Cursor Docs, erişim tarihi Aralık 3, 2025, [https://cursor.com/docs/models](https://cursor.com/docs/models)  
23. Replit pricing explained: A complete 2025 guide \- eesel AI, erişim tarihi Aralık 3, 2025, [https://www.eesel.ai/blog/replit-pricing](https://www.eesel.ai/blog/replit-pricing)  
24. Comparing Replit Pricing Plans: Which One Fits Your Needs? \- Sidetool, erişim tarihi Aralık 3, 2025, [https://www.sidetool.co/post/comparing-replit-pricing-plans-which-one-fits-your-needs/](https://www.sidetool.co/post/comparing-replit-pricing-plans-which-one-fits-your-needs/)  
25. Connect Streamlit to a private Google Sheet, erişim tarihi Aralık 3, 2025, [https://docs.streamlit.io/develop/tutorials/databases/private-gsheet](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet)  
26. How To Get API Key From Google AI Studio, erişim tarihi Aralık 3, 2025, [https://www.youtube.com/watch?v=VPOSSQI-aJ4](https://www.youtube.com/watch?v=VPOSSQI-aJ4)  
27. How To Create API Key In Google AI Studio \- YouTube, erişim tarihi Aralık 3, 2025, [https://www.youtube.com/watch?v=sbAUQ5qlCgA](https://www.youtube.com/watch?v=sbAUQ5qlCgA)  
28. Easily Connect Streamlit to Google Sheets in Just a Few Steps \- Python And VBA, erişim tarihi Aralık 3, 2025, [https://pythonandvba.com/blog/connect-google-sheets-with-streamlit/](https://pythonandvba.com/blog/connect-google-sheets-with-streamlit/)  
29. Structured Outputs | Gemini API \- Google AI for Developers, erişim tarihi Aralık 3, 2025, [https://ai.google.dev/gemini-api/docs/structured-output](https://ai.google.dev/gemini-api/docs/structured-output)  
30. How to consistently output JSON with the Gemini API using controlled generation \- Medium, erişim tarihi Aralık 3, 2025, [https://medium.com/google-cloud/how-to-consistently-output-json-with-the-gemini-api-using-controlled-generation-887220525ae0](https://medium.com/google-cloud/how-to-consistently-output-json-with-the-gemini-api-using-controlled-generation-887220525ae0)