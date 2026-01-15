# **LGS-Zeka: Eğitim Teknolojilerinde Ölçeklenebilir Mimari, Teknik Fizibilite ve Yapay Zeka Destekli Geliştirme Stratejisi Raporu**

## **1\. Yönetici Özeti ve Stratejik Vizyon**

Eğitim teknolojileri (EdTech) sektörü, veri yoğunluklu analizler ve kişiselleştirilmiş öğrenme deneyimleri ekseninde radikal bir dönüşüm geçirmektedir. "LGS-Zeka" projesi, Türkiye'deki Liselere Geçiş Sistemi (LGS) sınavına hazırlanan öğrenciler için kritik bir boşluğu doldurmayı hedefleyen, veriye dayalı bir performans takip ve yapay zeka destekli rehberlik sistemidir. Bu rapor, projenin teknik altyapısının belirlenmesi sürecinde gerçekleştirilen kapsamlı bir mimari analiz çalışmasını ve sistemin hayata geçirilmesi için gerekli olan uygulama yol haritasını sunmaktadır.

Analizin temel odak noktası, modern yazılım geliştirme dünyasında sıklıkla karşılaştırılan iki ana paradigma üzerinedir: No-Code/Low-Code (NCLC) platformlar (Glide, Bubble, AppSheet vb.) ve Python tabanlı özel yazılım geliştirme (Custom Development) ekosistemi. Yapılan çok boyutlu değerlendirmeler—ki bu değerlendirmeler veri ölçeklenebilirliği, algoritmik esneklik, maliyet projeksiyonları ve entegrasyon yeteneklerini kapsamaktadır—Python ekosisteminin LGS-Zeka projesi için tek sürdürülebilir ve stratejik seçenek olduğunu ortaya koymaktadır. Özellikle LGS puanlama sisteminin içerdiği ağırlıklı katsayılar, standart sapma hesaplamaları ve zaman serisi analizleri, No-Code platformların sunduğu basit mantıksal operatörlerin ötesinde bir hesaplama gücü gerektirmektedir.1

Raporun ilerleyen bölümlerinde, No-Code platformların özellikle veri satır limitleri ve API çağrı kısıtlamaları nedeniyle eğitim verisi analitiğinde nasıl bir darboğaz yarattığı detaylandırılmıştır.4 Buna karşılık, Python'un zengin kütüphane desteği (Pandas, Streamlit, Google Generative AI SDK), projenin temel değer önerisi olan "el yazısı matematik sorularının analizi" ve "kişiselleştirilmiş geri bildirim" özelliklerinin hayata geçirilmesinde kritik bir rol oynamaktadır. Gemini 1.5 Pro ve Flash modellerinin Python ortamında sunduğu multimodal (çok modlu) yetenekler, maliyet etkinliği ve yüksek doğruluk oranıyla rakiplerinden ayrışmaktadır.7

Raporun ikinci yarısı, bu teknik mimariyi hayata geçirmek için yenilikçi bir geliştirme metodolojisi sunmaktadır: Yapay Zeka Destekli IDE'ler (Cursor ve Windsurf) ile "Prompt Mühendisliği". Geleneksel kod yazım süreçlerini hızlandıran ve teknik borcu minimize eden bu yaklaşım için, veritabanı bağlantısından dashboard tasarımına, OCR entegrasyonundan hata yönetimine kadar projenin her aşamasını kapsayan detaylı komut setleri (promptlar) hazırlanmıştır. Bu promptlar, geliştiricinin sadece "ne" yapılacağını değil, "nasıl" yapılacağını da yapay zekaya dikte etmesini sağlayarak, projenin endüstri standartlarında (PEP-8 uyumlu, modüler, güvenli) inşa edilmesini garanti altına almaktadır.

## **2\. Mimari Karar Matrisi: Python vs. No-Code Platformlar**

LGS-Zeka projesinin başarısı, seçilen teknoloji yığınının (tech stack) projenin mevcut ihtiyaçlarını karşılarken gelecekteki büyüme potansiyeline de uyum sağlayabilmesine bağlıdır. Bu bağlamda, Python ve No-Code platformlar dört kritik eksende karşılaştırılmıştır.

### **2.1. Veri Hacmi, Yönetimi ve Ölçeklenebilirlik Analizi**

Eğitim verisi, doğası gereği kümülatif ve yüksek hacimlidir. Bir LGS öğrencisinin akademik yılı boyunca ürettiği veri noktaları, basit bir veritabanı yapısının ötesine geçer. Öğrencinin çözdüğü her soru, deneme sınavı sonuçları, konu bazlı başarı oranları, çalışma süreleri ve sisteme yüklenen soru görselleri, sürekli büyüyen bir veri seti oluşturur.

No-Code Platformların Yapısal Sınırları:  
Glide, Bubble ve AppSheet gibi platformlar, veri tutma kapasiteleri konusunda katı sınırlara sahiptir. Örneğin, Glide'ın ücretsiz planında 25.000 satır limiti bulunurken, kurumsal planlarda dahi bu limit genellikle 1 milyon satırın altındadır veya çok yüksek maliyetler gerektirir.4 AppSheet'in temel planlarında veritabanı başına satır limiti 2.500 ile 10.000 arasında değişmektedir.5  
Bir senaryo analizi yapıldığında:

