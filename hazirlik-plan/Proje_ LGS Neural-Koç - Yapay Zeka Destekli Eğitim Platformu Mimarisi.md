# **Proje: LGS Neural-Koç (Yapay Zeka Destekli Adaptif Öğrenme Mimarisi)**

Bu döküman, öğrencinin akademik performans verilerini işleyerek; kişiselleştirilmiş sınavlar oluşturan, eksik kazanımları tespit eden ve dinamik içerik üreten bir yazılım mimarisinin teknik tasarımını içerir. Hedef; manuel koçluk sürecini, veriye dayalı "Kurumsal Kaynak Planlaması" (ERP) disipliniyle yönetmektir.

## **1\. Sistem Mimarisi ve İş Akışı**

Sistem, **"Tanı (Diagnosis) \-\> Reçete (Prescription) \-\> Tedavi (Intervention)"** döngüsü üzerine kuruludur.

### **1.1. Veri Giriş Katmanı (Data Ingestion Layer)**

Yüklediğiniz deneme sınavı görselleri (Image 1-8) ham veridir. Bu verilerin sisteme "yapılandırılmış veri" olarak girmesi gerekir.

* **OCR & HTR (Handwritten Text Recognition):**  
  * **Teknoloji:** Google Cloud Vision API veya Mathpix (Matematiksel notasyon için).  
  * **İşlev:** Yüklediğiniz deneme kitapçığı fotoğraflarını tarar.  
  * **Kritik Özellik:** Sistem sadece şıkkı (A/B/C) değil, öğrencinin kağıt üzerindeki **"karalama yoğunluğunu"** analiz eder.  
  * *Analiz Mantığı:* Eğer bir matematik sorusunun etrafı bomboşsa "Boş Bırakıldı/Denemedi", çok fazla karalama ve silgi izi varsa "Uğraştı ama Bulamadı (Bilişsel Çaba Yüksek)", işlem hatası varsa "Dikkat Hatası" olarak etiketler.1

### **1.2. Etiketleme ve Taksonomi (Knowledge Graph)**

Her soru, MEB müfredatındaki en küçük yapı taşına (Micro-Skill) kadar etiketlenir.