* Bir öğrenci günde ortalama 50 soru çözmektedir.  
* Her soru için sistemde; Tarih, Ders, Konu, Doğru/Yanlış Durumu, Çözüm Süresi gibi en az 5 veri alanı tutulmaktadır.  
* 1000 öğrencili bir pilot çalışmada, sadece soru takip verisi ayda 1.5 milyon satıra (1000 öğrenci x 50 soru x 30 gün) ulaşmaktadır.

Bu hacimdeki bir veri akışı, No-Code platformların veritabanı motorlarını (genellikle Google Sheets veya basit SQL sarmalayıcıları) kilitleyecektir. Ayrıca, Glide gibi araçlar veriyi genellikle kullanıcının cihazına (client-side) yükleyerek işler. Milyonlarca satırlık bir veri setinin tarayıcıda işlenmeye çalışılması, sistemin kullanılamaz hale gelmesine (latency) ve çökmesine neden olur.6

Python'un Mimarisi ve Veri Gücü:  
Python mimarisinde, veritabanı katmanı uygulama katmanından tamamen bağımsızdır. PostgreSQL gibi endüstri standardı ilişkisel veritabanları (Supabase, NeonDB veya AWS RDS üzerinde) kullanıldığında, milyarlarca satırlık veri üzerinde milisaniyeler mertebesinde sorgulama yapılabilir.  
Python'un veri işleme kütüphanesi Pandas, büyük veri setlerini bellekte (in-memory) işleyerek karmaşık filtreleme, gruplama ve istatistiksel analiz işlemlerini saniyeler içinde gerçekleştirir.1 Örneğin, "Tüm öğrencilerin son 3 aydaki 'Kareköklü İfadeler' konusundaki başarı ortalamasının değişimi" gibi bir sorgu, Python'da tek satırlık bir vektörel işlemken, No-Code platformlarda karmaşık ve yavaş döngüler gerektiren bir işlemdir. Ayrıca, Python ekosistemi, verinin büyümesi durumunda Dask veya PySpark gibi dağıtık hesaplama araçlarına geçiş imkanı sunarak sınırsız bir ölçeklenebilirlik sağlar.11

### **2.2. Algoritmik Karmaşıklık: LGS Puanlama ve Adaptif Öğrenme**

LGS puan hesaplama sistemi, doğrusal olmayan ve dinamik parametrelere dayalı bir matematiksel modeldir. Her dersin (Türkçe, Matematik, Fen Bilimleri, T.C. İnkılap Tarihi, Din Kültürü, Yabancı Dil) katsayısı farklıdır. Daha önemlisi, puan hesaplamasında kullanılan "Standart Sapma" ve "Türkiye Geneli Ortalaması" gibi değerler her yıl değişmektedir.

LGS Puan Hesaplama Formülü ve No-Code Yetersizliği:  
Ham Puan (HP) hesaplaması:

$$HP \= (Doğru Sayısı) \- \\frac{Yanlış Sayısı}{3}$$  
Standart Puan (SP) hesaplaması ise çok daha komplekstir:

$$SP\_i \= 10 \\times \\frac{HP\_i \- Ort\_i}{Std\_i} \+ 50$$

(Burada $i$ dersi, $Ort$ Türkiye ortalamasını, $Std$ standart sapmayı temsil eder.)  
Sonuç olarak Ağırlıklı Standart Puan (ASP) ve Toplam Puan hesaplanır. Bu hesaplamalar, iç içe geçmiş matematiksel fonksiyonlar ve kayan noktalı sayı (floating point) hassasiyeti gerektirir.

No-Code platformlar, basit "Eğer-İse" (If-Then) mantığı ve temel aritmetik işlemler üzerine kuruludur.3 Karmaşık matematiksel modelleri görsel bloklarla (drag-and-drop) oluşturmaya çalışmak, "spagetti kod" olarak adlandırılan, takip edilmesi ve hatası ayıklanması (debug) imkansız yapılar ortaya çıkarır.12 Ayrıca, No-Code araçlarında, öğrencinin geçmiş performansına bakarak "Senin matematik netin düşük, şu konuya çalışmalısın" diyen bir Tavsiye Algoritması (Recommendation Engine) geliştirmek, platformun yeteneklerini aşan bir işlemdir.

Python'un Analitik Üstünlüğü:  
Python, bilimsel hesaplama (Scientific Computing) alanında dünya lideridir. NumPy kütüphanesi, yukarıdaki karmaşık formülleri matris işlemleri olarak son derece hızlı bir şekilde çözer.

* **Dinamik Parametre Yönetimi:** MEB tarafından katsayılarda bir değişiklik yapıldığında, Python kodunda sadece bir değişkeni güncellemek yeterlidir.  
* **Makine Öğrenmesi (ML) Entegrasyonu:** LGS-Zeka projesinin vizyonunda yer alan "Tahminleme" (Prediction) özelliği için Python vazgeçilmezdir. Scikit-learn veya XGBoost kütüphaneleri kullanılarak, öğrencinin mevcut performansına göre sene sonu LGS puanı %95+ doğrulukla tahmin edilebilir.13 No-Code platformlarda makine öğrenmesi modellerini eğitmek ve çalıştırmak yerel olarak mümkün değildir; mutlaka harici bir servise bağımlılık gerektirir.

### **2.3. Finansal Modelleme: Maliyet Yapısı ve "Vendor Lock-In" Riski**

Proje geliştirme sürecinde maliyetler, "Geliştirme Maliyeti" (CapEx) ve "İşletme Maliyeti" (OpEx) olarak ikiye ayrılır. No-Code platformlar düşük geliştirme maliyeti vaat etse de, uzun vadeli işletme maliyetleri ve gizli riskler barındırır.

**Maliyet Karşılaştırma Tablosu:**

| Maliyet Kalemi | No-Code (Glide / Bubble) | Python (Streamlit \+ Cloud) |
| :---- | :---- | :---- |
| **Lisanslama** | Kullanıcı/Uygulama başına aylık ödeme ($25 \- $500+).15 Kullanıcı sayısı arttıkça maliyet katlanarak artar. | Açık kaynak (Ücretsiz). Sadece sunucu ve API kullanımı ödenir. |
| **Veri Depolama** | Ekstra satır ve depolama alanı için fahiş fiyatlar talep edilir. | PostgreSQL maliyeti çok düşüktür (Örn: Supabase Free Tier 500MB, sonrası GB başına sentler). |
| **API ve Entegrasyon** | Harici API (Gemini vb.) bağlantıları için üst paketlere geçiş zorunluluğu.4 | API çağrıları kod içinde ücretsizdir, sadece API sağlayıcısına (Google) ödeme yapılır. |
| **Ölçekleme Maliyeti** | Platformun belirlediği "Tier" (Kademe) atlamaları maliyeti sıçratır. | Sunucu kaynakları (CPU/RAM) ihtiyaca göre doğrusal olarak artırılabilir. |

Vendor Lock-In (Sağlayıcı Bağımlılığı) Tehlikesi:  
No-Code platformların en büyük riski, projenin mülkiyetinin platforma bağımlı olmasıdır. Glide veya Bubble üzerinde geliştirilen bir uygulamanın kaynak kodunu alıp başka bir sunucuya taşımak teknik olarak mümkün değildir.12 Platform kapandığında, fiyat politikasını değiştirdiğinde veya teknik bir sorun yaşadığında, tüm proje risk altındadır.  
Python ile geliştirilen LGS-Zeka projesi ise %100 taşınabilirdir. Kodlar GitHub üzerinde saklanır ve Docker konteynerleri sayesinde Google Cloud, AWS, Azure veya yerel bir sunucu üzerinde herhangi bir değişiklik yapmadan çalıştırılabilir. Bu, projenin teknik egemenliğinin (technical sovereignty) tamamen geliştirici ekipte olmasını sağlar.

### **2.4. Yapay Zeka (AI) ve Vision Entegrasyonu: Neden Python Şart?**

LGS-Zeka projesinin "amiral gemisi" özelliği, öğrencilerin çözemedikleri soruların fotoğrafını çekip sisteme yüklemeleri ve yapay zekanın bu soruyu metne döküp (OCR) çözüm yolunu anlatmasıdır. Bu süreç, multimodal (görüntü ve metin işleyen) yapay zeka modellerinin derinlemesine entegrasyonunu gerektirir.

No-Code Platformlarda AI Entegrasyonu:  
No-Code araçlarında AI entegrasyonu genellikle "hazır bloklar" veya Zapier/Make gibi otomasyon araçları üzerinden yapılır.

* **Gecikme (Latency):** Bir fotoğrafın Glide'dan Zapier'e, oradan OpenAI/Gemini'ye gitmesi ve cevabın geri dönmesi ciddi bir zaman kaybı yaratır.  
* **Maliyet:** Her bir adım (Glide \-\> Zapier \-\> AI) ayrı bir işlem ücreti doğurur.  
* **Kalite Sorunu:** Standart OCR araçları (Google Vision API vb.), matematiksel formülleri (kesirler, kökler, integraller) tanımada başarısız olabilir veya sadece düz metin olarak döndürebilir.18 Matematiksel ifadelerin LaTeX formatında hatasız alınması, eğitim kalitesi için kritiktir.

Python ve Gemini 1.5 Pro/Flash:  
Python, yapay zeka geliştirmesinin ana dilidir. Google'ın sunduğu google-generativeai SDK'sı sayesinde, Gemini 1.5 modellerine doğrudan erişim sağlanır.19