* **Örnek (Image 2'deki Küp Sorusu):**  
  * *Ana Konu:* Kareköklü İfadeler.  
  * *Alt Konu:* Karekök içine alma / çıkarma.  
  * *Gerekli Beceri:* 3 Boyutlu Cisimlerin Açınımı (Uzamsal Zeka).  
  * *Tespit:* Öğrenci soruyu yanlış yaptıysa sistem "Kareköklü Sayılar" konusunu komple "bilmiyor" demez; **"Kareköklü sayılarda geometrik modelleme eksiği var"** tanısını koyar.

## ---

**2\. Algoritmik Strateji ve "Sıradaki Sınav" Üretimi**

Sistem, statik bir test kitabı yerine **"Bilgisayar Ortamında Bireyselleştirilmiş Test" (Computerized Adaptive Testing \- CAT)** mantığıyla çalışacaktır.3

### **2.1. Zorluk Seviyesi Algoritması (IRT \- Item Response Theory)**

Öğrencinin seviyesi 360-400 bandındadır. Bu seviyedeki öğrenciye sürekli "Zor" soru sormak motivasyonu, sürekli "Kolay" soru sormak gelişimi öldürür.

* **Algoritma:** $P(\\theta) \= c \+ (1-c) \\frac{1}{1+e^{-a(\\theta-b)}}$  
  * Sistem, öğrencinin "Yetenek Seviyesini ($\\theta$)" hesaplar.  
  * Bir sonraki deneme setini oluştururken, öğrencinin çözme ihtimalinin **%60 olduğu** (Hafif zorlayıcı \- Zone of Proximal Development) sorulardan oluşan bir havuz çeker.  
  * **Uygulama:** Öğrenci "Kareköklü Sayılar"da iyiyse, sistem ona "Yeni Nesil/Muhakeme" sorusu getirir. "DNA ve Genetik Kod"da zayıfsa (Image 7'deki hata), sistem ona önce "Kazanım/Temel Bilgi" sorusu getirir.

### **2.2. Dinamik Deneme Oluşturucu (The Generator)**

Elinizdeki veya piyasadaki kaynaklardan 8 taranmış sorular veritabanında "Zorluk (1-5)" ve "Konu" etiketiyle durur.

* **Senaryo:** B-1 denemesinde Matematik neti 5 geldi.  
* **Sistemin Ürettiği Görev:** "Bu hafta sonu çözülecek 20 soruluk *'Hibrit Mini Deneme'* şunları içermelidir:"  
  * 5 Adet: Çarpanlar Katlar (Kolay \- Moral düzeltmek için)  
  * 5 Adet: Üslü Sayılar (Orta \- Pekiştirmek için)  
  * 5 Adet: **Kareköklü Sayılar** (Zor \- B-1 denemesindeki hatayı telafi etmek için)  
  * 5 Adet: Mantık/Muhakeme (Türkçe paragraf \- Zihin jimnastiği)

## ---

**3\. İçerik Üretimi ve "RAG" Mimarisi (Retrieval-Augmented Generation)**

Sadece soru sormak yetmez, eksik konu için "nokta atışı" ders anlatımı gerekir. Burada **RAG (Retrieval-Augmented Generation)** teknolojisi devreye girer.5

### **3.1. Akıllı Özet Sistemi**

Sistem, öğrencinin yanlış yaptığı "Mevsimler ve İklim" (Image 1\) sorusunu analiz eder.

* **Prompt:** "Öğrenci, 'Eksen Eğikliğinin sonuçları' ile 'Gün Dönümü tarihlerini' karıştırıyor."  
* **Çıktı (AI Generation):** Sistem, tüm ders kitabını önüne koymak yerine, sadece bu karışıklığı giderecek 3 dakikalık bir okuma metni veya özel bir "Flashcard" (Bilgi Kartı) oluşturur.  
  * *Kart Önü:* 21 Haziran'da Kuzey Yarım Küre'de ne olur?  
  * *Kart Arkası:* En uzun gündüz yaşanır, Güneş ışınları Yengeç Dönencesine dik gelir.

### **3.2. Hata Defteri 2.0 (Dijital İkiz)**

Fiziksel kes-yapıştır yerine, sistem yanlış yapılan soruları dijital bir havuzda biriktirir.

* **Tekrar Döngüsü:** Yanlış yapılan soru, "Unutma Eğrisi"ne göre; 24 saat sonra, 3 gün sonra ve 1 hafta sonra tekrar karşısına çıkarılır. Öğrenci o soruyu doğru çözene kadar soru "Zombi" gibi peşini bırakmaz.

## ---

**4\. Uygulama Arayüzü ve Gamification (Kullanıcı Deneyimi)**

Dijital bağımlılığı (oyun/video) kırmak için, uygulamanın kendisi bir oyun gibi davranmalıdır.7

### **4.1. "Zeigarnik" Dashboard**

* **Tasarım:** Ana ekranda devasa bir "Tamamlanmamış Görevler" halkası olur. İnsan beyni yarım kalan işi bitirmeye meyillidir.  
* **Görev:** "Haftalık hedefin %85'i tamamlandı. Matematik bloğunu bitirirsen Seri (Streak) bozulmayacak."

### **4.2. Odak Modu (Focus Mode Integration)**

* **Özellik:** Uygulama "Sınav Modu"na alındığında, telefonun diğer özelliklerini kilitler (Android/iOS API izinleri ile).  
* **Pomodoro:** 25 dk ders \+ 5 dk mola. Ancak mola sırasında ekran kararır ve "Git su iç, ekrana bakma" uyarısı verir.

## ---

**5\. Eylem Planı: Bu Sistemi Nasıl Hayata Geçiririz?**

Bu sistemi "Custom Software" olarak yazmak aylar sürer. Ancak **No-Code** araçlarla MVP (Minimum Viable Product \- Prototip) hemen kurulabilir.

### **Adım 1: Veri Tabanı (Airtable / Google Sheets)**

* Tüm deneme sonuçlarını (Konu/Net/Yanlış Sayısı) buraya işleyeceğiz.  
* Sütunlar: Sınav Adı, Ders, Konu, Doğru/Yanlış, Hata Tipi (Dikkat/Bilgi).

### **Adım 2: Soru Bankası Havuzu (Notion)**

* Elinizdeki kaynakların fotoğraflarını çekip Notion veritabanına atın.  
* Her soruya "Etiket" atayın: \#Matematik, \#Zor, \#Kareköklü.

### **Adım 3: Analiz ve Görevlendirme (ChatGPT \+ Excel)**

* Haftalık olarak şu Prompt'u kullanacağız: *"Elimizdeki verilere göre, öğrenci Kareköklü sayılarda %40 başarıda, Üslü sayılarda %80 başarıda. Bana bu hafta için Kareköklü sayılar ağırlıklı, toplam 100 soruluk, zorluk seviyesi kademeli artan bir soru dağılım planı çıkar."*

### **Adım 4: Raporlama (PowerBI / Looker Studio)**

* Google Sheets'e bağlayacağımız basit bir dashboard ile "Matematik Net Artış Grafiği"ni görselleştirip, öğrencinin odasına asacağız. Görsel ilerleme, en büyük motivasyondur.

Bu yapı, öğrenciyi "rastgele test çözen" birinden, "stratejik ilerleyen" bir profesyonele dönüştürecektir. İlk adım olarak; B-1 denemesinin detaylı konu analizini (hangi sorunun hangi alt kazanım olduğu) bir Excel tablosuna işlememiz gerekecek.

#### **Alıntılanan çalışmalar**

1. 420 puan kaç yüzdelik dilim? \- Aradığınız cevap YaCevap'ta \- Yandex, erişim tarihi Aralık 2, 2025, [https://yandex.com.tr/yacevap/c/bilim-ve-egitim/q/420-puan-kac-yuzdelik-dilim-3253886047](https://yandex.com.tr/yacevap/c/bilim-ve-egitim/q/420-puan-kac-yuzdelik-dilim-3253886047)  
2. LGS'de matematikte en çok hangi konudan soru çıkıyor? \- Aradığınız cevap YaCevap'ta, erişim tarihi Aralık 2, 2025, [https://yandex.com.tr/yacevap/c/bilim-ve-egitim/q/lgs-de-matematikte-en-cok-hangi-konudan-soru-cikiyor-3411960674](https://yandex.com.tr/yacevap/c/bilim-ve-egitim/q/lgs-de-matematikte-en-cok-hangi-konudan-soru-cikiyor-3411960674)  
3. En İyi Paragraf Kitapları \- 2025-2026 \- TYT \- AYT \- 5 Öneri \- Gülhane Akademi, erişim tarihi Aralık 2, 2025, [https://www.gulhaneakademi.com/en-iyi-paragraf-kitaplari](https://www.gulhaneakademi.com/en-iyi-paragraf-kitaplari)  
4. 2025 LGS Fen Konuları ve LGS Fen Bilimleri Soru Dağılımı \- Özel Ders Alanı, erişim tarihi Aralık 2, 2025, [https://www.ozeldersalani.com/lgs-fen-konulari-ve-lgs-fen-bilimleri-soru-dagilimi](https://www.ozeldersalani.com/lgs-fen-konulari-ve-lgs-fen-bilimleri-soru-dagilimi)  
5. LGS Sürecinde Velilere Öneriler: Başarı İçin Rehber \- İkiartıbir, erişim tarihi Aralık 2, 2025, [https://ikiartibiregitim.com/blog/lgs-surecinde-velilere-oneriler/](https://ikiartibiregitim.com/blog/lgs-surecinde-velilere-oneriler/)  
6. ders çalışmak istemeyen çocukla başa çıkma yöntemleri \- Sınav Eğitim Kurumları, erişim tarihi Aralık 2, 2025, [https://sinav.com.tr/HaberDetay/genel/cocugum-ders-calismiyor-ne-yapabilirim-/22813](https://sinav.com.tr/HaberDetay/genel/cocugum-ders-calismiyor-ne-yapabilirim-/22813)  
7. Öğrenciler, Yeni Nesil Matematik Sorularını Çözebilmek İçin Nasıl Bir Yol İzlemelidir?-, erişim tarihi Aralık 2, 2025, [https://www.ogrencidoktoru.com/icerikler/icerik/kurumsal-makaleler/ogrenciler-yeni-nesil-matematik-sorularini-cozebilmek-icin-nasil-bir-yol-izlemelidir](https://www.ogrencidoktoru.com/icerikler/icerik/kurumsal-makaleler/ogrenciler-yeni-nesil-matematik-sorularini-cozebilmek-icin-nasil-bir-yol-izlemelidir)  
8. 2026 LGS Matematik Kaynak Önerileri: En İyi Soru Bankaları ve Denemeler, erişim tarihi Aralık 2, 2025, [https://www.mathclubs.org/post/lgs-2026-matematik-kaynak-%C3%B6nerileri](https://www.mathclubs.org/post/lgs-2026-matematik-kaynak-%C3%B6nerileri)