* **Yerel (Native) Entegrasyon:** Görüntü işleme, boyutlandırma ve formatlama işlemleri Python içinde yapılır ve doğrudan API'ye gönderilir. Aracı yoktur, gecikme minimumdur.  
* **Gelişmiş Vision Yetenekleri:** Gemini 1.5 Pro, el yazısı matematik sorularını okuma ve çözme konusunda rakiplerine (GPT-4o, Claude 3.5 Sonnet) göre daha yüksek performans göstermektedir.8 Özellikle el yazısının karmaşıklığı ve matematiksel sembollerin yoğunluğu düşünüldüğünde, Python üzerinden yapılan ince ayarlar (temperature, top\_k parametreleri) modelin başarısını artırır.  
* **Maliyet Avantajı:** Gemini 1.5 Flash modeli, ücretsiz katmanında (Free Tier) dakikada 15 isteğe (RPM) ve günde 1.500 isteğe kadar ücretsiz kullanım sunmaktadır.7 Bu, projenin başlangıç aşamasında AI maliyetini sıfırlayan devasa bir avantajdır. No-Code platformlar ise kendi "AI Kredileri" üzerinden fahiş fiyatlandırmalar yapmaktadır.

## ---

**3\. Derinlemesine Teknik Analiz: LGS-Zeka Sistemi Gereksinimleri**

LGS-Zeka sisteminin teknik başarısı, sadece doğru araçların seçilmesiyle değil, bu araçların nasıl bir mimari içinde kurgulandığıyla ilgilidir. Bu bölümde, sistemin fonksiyonel gereksinimlerinin teknik karşılıkları detaylandırılmıştır.

### **3.1. Fonksiyonel Gereksinimler ve Teknik Karşılıkları**

| Gereksinim | Teknik Çözüm (Python Stack) | Açıklama |
| :---- | :---- | :---- |
| **Kullanıcı Arayüzü (UI)** | **Streamlit** | Veri odaklı, hızlı, mobil uyumlu ve Python ile %100 entegre arayüz. React/Vue öğrenme maliyetini ortadan kaldırır. |
| **Veri Tabanı** | **PostgreSQL (Supabase)** | İlişkisel veri yapısı (Öğrenci \-\> Deneme \-\> Sorular). JSONB desteği ile esnek soru verisi saklama imkanı. |
| **Kimlik Doğrulama** | **Supabase Auth** | Güvenli, e-posta/şifre veya OAuth (Google Login) girişi. KVKK uyumlu kullanıcı yönetimi. |
| **OCR & Soru Analizi** | **Gemini 1.5 Flash/Pro** | Görüntüden metne (Image-to-Text) ve çözüme giden yol. JSON formatında yapılandırılmış çıktı.22 |
| **Raporlama** | **Plotly & Altair** | İnteraktif grafikler. Öğrencinin üzerine gelip detay görebildiği (hover) performans analizleri. |

### **3.2. Veri Güvenliği ve KVKK Uyumu**

Öğrenci verileri (isim, okul, akademik başarı) Kişisel Verilerin Korunması Kanunu (KVKK) kapsamında "hassas veri" niteliği taşıyabilir.

* **Python/Supabase Çözümü:** Supabase, *Row Level Security* (RLS) özelliği sunar. Bu, veritabanı seviyesinde bir güvenlik kuralıdır: "Bir öğrenci sadece kendi verisini görebilir." No-Code platformlarda bu tür granüler güvenlik kurallarını uygulamak zordur ve genellikle uygulama katmanında (güvensiz) çözülmeye çalışılır.10  
* **Veri Şifreleme:** Python kütüphaneleri (örn: cryptography) ile kritik veriler veritabanına yazılmadan önce şifrelenebilir.

### **3.3. Performans Beklentileri ve Limitler**

Sistemin hedeflenen performans metrikleri şöyledir:

* **Dashboard Yüklenme Süresi:** \< 2 saniye (Streamlit st.cache\_data ile optimize edilmiş).  
* **Soru Analiz Süresi:** \< 5 saniye (Gemini 1.5 Flash API yanıt süresi).  
* **Eşzamanlı Kullanıcı:** Başlangıçta 100+, ölçeklendiğinde 10.000+. Streamlit Cloud veya Google Cloud Run üzerinde "Auto-scaling" ile bu yük karşılanabilir. No-Code platformlar ise 100 eşzamanlı kullanıcıda bile performans sorunları yaşatmaktadır.23

## ---

**4\. Uygulama Mimarisi ve Teknoloji Yığını**

LGS-Zeka projesi için önerilen nihai teknoloji yığını (Tech Stack) aşağıdadır. Bu yapı, hem maliyet etkinliği hem de yüksek performans için optimize edilmiştir.

### **4.1. Backend ve Frontend: Streamlit**

Streamlit, Python scriptlerini dakikalar içinde interaktif web uygulamalarına dönüştüren açık kaynaklı bir framework'tür. LGS-Zeka için neden idealdir?

* **Tek Dil:** Hem backend hem frontend Python ile yazılır. Javascript, HTML veya CSS bilmeye gerek yoktur.25  
* **Hızlı İterasyon:** Yeni bir özellik (örn: yeni bir grafik) eklemek sadece birkaç satır kod gerektirir.  
* **State Management:** st.session\_state ile öğrencinin oturum bilgileri, filtre seçimleri ve sohbet geçmişi kolayca yönetilir.

### **4.2. Veritabanı Katmanı: Supabase (PostgreSQL)**

Google Sheets prototipleme için harika olsa da, 1000 öğrenci hedefi için bir ilişkisel veritabanı şarttır. Supabase, "Firebase'in açık kaynaklı alternatifi" olarak bilinir ve PostgreSQL'in gücünü modern bir API ile sunar.

* **Python Kütüphanesi:** supabase-py ile Python içinden veritabanına bağlanmak, veri eklemek ve çekmek son derece basittir.  
* **Realtime:** Veritabanındaki değişiklikleri (örn: yeni bir deneme sonucu) anlık olarak arayüze yansıtma yeteneği vardır.

### **4.3. Yapay Zeka Katmanı: Google Gemini API**

Projenin beyni Gemini 1.5 modelleridir.

* **Gemini 1.5 Flash:** Hız ve maliyet odaklı. Soru analizi, konu sınıflandırma ve basit sohbetler için kullanılır. Milyon token başına maliyeti çok düşüktür.7  
* **Gemini 1.5 Pro:** Karmaşık muhakeme (Reasoning) ve zor matematik soruları için kullanılır. Pahalıdır ancak doğruluğu yüksektir. Sistem, sorunun zorluğuna göre dinamik olarak model seçimi yapabilir.

## ---

**5\. Yapay Zeka Destekli Geliştirme Kılavuzu: Cursor ve Windsurf için Master Prompt Setleri**

Bu bölüm, projeyi modern AI destekli IDE'ler (Cursor, Windsurf) kullanarak inşa etmek isteyen geliştiriciler için hazırlanmış kapsamlı bir rehberdir. Bu promptlar, basit kod üretim komutları değil, projenin mimarisini, stilini ve güvenlik kurallarını yapay zekaya dikte eden "Sistem Mühendisliği" talimatlarıdır.

Kullanım Stratejisi:

1. **Cursor:** .cursorrules dosyasına "Master Context" eklenir. Cmd+K (Generate) veya Cmd+L (Chat) modlarında aşama aşama promptlar verilir.  
2. **Windsurf:** "Cascade" modu kullanılarak, projenin bağlamı (context) korunarak ardışık komutlar verilir.

### **5.1. Başlangıç: Proje Bağlamı ve Kurulum (Master Context)**

Bu prompt, AI asistanına projenin "kimliğini" ve teknik sınırlarını öğretir. Her oturumun başında veya .cursorrules dosyasında kullanılmalıdır.

**Prompt Adı:** LGS\_Zeka\_System\_Architecture

SİSTEM ROLÜ:  
Sen, Eğitim Teknolojileri (EdTech) alanında uzmanlaşmış, Python (Streamlit) ve PostgreSQL mimarisine hakim Kıdemli Yazılım Mimarisin. Görevin, "LGS-Zeka" adlı LGS hazırlık platformunu sıfırdan inşa etmektir.  
PROJE VİZYONU:  
LGS-Zeka, öğrencilerin deneme sınavı sonuçlarını takip eden, yapamadıkları soruları AI (Gemini) ile analiz eden ve kişiselleştirilmiş çalışma programları sunan bir web uygulamasıdır.  
**TEKNİK KISITLAR VE TERCİHLER:**

1. **Frontend/Framework:** Streamlit kullanılacak. Tasarım dili modern, minimalist ve öğrenci dostu olmalı. streamlit-option-menu ile sol navigasyon sağlanacak.  
2. **Veritabanı:** Prototip aşaması için Google Sheets (st.connection), nihai aşama için Supabase (PostgreSQL) kullanılacak. Kod modüler olmalı, veritabanı değişimi kolay yapılabilmeli.  
3. **AI Entegrasyonu:** google-generativeai kütüphanesi ile Gemini 1.5 Flash ve Pro modelleri kullanılacak.  
4. **Güvenlik:** API anahtarları ASLA koda gömülmeyecek, .streamlit/secrets.toml dosyasından çekilecek.  
5. **Kod Standartları:** PEP-8 uyumlu, docstring'leri yazılmış, tip tanımlamaları (type hinting) yapılmış Python kodu.

HEDEF:  
Bu oturumda seninle adım adım (Veritabanı \-\> AI Vision \-\> Dashboard \-\> Raporlama) ilerleyeceğiz. Her adımda benden onay almadan bir sonraki faza geçme. Kodları yazarken hata yönetimi (try-except) bloklarını ihmal etme.

### **5.2. Faz 1: Altyapı ve Veritabanı Katmanı Kurulumu**

Bu prompt, projenin dosya yapısını oluşturur ve veri bağlantısını sağlar.

**Prompt Adı:** Phase1\_Infrastructure\_Setup

**GÖREV: FAZ 1 \- Proje İskeleti ve Veri Katmanı**

Lütfen aşağıdaki adımları sırasıyla uygula:

1. **Dosya Yapısı:** Aşağıdaki klasör ağacını oluştur (veya oluşturmam için bash komutlarını ver):  
   * app.py: Ana uygulama dosyası.  
   * pages/: Sayfaların tutulacağı klasör (dashboard.py, ai\_koc.py, soru\_analiz.py).  
   * utils/: Yardımcı fonksiyonlar (db\_manager.py, gemini\_helper.py, auth.py).  
   * assets/: Logo ve CSS dosyaları.  
   * .streamlit/: Konfigürasyon ve secret dosyaları.  
   * requirements.txt: Gerekli kütüphaneler.  
2. **Requirements.txt:** Proje için gerekli şu kütüphaneleri ekle: streamlit, pandas, plotly, google-generativeai, streamlit-option-menu, st-annotated-text, gspread, oauth2client (Google Sheets için), supabase (ilerisi için).  
3. **Veritabanı Modülü (utils/db\_manager.py):**  
   * st.connection kullanarak Google Sheets bağlantısını kuran bir sınıf yaz.  
   * fetch\_data(sheet\_name) ve add\_data(sheet\_name, data\_dict) fonksiyonlarını oluştur.  
   * **Kritik:** Google Sheets API kotalarını aşmamak için st.cache\_data(ttl=60) dekoratörünü okuma fonksiyonlarına ekle.26  
   * **Veri Şeması:** Öğrenci verileri için şu sütunları varsay: Tarih, Ders (Matematik, Fen vb.), Konu, Doğru, Yanlış, Boş, Net, Görsel\_URL.  
4. **Secrets Yönetimi:** .streamlit/secrets.toml dosyasının şablonunu (örnek verilerle) hazırla. Hem Google Sheets hem de Gemini API key alanlarını göster.

### **5.3. Faz 2: AI Vision ve OCR Motoru (Soru Analizi)**

Bu prompt, Gemini API kullanarak görsel analizi yapan modülü yazdırır.

**Prompt Adı:** Phase2\_AI\_Vision\_Engine

**GÖREV: FAZ 2 \- AI Vision Entegrasyonu**

Şimdi utils/gemini\_helper.py dosyasını oluşturacağız. Bu modül, yüklenen matematik sorularını analiz edecek.

**Gereksinimler:**

1. **Model Yapılandırması:** google.generativeai kütüphanesini st.secrets içindeki API anahtarı ile başlat.  
2. **Fonksiyon:** analyze\_question\_image(image\_file, model\_type='flash') adında bir fonksiyon yaz.  
   * model\_type='flash' ise gemini-1.5-flash (Hız/Maliyet), pro ise gemini-1.5-pro (Yüksek Başarım) kullanılsın.  
3. Prompt Mühendisliği (System Instruction): Modele şu talimatı ver:  
   "Sen uzman bir LGS Matematik öğretmenisin. Görevin bu görseldeki soruyu analiz etmek. Çıktıyı SADECE geçerli bir JSON formatında ver. JSON yapısı:  
   {  
   'soru\_metni': 'Sorunun metni (Matematiksel ifadeler LaTeX formatında)',  
   'konu': 'Sorunun ait olduğu LGS konusu (örn: Üslü İfadeler)',  
   'cozum\_adimlari': \['Adım 1...', 'Adım 2...'\],  
   'dogru\_cevap': 'Varsa şıkkı veya sonucu',  
   'ipucu': 'Öğrenciye soruyu çözmesi için küçük bir ipucu',  
   'zorluk\_seviyesi': '1-5 arası tam sayı'  
   }"  
4. **Hata Yönetimi:** JSON ayrıştırma hatası olursa (model bazen düz metin dönebilir), ham metni güvenli bir şekilde döndür ve kullanıcıya uyarı göster. response\_schema parametresini kullanarak structured output (yapılandırılmış çıktı) zorlamayı dene.22  
5. **Görsel İşleme:** Streamlit file\_uploader'dan gelen veriyi PIL.Image formatına çevirerek API'ye gönder.

### **5.4. Faz 3: LGS Puan Hesaplama ve Dashboard Mantığı**

Bu prompt, matematiksel hesaplamaları ve görselleştirmeyi içerir.

**Prompt Adı:** Phase3\_Scoring\_and\_Dashboard

**GÖREV: FAZ 3 \- Puanlama Motoru ve Dashboard UI**

1. **Puanlama Modülü (utils/scoring.py):**  
   * LGS Puan hesaplama algoritmasını Python fonksiyonu olarak yaz.  
   * **Katsayılar:** Türkçe, Mat, Fen (4); İnkılap, Din, Dil (1).  
   * **Formül:** Net \= Doğru \- (Yanlış / 3). Puan hesaplarken varsayılan Standart Sapma ve Ortalama değerlerini kullan (Bu değerleri bir CONSTANTS sözlüğünde tut, kolay değişebilsin).  
2. **Dashboard Sayfası (pages/dashboard.py):**  
   * **Metrikler:** Sayfanın en üstünde st.metric kullanarak "Toplam Net", "Tahmini LGS Puanı", "Hedeflenen Puana Uzaklık" göster.  
   * **Grafik 1 (Gelişim):** Plotly Express Line Chart kullanarak, öğrencinin tarih bazlı net değişimini çiz. (X ekseni: Tarih, Y ekseni: Net, Renk: Ders).  
   * **Grafik 2 (Konu Analizi):** Öğrencinin en çok yanlış yaptığı konuları gösteren bir Bar Chart (Yatay Çubuk Grafik). "Matematik Dersi \- Konu Bazlı Yanlış Sayıları" başlığıyla.  
   * **Grafik 3 (Radar):** Ders bazlı dengeyi göstermek için Radar Chart (Örümcek Ağı Grafiği).  
3. **İnteraktivite:** Sol tarafta (Sidebar) Tarih Aralığı Filtresi ve Ders Filtresi ekle. Grafikler bu filtrelere göre dinamik güncellensin.

### **5.5. Faz 4: Sanal Koç ve İterasyon**

**Prompt Adı:** Phase4\_AI\_Coach\_Iterative

**GÖREV: FAZ 4 \- Sanal LGS Koçu**

pages/ai\_koc.py sayfasında çalışacak, öğrenciyle sohbet eden bir chatbot tasarla.

1. **Context (Bağlam) Yükleme:** Chatbot başlatıldığında, utils/db\_manager.py üzerinden öğrencinin son 5 deneme sonucunu ve en zayıf olduğu 3 konuyu çek.  
2. **System Prompt Enjeksiyonu:** Bu verileri System Prompt'a ekle: "Sen öğrencinin durumunu biliyorsun. Son denemede Matematik neti düşmüş. Konuşmalarında buna atıfta bulun ve moral ver."  
3. **Chat Arayüzü:** st.chat\_message ve st.chat\_input bileşenlerini kullan.  
4. **Streaming:** Gemini API'nin stream=True özelliğini kullanarak cevabın kelime kelime akmasını sağla (Daha doğal bir deneyim için).

## ---

**6\. Gelecek Vizyonu ve Sonuç**

LGS-Zeka projesi için yapılan detaylı teknik analiz, No-Code platformların eğitim teknolojileri alanındaki karmaşık veri ve algoritma ihtiyaçlarını karşılamakta yetersiz kaldığını net bir şekilde göstermektedir. Veri satır limitleri, API çağrı maliyetleri ve esneklik sorunları, projenin büyüme aşamasında aşılamaz duvarlar örmektedir.

Buna karşılık, Python ekosistemi (Streamlit, Supabase, Gemini API), hem maliyet etkinliği hem de sınırsız ölçeklenebilirlik sunmaktadır. Hazırlanan "Prompt Setleri" sayesinde, bu güçlü mimari Cursor ve Windsurf gibi yapay zeka araçlarıyla haftalar yerine günler içinde, kurumsal kalitede bir yazılım ürününe dönüştürülebilir. Bu yaklaşım, sadece bir uygulama geliştirmek değil, geleceğe dayanıklı (future-proof) bir eğitim platformu inşa etmek anlamına gelmektedir. Geliştirilen sistem, ileride mobil uygulamaya (Flutter/React Native) dönüştürülmek istendiğinde bile, Python backend ve veritabanı yapısı aynen korunarak büyük bir avantaj sağlayacaktır.

#### **Alıntılanan çalışmalar**

1. Python AI: Why Is Python So Good for Machine Learning? \- Netguru, erişim tarihi Aralık 4, 2025, [https://www.netguru.com/blog/python-machine-learning](https://www.netguru.com/blog/python-machine-learning)  
2. 8 Reasons Why Python is Good for AI and ML \- Django Stars, erişim tarihi Aralık 4, 2025, [https://djangostars.com/blog/why-python-is-good-for-artificial-intelligence-and-machine-learning/](https://djangostars.com/blog/why-python-is-good-for-artificial-intelligence-and-machine-learning/)  
3. erişim tarihi Aralık 4, 2025, [https://www.vegam.ai/no-code/limitations\#:\~:text=No%2Dcode%20platforms%20struggle%20with,or%20multi%2Dstep%20approval%20processes.](https://www.vegam.ai/no-code/limitations#:~:text=No%2Dcode%20platforms%20struggle%20with,or%20multi%2Dstep%20approval%20processes.)  
4. Glide's 2024 New Pricing: Pros, Cons, And Alternatives \- Jodoo Blog, erişim tarihi Aralık 4, 2025, [https://www.jodoo.com/blog/glides-2024-new-pricing-and-alternatives](https://www.jodoo.com/blog/glides-2024-new-pricing-and-alternatives)  
5. Restrictions, limits, and known issues \- AppSheet Help, erişim tarihi Aralık 4, 2025, [https://support.google.com/appsheet/answer/12653576?hl=en](https://support.google.com/appsheet/answer/12653576?hl=en)  
6. No Code Limitations: Understanding the Disadvantages and Restrictions, erişim tarihi Aralık 4, 2025, [https://www.vegam.ai/no-code/limitations](https://www.vegam.ai/no-code/limitations)  
7. Gemini Developer API pricing, erişim tarihi Aralık 4, 2025, [https://ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)  
8. Can Vision-Language Models Evaluate Handwritten Math? \- arXiv, erişim tarihi Aralık 4, 2025, [https://arxiv.org/html/2501.07244v1](https://arxiv.org/html/2501.07244v1)  
9. Row limit on Free plan \- Is it correct? \- Ask for Help \- Glide Community, erişim tarihi Aralık 4, 2025, [https://community.glideapps.com/t/row-limit-on-free-plan-is-it-correct/71443](https://community.glideapps.com/t/row-limit-on-free-plan-is-it-correct/71443)  
10. What limitations have you hit with no-code tools when building backends? \- Reddit, erişim tarihi Aralık 4, 2025, [https://www.reddit.com/r/nocode/comments/1jl1vym/what\_limitations\_have\_you\_hit\_with\_nocode\_tools/](https://www.reddit.com/r/nocode/comments/1jl1vym/what_limitations_have_you_hit_with_nocode_tools/)  
11. Why Python is the best for Artificial Intelligence and Machine Learning \- TriState Technology, erişim tarihi Aralık 4, 2025, [https://www.tristatetechnology.com/blog/why-is-python-the-best-for-artificial-intelligence-and-machine-learning](https://www.tristatetechnology.com/blog/why-is-python-the-best-for-artificial-intelligence-and-machine-learning)  
12. The top 5 limitations of no-code and low-code platforms \- Apptension, erişim tarihi Aralık 4, 2025, [https://www.apptension.com/blog-posts/no-code-and-low-code-limitations](https://www.apptension.com/blog-posts/no-code-and-low-code-limitations)  
13. lightgbm.LGBMRegressor — LightGBM 4.6.0.99 documentation, erişim tarihi Aralık 4, 2025, [https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html)  
14. DREAMTools: a Python package for scoring collaborative challenges \- PMC, erişim tarihi Aralık 4, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4837986/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4837986/)  
15. Builder.ai vs Bubble.io \- LowCode Agency, erişim tarihi Aralık 4, 2025, [https://www.lowcode.agency/blog/builder-ai-vs-bubble-io](https://www.lowcode.agency/blog/builder-ai-vs-bubble-io)  
16. Why Most Low-Code Platforms Eventually Face Limitations—and Strategic Considerations for the Future \- Baytech Consulting, erişim tarihi Aralık 4, 2025, [https://www.baytechconsulting.com/blog/why-most-low-code-platforms-eventually-face-limitations-and-strategic-considerations-for-the-future](https://www.baytechconsulting.com/blog/why-most-low-code-platforms-eventually-face-limitations-and-strategic-considerations-for-the-future)  
17. 5 Pros and Cons of No-Code Development for 2024 \- Northwest Executive Education, erişim tarihi Aralık 4, 2025, [https://northwest.education/insights/careers/5-pros-and-cons-of-no-code-development/](https://northwest.education/insights/careers/5-pros-and-cons-of-no-code-development/)  
18. Gemini vs. Vision AI: Which One Is Better at Identifying Images? \- Whitespark, erişim tarihi Aralık 4, 2025, [https://whitespark.ca/blog/gemini-vs-vision-ai-which-one-is-better-at-identifying-images/](https://whitespark.ca/blog/gemini-vs-vision-ai-which-one-is-better-at-identifying-images/)  
19. Gemini API quickstart \- Google AI for Developers, erişim tarihi Aralık 4, 2025, [https://ai.google.dev/gemini-api/docs/quickstart](https://ai.google.dev/gemini-api/docs/quickstart)  
20. None of the LLMs can truly replace a human for grading handwritten math exams, Gemini 2.5 Pro gets closest : r/singularity \- Reddit, erişim tarihi Aralık 4, 2025, [https://www.reddit.com/r/singularity/comments/1kobky6/none\_of\_the\_llms\_can\_truly\_replace\_a\_human\_for/](https://www.reddit.com/r/singularity/comments/1kobky6/none_of_the_llms_can_truly_replace_a_human_for/)  
21. Rate limits | Gemini API \- Google AI for Developers, erişim tarihi Aralık 4, 2025, [https://ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits)  
22. Structured Outputs | Gemini API \- Google AI for Developers, erişim tarihi Aralık 4, 2025, [https://ai.google.dev/gemini-api/docs/structured-output](https://ai.google.dev/gemini-api/docs/structured-output)  
23. | Understanding Streamlit Community Cloud Limits: Navigating Constraints and Maximizing Potential \- Streamoku, erişim tarihi Aralık 4, 2025, [https://www.streamoku.com/post/understanding-streamlit-community-cloud-limits-navigating-constraints-and-maximizing-potential](https://www.streamoku.com/post/understanding-streamlit-community-cloud-limits-navigating-constraints-and-maximizing-potential)  
24. App over its resource limits \- Streamlit forum, erişim tarihi Aralık 4, 2025, [https://discuss.streamlit.io/t/app-over-its-resource-limits/36667](https://discuss.streamlit.io/t/app-over-its-resource-limits/36667)  
25. Do you think it's worth learning Streamlit? Or should one stick to Flask or Django? : r/Python, erişim tarihi Aralık 4, 2025, [https://www.reddit.com/r/Python/comments/ynzbre/do\_you\_think\_its\_worth\_learning\_streamlit\_or/](https://www.reddit.com/r/Python/comments/ynzbre/do_you_think_its_worth_learning_streamlit_or/)  
26. What to do when a Streamlit Cloud Community App is hitting resource limits?, erişim tarihi Aralık 4, 2025, [https://community.snowflake.com/s/article/What-to-do-when-a-Streamlit-Cloud-Community-App-is-hitting-resource-limits](https://community.snowflake.com/s/article/What-to-do-when-a-Streamlit-Cloud-Community-App-is-hitting-resource-limits)